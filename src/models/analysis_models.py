from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from .agent_models import QueryType, ComplexityLevel, FinancialFocus

class EntityExtraction(BaseModel):
    models: List[str] = Field(default_factory=list, description="ML models mentioned")
    metrics: List[str] = Field(default_factory=list, description="Financial metrics mentioned")
    concepts: List[str] = Field(default_factory=list, description="Financial concepts mentioned")

class QueryAnalysis(BaseModel):
    complexity: ComplexityLevel = Field(..., description="Query complexity assessment")
    entities: EntityExtraction = Field(default_factory=EntityExtraction, description="Extracted entities")
    query_type: QueryType = Field(..., description="Classification of query type")
    financial_focus: FinancialFocus = Field(..., description="Financial domain focus")

class ExpertAnalysis(BaseModel):
    key_finding: str = Field(..., description="Primary finding from analysis")
    relevant_sections: List[str] = Field(default_factory=list, description="Relevant paper sections")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Analysis confidence")
    methodology_insights: List[str] = Field(default_factory=list, description="Methodology-related insights")
    limitations: List[str] = Field(default_factory=list, description="Identified limitations")

class ConfidenceScore(BaseModel):
    value: float = Field(..., ge=0.0, le=1.0, description="Confidence value")
    reasoning: str = Field(..., description="Explanation for confidence level")
    factors: List[str] = Field(default_factory=list, description="Factors affecting confidence")