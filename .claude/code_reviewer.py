import ast
import re
from pathlib import Path
from typing import Dict, List, Tuple

class MinimalCodeReviewer:
    def __init__(self, max_lines=50, max_complexity=10):
        self.max_lines = max_lines
        self.max_complexity = max_complexity

    def review_file(self, file_path: str) -> Dict:
        with open(file_path, 'r') as f:
            content = f.read()

        tree = ast.parse(content)
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                lines = node.end_lineno - node.lineno + 1
                if lines > self.max_lines:
                    issues.append(f"Function '{node.name}' has {lines} lines (max {self.max_lines})")

        imports = self._check_imports(content)
        duplicates = self._check_duplicates(content)

        return {
            'file': file_path,
            'issues': issues,
            'unused_imports': imports,
            'duplicate_patterns': duplicates,
            'score': max(0, 100 - len(issues) * 10 - len(imports) * 5)
        }

    def _check_imports(self, content: str) -> List[str]:
        import_lines = [line.strip() for line in content.split('\n') if line.strip().startswith(('import ', 'from '))]
        used_imports = []

        for imp in import_lines:
            module_name = imp.split()[1].split('.')[0]
            if module_name not in content.replace(imp, ''):
                used_imports.append(imp)

        return used_imports

    def _check_duplicates(self, content: str) -> List[str]:
        lines = content.split('\n')
        duplicates = []

        for i, line in enumerate(lines):
            if line.strip() and lines.count(line) > 1:
                duplicates.append(f"Duplicate line {i+1}: {line.strip()}")

        return list(set(duplicates))