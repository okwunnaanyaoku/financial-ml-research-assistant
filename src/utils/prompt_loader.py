"""
Utility for loading and managing prompt templates.

This module provides functionality to load prompt templates from files
and substitute variables with actual values.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import re


class PromptLoader:
    """Utility class for loading and processing prompt templates."""

    def __init__(self, prompts_dir: Optional[str] = None):
        """Initialize the prompt loader.

        Args:
            prompts_dir: Directory containing prompt files. Defaults to project prompts directory.
        """
        if prompts_dir is None:
            # Default to prompts directory relative to this file
            current_dir = Path(__file__).parent
            self.prompts_dir = current_dir.parent.parent / 'prompts'
        else:
            self.prompts_dir = Path(prompts_dir)

        self.prompts_dir = self.prompts_dir.resolve()

    def load_prompt(self, prompt_name: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """Load a prompt template and substitute variables.

        Args:
            prompt_name: Name of the prompt file (without .txt extension)
            variables: Dictionary of variables to substitute in the template

        Returns:
            Processed prompt string with variables substituted

        Raises:
            FileNotFoundError: If the prompt file doesn't exist
            ValueError: If required variables are missing
        """
        prompt_file = self.prompts_dir / f"{prompt_name}.txt"

        if not prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                template = f.read()
        except IOError as e:
            raise IOError(f"Failed to read prompt file {prompt_file}: {e}")

        if variables:
            template = self._substitute_variables(template, variables)

        return template

    def _substitute_variables(self, template: str, variables: Dict[str, Any]) -> str:
        """Substitute variables in the template.

        Supports both {variable} and {{variable}} syntax.

        Args:
            template: Template string with variable placeholders
            variables: Dictionary of variable names and values

        Returns:
            Template with variables substituted

        Raises:
            ValueError: If required variables are missing
        """
        # Find all variable placeholders
        placeholders = re.findall(r'\{([^{}]+)\}', template)

        missing_vars = []
        for placeholder in placeholders:
            if placeholder not in variables:
                missing_vars.append(placeholder)

        if missing_vars:
            raise ValueError(f"Missing required variables: {missing_vars}")

        # Substitute variables
        result = template
        for var_name, value in variables.items():
            # Handle both {var} and {{var}} patterns
            result = result.replace(f"{{{var_name}}}", str(value))
            result = result.replace(f"{{{{{var_name}}}}}", str(value))

        return result

    def list_available_prompts(self) -> List[str]:
        """List all available prompt templates.

        Returns:
            List of prompt names (without .txt extension)
        """
        if not self.prompts_dir.exists():
            return []

        prompts = []
        for file in self.prompts_dir.glob('*.txt'):
            prompts.append(file.stem)

        return sorted(prompts)

    def get_prompt_path(self, prompt_name: str) -> Path:
        """Get the full path to a prompt file.

        Args:
            prompt_name: Name of the prompt file (without .txt extension)

        Returns:
            Path object pointing to the prompt file
        """
        return self.prompts_dir / f"{prompt_name}.txt"

    def prompt_exists(self, prompt_name: str) -> bool:
        """Check if a prompt template exists.

        Args:
            prompt_name: Name of the prompt file (without .txt extension)

        Returns:
            True if the prompt file exists, False otherwise
        """
        return self.get_prompt_path(prompt_name).exists()


# Convenience function for quick prompt loading
def load_prompt(prompt_name: str, variables: Optional[Dict[str, Any]] = None,
                prompts_dir: Optional[str] = None) -> str:
    """Convenience function to load a prompt template.

    Args:
        prompt_name: Name of the prompt file (without .txt extension)
        variables: Dictionary of variables to substitute in the template
        prompts_dir: Directory containing prompt files

    Returns:
        Processed prompt string with variables substituted
    """
    loader = PromptLoader(prompts_dir)
    return loader.load_prompt(prompt_name, variables)