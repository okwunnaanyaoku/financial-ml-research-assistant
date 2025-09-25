
from typing import Any, ClassVar, Dict, List, Union

from .base_agent import BaseAgent
from .models import (
    DomainExpertAnalysis,
    DomainExpertMetadata,
    DomainExpertRequest,
    DomainExpertResponse,
    QueryAnalyzerMetadata,
    SourceInfo,
)
from retrieval.hybrid_search import HybridSearch


class DomainExpert(BaseAgent):
    """LLM-powered expert that analyzes retrieved chunks and surfaces citations."""

    MAX_CHUNKS_FOR_LLM: ClassVar[int] = 3
    MIN_SCORE_THRESHOLD: ClassVar[float] = 0.3
    MAX_TEXT_SNIPPET: ClassVar[int] = 300

    def __init__(self) -> None:
        super().__init__(name="DomainExpert")
        self.search_system = HybridSearch()

    def process(
        self, input_data: Union[DomainExpertRequest, Dict[str, Any]]
    ) -> DomainExpertResponse:
        request = (
            input_data
            if isinstance(input_data, DomainExpertRequest)
            else DomainExpertRequest.model_validate(input_data)
        )

        raw_chunks = self.search_system.search(request.query, k=5)
        chunks = self._select_high_value_chunks(raw_chunks)
        metadata = self._analyze_chunks(chunks, request.query_analysis, request.query)

        return DomainExpertResponse(
            agent=self.name,
            content="Expert analysis complete" if chunks else "No relevant information found",
            metadata=metadata,
        )

    def _select_high_value_chunks(
        self, chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        if not chunks:
            return []

        filtered = [
            chunk
            for chunk in chunks
            if chunk.get("hybrid_score", 0.0) >= self.MIN_SCORE_THRESHOLD
        ]

        selected = filtered if filtered else chunks
        return selected[: self.MAX_CHUNKS_FOR_LLM]

    def _analyze_chunks(
        self,
        chunks: List[Dict[str, Any]],
        query_analysis: QueryAnalyzerMetadata,
        query: str,
    ) -> DomainExpertMetadata:
        if not chunks:
            analysis = DomainExpertAnalysis(
                key_finding="No relevant information found",
                confidence=0.0,
                relevant_sections=[],
                methodology_insights=[],
                limitations=[],
            )
            return DomainExpertMetadata(analysis=analysis, sources=[])

        if not self._is_llm_available():
            raise RuntimeError(
                "Gemini client unavailable; set GEMINI_API_KEY before processing queries"
            )

        metadata = self._llm_analyze_content(chunks, query_analysis, query)
        if metadata is None:
            raise ValueError("Unable to parse LLM response for expert analysis")
        return metadata

    def _llm_analyze_content(
        self,
        chunks: List[Dict[str, Any]],
        query_analysis: QueryAnalyzerMetadata,
        query: str,
    ) -> DomainExpertMetadata | None:
        response = self._generate_llm_response(
            "domain_expert/content_analysis",
            {
                "query": query,
                "query_analysis": query_analysis.model_dump(),
                "chunks": self._format_chunks_for_llm(chunks),
            },
        )
        return self._parse_expert_response(response, chunks)

    def _format_chunks_for_llm(self, chunks: List[Dict[str, Any]]) -> str:
        formatted_chunks: List[str] = []
        for idx, chunk in enumerate(chunks, start=1):
            section = chunk["metadata"].get("section", "Unknown")
            text_snippet = chunk["text"][: self.MAX_TEXT_SNIPPET]
            score = chunk.get("hybrid_score", 0.0)
            formatted_chunks.append(
                f"**Chunk {idx}** (Section: {section}, Relevance: {score:.3f}):\n"
                f"{text_snippet}..."
            )
        return "\n\n".join(formatted_chunks)

    def _parse_expert_response(
        self, response: str, chunks: List[Dict[str, Any]]
    ) -> DomainExpertMetadata | None:
        if not response:
            return None

        response_lower = response.lower()
        sections_found = [chunk["metadata"].get("section", "Unknown") for chunk in chunks]
        unique_sections: List[str] = []
        seen: set[str] = set()
        for section in sections_found:
            if section and section not in seen:
                seen.add(section)
                unique_sections.append(section)

        avg_score = sum(chunk.get("hybrid_score", 0.0) for chunk in chunks) / len(chunks)
        confidence_factors = [
            len(response) > 200,
            any(word in response_lower for word in ["accuracy", "performance", "result"]),
            any(word in response_lower for word in ["lstm", "cnn", "neural", "model"]),
            avg_score > 0.3,
        ]
        base_confidence = min(avg_score * 1.5, 1.0)
        confidence_boost = sum(confidence_factors) * 0.1
        final_confidence = max(0.0, min(base_confidence + confidence_boost, 1.0))

        analysis = DomainExpertAnalysis(
            key_finding=response[:500] if len(response) > 500 else response,
            relevant_sections=unique_sections,
            confidence=round(final_confidence, 2),
            methodology_insights=self._extract_methodology_from_response(response),
            limitations=self._extract_limitations_from_response(response),
        )

        sources = [self._format_source(chunk) for chunk in chunks]
        return DomainExpertMetadata(analysis=analysis, sources=sources)

    def _extract_methodology_from_response(self, response: str) -> List[str]:
        methodologies: List[str] = []
        for sentence in response.split(". ")[:3]:
            if any(word in sentence.lower() for word in ["method", "algorithm", "approach", "model", "technique"]):
                methodologies.append(sentence.strip()[:100] + "...")
        return methodologies

    def _extract_limitations_from_response(self, response: str) -> List[str]:
        limitations: List[str] = []
        for sentence in response.split(". ")[:2]:
            if any(word in sentence.lower() for word in ["limitation", "constraint", "challenge", "drawback", "gap"]):
                limitations.append(sentence.strip()[:100] + "...")
        return limitations

    def _format_source(self, chunk: Dict[str, Any]) -> SourceInfo:
        metadata = chunk.get("metadata", {})
        return SourceInfo(
            section=metadata.get("section", "Unknown"),
            paper=(metadata.get("paper_title", "") or "Unknown")[:50] + "...",
            relevance_score=round(chunk.get("hybrid_score", 0.0), 3),
        )
