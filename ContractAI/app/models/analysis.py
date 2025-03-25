from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ClauseCreate(BaseModel):
    """Model for creating a clause."""
    type: str = Field(..., description="Clause type")
    text: str = Field(..., description="Clause text content")
    confidence: float = Field(..., description="Confidence score of detection")
    position: Dict[str, int] = Field(..., description="Position in document")
    context: Optional[str] = Field(None, description="Context surrounding the clause")


class RiskCreate(BaseModel):
    """Model for creating a risk."""
    clause_type: str = Field(..., description="Type of clause containing the risk")
    risk_type: str = Field(..., description="Type of risk identified")
    risk_level: str = Field(..., description="Risk level (high, medium, low)")
    context: str = Field(..., description="Context surrounding the risk")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional risk details")


class ComparisonCreate(BaseModel):
    """Model for creating a comparison."""
    match_score: float = Field(..., description="Similarity score to standard clause")
    differences: List[Dict[str, Any]] = Field(..., description="Differences from standard")
    standard_text: str = Field(..., description="Text of the standard clause")
    document_text: str = Field(..., description="Text from the document")


class RecommendationCreate(BaseModel):
    """Model for creating a recommendation."""
    risk_type: str = Field(..., description="Type of risk being addressed")
    recommendation: str = Field(..., description="Suggested action")
    context: str = Field(..., description="Context for the recommendation")
    priority: str = Field(..., description="Priority level (high, medium, low)")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional recommendation details")


class AnalysisCreate(BaseModel):
    """Model for creating an analysis."""
    document_id: int = Field(..., description="Document ID")
    clauses: List[ClauseCreate] = Field(default_factory=list)
    risks: List[RiskCreate] = Field(default_factory=list)
    comparisons: Dict[str, ComparisonCreate] = Field(default_factory=dict)
    recommendations: List[RecommendationCreate] = Field(default_factory=list)
    summary: Optional[str] = Field(None, description="Executive summary of the document")


class AnalysisUpdate(BaseModel):
    """Model for updating an analysis."""
    clauses: Optional[List[ClauseCreate]] = None
    risks: Optional[List[RiskCreate]] = None
    comparisons: Optional[Dict[str, ComparisonCreate]] = None
    recommendations: Optional[List[RecommendationCreate]] = None
    summary: Optional[str] = None


class AnalysisSummary(BaseModel):
    """Summary statistics for an analysis."""
    document_id: int
    total_clauses: int = Field(..., description="Total number of clauses detected")
    high_risks: int = Field(..., description="Count of high-risk issues")
    medium_risks: int = Field(..., description="Count of medium-risk issues")
    low_risks: int = Field(..., description="Count of low-risk issues")
    completion_percentage: float = Field(..., description="Analysis completion percentage")
    created_at: datetime


class BatchAnalysisRequest(BaseModel):
    """Request model for batch analysis."""
    document_ids: List[int] = Field(..., description="List of document IDs to analyze")


class BatchAnalysisResponse(BaseModel):
    """Response model for batch analysis."""
    total: int = Field(..., description="Total number of documents in batch")
    processed: int = Field(..., description="Number of documents processed")
    failed: int = Field(..., description="Number of documents that failed processing")
    task_id: Optional[str] = Field(None, description="Task ID for tracking progress")