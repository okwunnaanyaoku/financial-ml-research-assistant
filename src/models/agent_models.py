from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class QueryType(str, Enum):
    FACTUAL = "factual"
    COMPARATIVE = "comparative"
    METHODOLOGY = "methodology"
    EVALUATION = "evaluation"

class ComplexityLevel(str, Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"

class FinancialFocus(str, Enum):
    CRYPTOCURRENCY = "cryptocurrency"
    EQUITY = "equity"
    TRADING = "trading"
    GENERAL = "general"

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The research query")
    context: Optional[str] = Field(None, description="Additional context")

class QueryResponse(BaseModel):
    content: str = Field(..., description="Generated response content")
    sources: List[str] = Field(default_factory=list, description="Source references")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Response metadata")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score")

class AgentMessage(BaseModel):
    agent: str = Field(..., description="Agent name")
    content: str = Field(..., description="Message content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Agent-specific metadata")

class RetrievalResult(BaseModel):
    chunk_id: str = Field(..., description="Unique chunk identifier")
    text: str = Field(..., description="Retrieved text content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Chunk metadata")
    hybrid_score: float = Field(..., ge=0.0, description="Hybrid search relevance score")