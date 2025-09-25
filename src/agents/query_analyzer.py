import re
from typing import Any, ClassVar, Dict, List, Union

from .base_agent import BaseAgent
from .models import Entities, QueryAnalyzerMetadata, QueryAnalyzerRequest, QueryAnalyzerResponse


class QueryAnalyzer(BaseAgent):
    financial_terms: ClassVar[Dict[str, List[str]]] = {
        "models": ["lstm", "cnn", "transformer", "mlp", "gru", "attention", "neural network"],
        "metrics": ["sharpe", "volatility", "var", "drawdown", "alpha", "beta", "return"],
        "concepts": ["trading", "prediction", "classification", "sentiment", "technical indicators"],
    }

    def __init__(self) -> None:
        super().__init__(name="QueryAnalyzer")

    def process(self, input_data: Union[QueryAnalyzerRequest, Dict[str, Any]]) -> QueryAnalyzerResponse:
        request = (
            input_data
            if isinstance(input_data, QueryAnalyzerRequest)
            else QueryAnalyzerRequest.model_validate(input_data)
        )

        if not self._is_llm_available():
            raise RuntimeError("Gemini client unavailable; set GEMINI_API_KEY before processing queries")

        metadata = self._llm_analyze_query(request.query)
        return QueryAnalyzerResponse(agent=self.name, content="Query analyzed", metadata=metadata)

    def _llm_analyze_query(self, query: str) -> QueryAnalyzerMetadata:
        response = self._generate_llm_response(
            "query_analyzer/financial_classification",
            {"query": query},
        )
        metadata = self._parse_llm_response(response)
        if metadata is None:
            raise ValueError("Unable to parse LLM response for query analysis")
        return metadata

    def _parse_llm_response(self, response: str) -> QueryAnalyzerMetadata | None:
        if not response:
            return None

        analysis = {
            "complexity": "moderate",
            "entities": {"models": [], "metrics": [], "concepts": []},
            "query_type": "factual",
            "financial_focus": "general",
        }

        response_lower = response.lower()

        if "complex" in response_lower:
            analysis["complexity"] = "complex"
        elif "simple" in response_lower:
            analysis["complexity"] = "simple"

        if any(word in response_lower for word in ["comparative", "comparison"]):
            analysis["query_type"] = "comparative"
        elif any(word in response_lower for word in ["methodology", "method"]):
            analysis["query_type"] = "methodology"
        elif any(word in response_lower for word in ["evaluation", "performance"]):
            analysis["query_type"] = "evaluation"

        if any(word in response_lower for word in ["crypto", "bitcoin"]):
            analysis["financial_focus"] = "cryptocurrency"
        elif any(word in response_lower for word in ["stock", "equity"]):
            analysis["financial_focus"] = "equity"
        elif "trading" in response_lower:
            analysis["financial_focus"] = "trading"

        analysis["entities"] = self._extract_entities(response_lower)

        try:
            return QueryAnalyzerMetadata(
                complexity=analysis["complexity"],
                entities=Entities(**analysis["entities"]),
                query_type=analysis["query_type"],
                financial_focus=analysis["financial_focus"],
            )
        except Exception:
            return None

    def _extract_entities(self, query: str) -> Dict[str, List[str]]:
        entities: Dict[str, List[str]] = {"models": [], "metrics": [], "concepts": []}
        for category, terms in self.financial_terms.items():
            matches = [term for term in terms if term in query]
            if matches:
                entities[category].extend(matches)
        return entities

