# Code Review Agent Command

**Command:** `/review-code`

**Description:** Validates code minimalism and removes bloat by analyzing Python code for quality issues, providing specific recommendations for improvement.

## Usage

```
/review-code [path] [--exclude dir1,dir2] [--format json|text]
```

### Parameters

- `path` (optional): Path to analyze (defaults to current working directory)
- `--exclude` (optional): Comma-separated list of directories to exclude
- `--format` (optional): Output format - 'json' for structured data or 'text' for human-readable report (default: text)

### Examples

```bash
# Review current directory
/review-code

# Review specific directory
/review-code src/

# Review with exclusions
/review-code --exclude tests,docs,venv

# Get JSON output for automation
/review-code --format json
```

## What It Analyzes

### Code Quality Checks

1. **Function Length**: Flags functions over 50 lines for decomposition
2. **Class Length**: Identifies classes exceeding 200 lines
3. **Cyclomatic Complexity**: Detects functions with complexity > 10
4. **Deep Nesting**: Finds overly nested code structures
5. **Long Parameter Lists**: Functions with > 5 parameters

### Bloat Detection

1. **Unused Imports**: Identifies imports not referenced in code
2. **Duplicate Logic**: Finds similar code patterns across modules
3. **Magic Numbers**: Detects hardcoded values that should be constants
4. **Code Smells**: Over-engineered solutions and unnecessary complexity

### Minimalism Validation

1. **Single Responsibility**: Ensures functions have focused purposes
2. **Essential Functionality**: Identifies non-essential code
3. **Simplification Opportunities**: Suggests cleaner implementations
4. **Import Optimization**: Recommends import consolidation

## Output

### Quality Score (0-100)
- **90-100**: Excellent - Minimal, clean code
- **80-89**: Good - Minor issues, mostly clean
- **70-79**: Fair - Some bloat, needs attention
- **60-69**: Poor - Significant issues
- **<60**: Critical - Major refactoring needed

### Issue Categories

- **High Severity**: Long functions/classes, high complexity, duplicate logic
- **Medium Severity**: Deep nesting, long parameter lists, code smells
- **Low Severity**: Unused imports, magic numbers, minor optimizations

### Recommendations

Each issue includes:
- **Specific Problem**: Exact location and description
- **Impact Assessment**: How it affects code quality
- **Recommended Fix**: Actionable improvement steps
- **Minimal Alternative**: Simpler implementation approach

## Standards Enforced

Based on CLAUDE.md project standards:

1. **Function Decomposition**: Break functions > 50 lines into focused units
2. **Logic Consolidation**: Extract common patterns into reusable components
3. **Import Cleanup**: Remove unused dependencies and optimize imports
4. **Complexity Reduction**: Simplify conditional logic and nested structures
5. **Essential Functionality**: Ensure every line serves a clear purpose

## Integration

This command integrates with the existing multi-agent architecture:

- Uses `CodeReviewAgent` from `src/agents/code_review_agent.py`
- Leverages AST analysis for accurate code parsing
- Provides actionable feedback aligned with project goals
- Supports both individual file and codebase-wide analysis

## Best Practices

1. **Run Before Commits**: Validate changes before version control
2. **Iterative Improvement**: Address high-severity issues first
3. **Team Standards**: Use for consistent code quality across team
4. **Automated Checks**: Integrate into CI/CD for quality gates
5. **Regular Reviews**: Periodic codebase health assessments

The agent enforces minimalism principles while maintaining full functionality, ensuring code remains clean, readable, and maintainable.