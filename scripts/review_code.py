#!/usr/bin/env python3
"""
Script to execute code review via slash command integration.

This script provides the command-line interface for the /review-code slash command,
integrating with the CodeReviewAgent to analyze code quality and minimalism.
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.code_review_agent import CodeReviewAgent
import yaml


def load_config():
    """Load configuration from config.yaml."""
    config_path = Path(__file__).parent.parent / 'config.yaml'

    default_config = {
        'max_function_lines': 50,
        'max_class_lines': 200,
        'max_file_lines': 500,
        'max_complexity': 10
    }

    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f) or {}
                return {**default_config, **config.get('code_review', {})}
        except Exception as e:
            print(f"Warning: Failed to load config.yaml: {e}")
            return default_config

    return default_config


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Code Review Agent - Validates code minimalism and removes bloat',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python review_code.py                          # Review current directory
  python review_code.py src/                     # Review specific directory
  python review_code.py --exclude tests,docs    # Review with exclusions
  python review_code.py --format json           # Get JSON output
        """
    )

    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to analyze (default: current directory)'
    )

    parser.add_argument(
        '--exclude',
        type=str,
        help='Comma-separated list of directories to exclude'
    )

    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--file',
        type=str,
        help='Analyze a single file instead of directory'
    )

    parser.add_argument(
        '--score-only',
        action='store_true',
        help='Output only the quality score'
    )

    return parser.parse_args()


def main():
    """Main execution function."""
    args = parse_arguments()

    # Load configuration
    config = load_config()

    # Initialize the code review agent
    agent = CodeReviewAgent(config)

    try:
        if args.file:
            # Analyze single file
            if not os.path.exists(args.file):
                print(f"Error: File '{args.file}' not found", file=sys.stderr)
                sys.exit(1)

            if not args.file.endswith('.py'):
                print(f"Error: File '{args.file}' is not a Python file", file=sys.stderr)
                sys.exit(1)

            results = agent.review_file(args.file)

            if args.score_only:
                print(results['score'])
                return

            # Convert single file results to codebase format
            codebase_results = {
                'overall_score': results['score'],
                'files_analyzed': 1,
                'issues': results['issues'],
                'file_reports': {args.file: results},
                'summary': {
                    'total_issues': sum(len(issues) for issues in results['issues'].values()),
                    'issue_breakdown': {k: len(v) for k, v in results['issues'].items()},
                    'files_with_issues': 1 if any(results['issues'].values()) else 0,
                    'average_score': results['score']
                },
                'recommendations': agent._generate_recommendations({'issues': results['issues']})
            }

        else:
            # Analyze directory/codebase
            if not os.path.exists(args.path):
                print(f"Error: Path '{args.path}' not found", file=sys.stderr)
                sys.exit(1)

            exclude_dirs = set()
            if args.exclude:
                exclude_dirs = set(dir.strip() for dir in args.exclude.split(','))

            codebase_results = agent.review_codebase(args.path, exclude_dirs)

            if args.score_only:
                print(f"{codebase_results['overall_score']:.1f}")
                return

        # Output results
        if args.format == 'json':
            print(json.dumps(codebase_results, indent=2))
        else:
            # Text format
            report = agent.format_report(codebase_results)
            print(report)

            # Add file-specific details for multi-file analysis
            if not args.file and codebase_results['files_analyzed'] > 1:
                print("\n" + "=" * 60)
                print("FILE DETAILS")
                print("=" * 60)

                # Show worst scoring files
                file_scores = [
                    (path, report['score'])
                    for path, report in codebase_results['file_reports'].items()
                    if not report.get('error')
                ]
                file_scores.sort(key=lambda x: x[1])

                if file_scores:
                    print("\nLowest Scoring Files:")
                    for path, score in file_scores[:5]:
                        print(f"  {score:5.1f} - {path}")

                # Show files with errors
                error_files = [
                    (path, report['error'])
                    for path, report in codebase_results['file_reports'].items()
                    if report.get('error')
                ]

                if error_files:
                    print(f"\nFiles with Errors ({len(error_files)}):")
                    for path, error in error_files[:3]:
                        print(f"  {path}: {error}")
                    if len(error_files) > 3:
                        print(f"  ... and {len(error_files) - 3} more")

        # Set exit code based on quality score
        if codebase_results['overall_score'] < 60:
            sys.exit(2)  # Critical quality issues
        elif codebase_results['overall_score'] < 80:
            sys.exit(1)  # Quality issues found
        else:
            sys.exit(0)  # Good quality

    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()