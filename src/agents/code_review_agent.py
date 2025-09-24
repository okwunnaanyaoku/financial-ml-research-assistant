"""
Code Review Agent for validating code minimalism and removing bloat.

This agent analyzes Python code for quality issues and provides specific
recommendations for improvement, focusing on minimalism and functionality.
"""

import ast
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any, Optional
import importlib.util

from ..utils.prompt_loader import PromptLoader


class CodeReviewAgent:
    """Agent that validates code minimalism and identifies bloat."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the code review agent.

        Args:
            config: Configuration dictionary with thresholds and settings
        """
        self.config = config
        self.prompt_loader = PromptLoader()

        # Default thresholds
        self.max_function_lines = config.get('max_function_lines', 50)
        self.max_class_lines = config.get('max_class_lines', 200)
        self.max_file_lines = config.get('max_file_lines', 500)
        self.max_complexity = config.get('max_complexity', 10)

        # Track analysis results
        self.analysis_results = {}

    def review_codebase(self, root_path: str, exclude_dirs: Set[str] = None) -> Dict[str, Any]:
        """Review an entire codebase for quality issues.

        Args:
            root_path: Root directory to analyze
            exclude_dirs: Directories to exclude from analysis

        Returns:
            Dictionary containing comprehensive analysis results
        """
        if exclude_dirs is None:
            exclude_dirs = {'.git', '__pycache__', '.pytest_cache', 'venv', 'env'}

        python_files = self._find_python_files(root_path, exclude_dirs)

        results = {
            'overall_score': 0,
            'files_analyzed': len(python_files),
            'issues': defaultdict(list),
            'recommendations': [],
            'file_reports': {},
            'summary': {}
        }

        total_score = 0
        file_count = 0

        for file_path in python_files:
            file_report = self.review_file(file_path)
            results['file_reports'][file_path] = file_report

            # Aggregate issues
            for issue_type, issues in file_report['issues'].items():
                results['issues'][issue_type].extend(issues)

            total_score += file_report['score']
            file_count += 1

        # Calculate overall score
        results['overall_score'] = total_score / file_count if file_count > 0 else 0

        # Generate summary and recommendations
        results['summary'] = self._generate_summary(results)
        results['recommendations'] = self._generate_recommendations(results)

        return results

    def review_file(self, file_path: str) -> Dict[str, Any]:
        """Review a single Python file for quality issues.

        Args:
            file_path: Path to the Python file

        Returns:
            Dictionary containing file analysis results
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (IOError, UnicodeDecodeError) as e:
            return {
                'score': 0,
                'error': f"Failed to read file: {e}",
                'issues': {},
                'metrics': {}
            }

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            return {
                'score': 0,
                'error': f"Syntax error: {e}",
                'issues': {},
                'metrics': {}
            }

        # Analyze the file
        issues = defaultdict(list)
        metrics = self._calculate_metrics(content, tree, file_path)

        # Check for various issues
        issues.update(self._check_function_length(tree, content))
        issues.update(self._check_class_length(tree, content))
        issues.update(self._check_duplicated_logic(tree))
        issues.update(self._check_unused_imports(tree, content))
        issues.update(self._check_complexity(tree))
        issues.update(self._check_code_smells(tree, content))

        # Calculate quality score
        score = self._calculate_quality_score(issues, metrics)

        return {
            'score': score,
            'issues': dict(issues),
            'metrics': metrics,
            'file_path': file_path
        }

    def _find_python_files(self, root_path: str, exclude_dirs: Set[str]) -> List[str]:
        """Find all Python files in the given directory."""
        python_files = []

        for root, dirs, files in os.walk(root_path):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))

        return python_files

    def _calculate_metrics(self, content: str, tree: ast.AST, file_path: str) -> Dict[str, Any]:
        """Calculate various code metrics."""
        lines = content.split('\n')

        return {
            'total_lines': len(lines),
            'code_lines': len([line for line in lines if line.strip() and not line.strip().startswith('#')]),
            'comment_lines': len([line for line in lines if line.strip().startswith('#')]),
            'blank_lines': len([line for line in lines if not line.strip()]),
            'functions': len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]),
            'classes': len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]),
            'imports': len([node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]),
            'file_path': file_path
        }

    def _check_function_length(self, tree: ast.AST, content: str) -> Dict[str, List[Dict]]:
        """Check for functions that exceed maximum line limit."""
        issues = defaultdict(list)
        lines = content.split('\n')

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                start_line = node.lineno
                end_line = node.end_lineno or start_line
                function_lines = end_line - start_line + 1

                if function_lines > self.max_function_lines:
                    issues['long_functions'].append({
                        'function': node.name,
                        'lines': function_lines,
                        'start_line': start_line,
                        'end_line': end_line,
                        'severity': 'high' if function_lines > self.max_function_lines * 1.5 else 'medium',
                        'description': f"Function '{node.name}' has {function_lines} lines (limit: {self.max_function_lines})"
                    })

        return issues

    def _check_class_length(self, tree: ast.AST, content: str) -> Dict[str, List[Dict]]:
        """Check for classes that exceed maximum line limit."""
        issues = defaultdict(list)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                start_line = node.lineno
                end_line = node.end_lineno or start_line
                class_lines = end_line - start_line + 1

                if class_lines > self.max_class_lines:
                    issues['long_classes'].append({
                        'class': node.name,
                        'lines': class_lines,
                        'start_line': start_line,
                        'end_line': end_line,
                        'severity': 'high' if class_lines > self.max_class_lines * 1.5 else 'medium',
                        'description': f"Class '{node.name}' has {class_lines} lines (limit: {self.max_class_lines})"
                    })

        return issues

    def _check_duplicated_logic(self, tree: ast.AST) -> Dict[str, List[Dict]]:
        """Check for duplicated logic patterns."""
        issues = defaultdict(list)

        # Track similar code blocks by their AST structure
        code_blocks = defaultdict(list)

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.For, ast.While, ast.If)):
                # Generate a simplified signature for comparison
                signature = self._generate_code_signature(node)
                if signature:
                    code_blocks[signature].append({
                        'node': node,
                        'type': type(node).__name__,
                        'line': node.lineno,
                        'name': getattr(node, 'name', f"{type(node).__name__}_at_line_{node.lineno}")
                    })

        # Find duplicates
        for signature, blocks in code_blocks.items():
            if len(blocks) > 1:
                issues['duplicated_logic'].append({
                    'signature': signature,
                    'occurrences': len(blocks),
                    'locations': [(block['name'], block['line']) for block in blocks],
                    'severity': 'high' if len(blocks) > 2 else 'medium',
                    'description': f"Similar code pattern found in {len(blocks)} locations"
                })

        return issues

    def _check_unused_imports(self, tree: ast.AST, content: str) -> Dict[str, List[Dict]]:
        """Check for unused imports."""
        issues = defaultdict(list)

        # Collect all imports
        imports = set()
        import_nodes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname or alias.name
                    imports.add(name.split('.')[0])
                    import_nodes.append((node.lineno, alias.name, name))
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        name = alias.asname or alias.name
                        imports.add(name)
                        import_nodes.append((node.lineno, f"{node.module}.{alias.name}", name))

        # Check usage in code
        used_imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used_imports.add(node.id)
            elif isinstance(node, ast.Attribute):
                # Handle attribute access like module.function
                if isinstance(node.value, ast.Name):
                    used_imports.add(node.value.id)

        # Find unused imports
        for line, full_name, import_name in import_nodes:
            if import_name not in used_imports:
                # Check if it's used in string literals (like __all__)
                if not re.search(rf'\b{re.escape(import_name)}\b', content):
                    issues['unused_imports'].append({
                        'import': full_name,
                        'line': line,
                        'severity': 'low',
                        'description': f"Unused import '{full_name}' at line {line}"
                    })

        return issues

    def _check_complexity(self, tree: ast.AST) -> Dict[str, List[Dict]]:
        """Check cyclomatic complexity of functions."""
        issues = defaultdict(list)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_cyclomatic_complexity(node)
                if complexity > self.max_complexity:
                    issues['high_complexity'].append({
                        'function': node.name,
                        'complexity': complexity,
                        'line': node.lineno,
                        'severity': 'high' if complexity > self.max_complexity * 1.5 else 'medium',
                        'description': f"Function '{node.name}' has complexity {complexity} (limit: {self.max_complexity})"
                    })

        return issues

    def _check_code_smells(self, tree: ast.AST, content: str) -> Dict[str, List[Dict]]:
        """Check for various code smells."""
        issues = defaultdict(list)

        # Check for overly nested code
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                max_depth = self._calculate_nesting_depth(node)
                if max_depth > 4:
                    issues['deep_nesting'].append({
                        'function': node.name,
                        'depth': max_depth,
                        'line': node.lineno,
                        'severity': 'medium',
                        'description': f"Function '{node.name}' has deep nesting (depth: {max_depth})"
                    })

        # Check for magic numbers
        for node in ast.walk(tree):
            if isinstance(node, ast.Num) and isinstance(node.n, (int, float)):
                # Skip common acceptable numbers
                if node.n not in [0, 1, -1, 2, 10, 100, 1000]:
                    issues['magic_numbers'].append({
                        'value': node.n,
                        'line': node.lineno,
                        'severity': 'low',
                        'description': f"Magic number {node.n} found at line {node.lineno}"
                    })

        # Check for long parameter lists
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                param_count = len(node.args.args) + len(node.args.kwonlyargs)
                if param_count > 5:
                    issues['long_parameter_list'].append({
                        'function': node.name,
                        'parameters': param_count,
                        'line': node.lineno,
                        'severity': 'medium',
                        'description': f"Function '{node.name}' has {param_count} parameters"
                    })

        return issues

    def _generate_code_signature(self, node: ast.AST) -> str:
        """Generate a simplified signature for code comparison."""
        try:
            # Create a simplified representation of the AST structure
            if isinstance(node, ast.FunctionDef):
                return f"func_{len(node.args.args)}_{len(node.body)}"
            elif isinstance(node, ast.For):
                return f"for_{len(node.body)}_{len(node.orelse)}"
            elif isinstance(node, ast.While):
                return f"while_{len(node.body)}_{len(node.orelse)}"
            elif isinstance(node, ast.If):
                return f"if_{len(node.body)}_{len(node.orelse)}"
            return ""
        except AttributeError:
            return ""

    def _calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.AsyncWith, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1

        return complexity

    def _calculate_nesting_depth(self, node: ast.AST, current_depth: int = 0) -> int:
        """Calculate maximum nesting depth in a function."""
        max_depth = current_depth

        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                depth = self._calculate_nesting_depth(child, current_depth + 1)
                max_depth = max(max_depth, depth)
            else:
                depth = self._calculate_nesting_depth(child, current_depth)
                max_depth = max(max_depth, depth)

        return max_depth

    def _calculate_quality_score(self, issues: Dict[str, List], metrics: Dict[str, Any]) -> int:
        """Calculate a quality score based on issues found."""
        base_score = 100

        # Deduct points for different types of issues
        severity_weights = {'high': 10, 'medium': 5, 'low': 2}

        for issue_type, issue_list in issues.items():
            for issue in issue_list:
                severity = issue.get('severity', 'medium')
                base_score -= severity_weights.get(severity, 5)

        # Additional deductions based on metrics
        if metrics.get('total_lines', 0) > self.max_file_lines:
            base_score -= 10

        # Ensure score is between 0 and 100
        return max(0, min(100, base_score))

    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the analysis results."""
        total_issues = sum(len(issues) for issues in results['issues'].values())

        issue_breakdown = {
            issue_type: len(issues)
            for issue_type, issues in results['issues'].items()
        }

        return {
            'total_issues': total_issues,
            'issue_breakdown': issue_breakdown,
            'files_with_issues': len([
                report for report in results['file_reports'].values()
                if any(report['issues'].values())
            ]),
            'average_score': results['overall_score']
        }

    def _generate_recommendations(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific recommendations based on analysis results."""
        recommendations = []

        # Function length recommendations
        if 'long_functions' in results['issues']:
            recommendations.append({
                'type': 'function_decomposition',
                'priority': 'high',
                'title': 'Break down long functions',
                'description': f"Found {len(results['issues']['long_functions'])} functions exceeding {self.max_function_lines} lines",
                'action': 'Extract logical chunks into separate functions with single responsibilities'
            })

        # Duplicate logic recommendations
        if 'duplicated_logic' in results['issues']:
            recommendations.append({
                'type': 'logic_consolidation',
                'priority': 'high',
                'title': 'Consolidate duplicate logic',
                'description': f"Found {len(results['issues']['duplicated_logic'])} instances of duplicated code patterns",
                'action': 'Extract common logic into reusable functions or classes'
            })

        # Import cleanup recommendations
        if 'unused_imports' in results['issues']:
            recommendations.append({
                'type': 'import_cleanup',
                'priority': 'low',
                'title': 'Remove unused imports',
                'description': f"Found {len(results['issues']['unused_imports'])} unused imports",
                'action': 'Remove imports that are not used in the code'
            })

        # Complexity reduction recommendations
        if 'high_complexity' in results['issues']:
            recommendations.append({
                'type': 'complexity_reduction',
                'priority': 'medium',
                'title': 'Reduce function complexity',
                'description': f"Found {len(results['issues']['high_complexity'])} functions with high complexity",
                'action': 'Break complex functions into smaller, more focused functions'
            })

        return recommendations

    def format_report(self, results: Dict[str, Any]) -> str:
        """Format the analysis results into a readable report."""
        report_lines = []

        # Header
        report_lines.append("=" * 60)
        report_lines.append("CODE REVIEW REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Overall Quality Score: {results['overall_score']:.1f}/100")
        report_lines.append(f"Files Analyzed: {results['files_analyzed']}")
        report_lines.append("")

        # Summary
        summary = results['summary']
        report_lines.append("SUMMARY")
        report_lines.append("-" * 20)
        report_lines.append(f"Total Issues: {summary['total_issues']}")
        report_lines.append(f"Files with Issues: {summary['files_with_issues']}")
        report_lines.append("")

        # Issue breakdown
        if summary['issue_breakdown']:
            report_lines.append("Issue Breakdown:")
            for issue_type, count in summary['issue_breakdown'].items():
                report_lines.append(f"  - {issue_type.replace('_', ' ').title()}: {count}")
            report_lines.append("")

        # Recommendations
        if results['recommendations']:
            report_lines.append("RECOMMENDATIONS")
            report_lines.append("-" * 20)
            for i, rec in enumerate(results['recommendations'], 1):
                report_lines.append(f"{i}. {rec['title']} ({rec['priority']} priority)")
                report_lines.append(f"   {rec['description']}")
                report_lines.append(f"   Action: {rec['action']}")
                report_lines.append("")

        # Detailed issues
        if results['issues']:
            report_lines.append("DETAILED ISSUES")
            report_lines.append("-" * 20)

            for issue_type, issues in results['issues'].items():
                if issues:
                    report_lines.append(f"\n{issue_type.replace('_', ' ').title()}:")
                    for issue in issues[:5]:  # Limit to top 5 per category
                        report_lines.append(f"  - {issue['description']}")
                    if len(issues) > 5:
                        report_lines.append(f"  ... and {len(issues) - 5} more")

        return "\n".join(report_lines)