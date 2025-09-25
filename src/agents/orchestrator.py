from typing import Any, Dict, Union

from .base_agent import BaseAgent
from .domain_expert import DomainExpert
from .models import (
    DomainExpertMetadata,
    DomainExpertRequest,
    OrchestratorMetadata,
    OrchestratorRequest,
    OrchestratorResponse,
    QueryAnalyzerRequest,
    QueryAnalyzerMetadata,
    SourceInfo,
)
from .query_analyzer import QueryAnalyzer


class Orchestrator(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="Orchestrator")
        self.query_analyzer = QueryAnalyzer()
        self.domain_expert = DomainExpert()

    def process(self, input_data: Union[OrchestratorRequest, Dict[str, Any]]) -> OrchestratorResponse:
        request = (
            input_data
            if isinstance(input_data, OrchestratorRequest)
            else OrchestratorRequest.model_validate(input_data)
        )

        if not self._is_llm_available():
            raise RuntimeError("Gemini client unavailable; set GEMINI_API_KEY before processing queries")

        query_analysis = self.query_analyzer.process(
            QueryAnalyzerRequest(query=request.query)
        )

        expert_response = self.domain_expert.process(
            DomainExpertRequest(
                query=request.query,
                query_analysis=query_analysis.metadata,
            )
        )

        final_content = self._llm_synthesize_response(
            request.query,
            query_analysis.metadata,
            expert_response.metadata,
        )

        if not final_content:
            raise ValueError("LLM failed to synthesize orchestrated response")

        return OrchestratorResponse(
            agent=self.name,
            content=final_content,
            metadata=OrchestratorMetadata(
                query_analysis=query_analysis.metadata,
                expert_analysis=expert_response.metadata,
            ),
        )

    def _llm_synthesize_response(
        self,
        query: str,
        query_analysis: QueryAnalyzerMetadata,
        expert_analysis: DomainExpertMetadata,
    ) -> str:
        sources_text = self._format_sources_for_llm(expert_analysis.sources)
        return self._generate_llm_response(
            "orchestrator/response_synthesis",
            {
                "query": query,
                "query_analysis": query_analysis.model_dump(),
                "expert_analysis": expert_analysis.analysis.model_dump(),
                "sources": sources_text,
            },
        )

    def _format_sources_for_llm(self, sources: list[SourceInfo]) -> str:
        if not sources:
            return "No specific sources available"

        formatted: list[str] = []
        for source in sources[:3]:
            section = source.section or "Unknown"
            formatted.append(f"- {section} (relevance: {source.relevance_score:.3f})")
        return "\n".join(formatted)

