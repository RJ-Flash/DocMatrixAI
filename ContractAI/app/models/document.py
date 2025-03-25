from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class DocumentBase(BaseModel):
    """Base document model."""
    name: str = Field(..., description="Document name")
    content_type: Optional[str] = Field(None, description="MIME type of the document")


class DocumentCreate(DocumentBase):
    """Document creation model."""
    pass


class DocumentUpdate(BaseModel):
    """Document update model."""
    name: Optional[str] = Field(None, description="Document name")
    status: Optional[str] = Field(None, description="Document processing status")


class DocumentResponse(DocumentBase):
    """Document response model."""
    id: int
    status: str = Field(..., description="Document processing status")
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True


class DocumentDetailResponse(DocumentResponse):
    """Detailed document response with analysis if available."""
    analysis: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """Response model for list of documents."""
    total: int
    documents: List[DocumentResponse]


class ClauseBase(BaseModel):
    """Base model for contract clauses."""
    type: str = Field(..., description="Clause type")
    text: str = Field(..., description="Clause text content")
    confidence: float = Field(..., description="Confidence score of detection")
    position: Dict[str, int] = Field(..., description="Position in document")


class RiskBase(BaseModel):
    """Base model for contract risks."""
    clause_type: str = Field(..., description="Type of clause containing the risk")
    risk_type: str = Field(..., description="Type of risk identified")
    risk_level: str = Field(..., description="Risk level (high, medium, low)")
    context: str = Field(..., description="Context surrounding the risk")


class ComparisonBase(BaseModel):
    """Base model for clause comparison results."""
    match_score: float = Field(..., description="Similarity score to standard clause")
    differences: List[Dict[str, Any]] = Field(..., description="Differences from standard")


class RecommendationBase(BaseModel):
    """Base model for recommendations."""
    risk_type: str = Field(..., description="Type of risk being addressed")
    recommendation: str = Field(..., description="Suggested action")
    context: str = Field(..., description="Context for the recommendation")
    priority: str = Field(..., description="Priority level (high, medium, low)")


class AnalysisResponse(BaseModel):
    """Response model for document analysis."""
    document_id: int
    clauses: List[ClauseBase] = Field(default_factory=list)
    risks: List[RiskBase] = Field(default_factory=list)
    comparisons: Dict[str, ComparisonBase] = Field(default_factory=dict)
    recommendations: List[RecommendationBase] = Field(default_factory=list)
    summary: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True