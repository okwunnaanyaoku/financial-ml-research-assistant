from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import sys
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

sys.path.append(str(Path(__file__).parent.parent))
from llm.gemini_client import gemini_client
from utils.prompt_loader import load_prompt


class BaseAgent(BaseModel, ABC):
    name: str
    llm_client: Any = Field(default_factory=lambda: gemini_client)

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        ...

    def _format_response(self, content: str, metadata: Dict | None = None) -> Dict[str, Any]:
        return {
            "agent": self.name,
            "content": content,
            "metadata": metadata or {}
        }

    def _validate_input(self, input_data: Dict[str, Any], required_keys: list[str]) -> bool:
        return all(key in input_data for key in required_keys)

    def _generate_llm_response(
        self,
        prompt_name: str,
        variables: Optional[Dict[str, Any]] = None,
        temperature: Optional[float] = None
    ) -> str:
        try:
            prompt = load_prompt(prompt_name, **(variables or {}))
            return self.llm_client.generate_response(prompt, temperature)
        except Exception as exc:  # pragma: no cover - defensive
            return f"Error generating LLM response: {exc}"

    def _is_llm_available(self) -> bool:
        return self.llm_client.is_available()
