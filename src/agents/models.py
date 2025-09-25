from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field


class QueryAnalyzerRequest(BaseModel):
    query: str = Field(..., min_length=1)

    model_config = ConfigDict(str_strip_whitespace=True)


class Entities(BaseModel):
    models: List[str] = Field(default_factory=list)
    metrics: List[str] = Field(default_factory=list)
    concepts: List[str] = Field(default_factory=list)


class QueryAnalyzerMetadata(BaseModel):
    complexity: Literal["simple", "moderate", "complex"]
    entities: Entities
    query_type: Literal["factual", "comparative", "methodology", "evaluation"]
    financial_focus: Literal["general", "equity", "cryptocurrency", "trading"]


class QueryAnalyzerResponse(BaseModel):
    agent: str
    content: str
    metadata: QueryAnalyzerMetadata

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def as_dict(self) -> dict:
        return self.model_dump()


class DomainExpertRequest(BaseModel):
    query: str
    query_analysis: QueryAnalyzerMetadata

    model_config = ConfigDict(str_strip_whitespace=True)


class SourceInfo(BaseModel):
    section: str
    paper: str
    relevance_score: float


class DomainExpertAnalysis(BaseModel):
    key_finding: str
    relevant_sections: List[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    methodology_insights: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class DomainExpertMetadata(BaseModel):
    analysis: DomainExpertAnalysis
    sources: List[SourceInfo] = Field(default_factory=list)


class DomainExpertResponse(BaseModel):
    agent: str
    content: str
    metadata: DomainExpertMetadata

    def as_dict(self) -> dict:
        return self.model_dump()


class OrchestratorRequest(BaseModel):
    query: str

    model_config = ConfigDict(str_strip_whitespace=True)


class OrchestratorMetadata(BaseModel):
    query_analysis: QueryAnalyzerMetadata
    expert_analysis: DomainExpertMetadata


class OrchestratorResponse(BaseModel):
    agent: str
    content: str
    metadata: OrchestratorMetadata

    def as_dict(self) -> dict:
        return self.model_dump()
