import logging
import asyncio
from typing import Dict, List, Any, Optional
from app.ai.agents.clause_agent import ClauseDetectionAgent
from app.ai.agents.risk_agent import RiskAnalysisAgent
from app.ai.agents.compare_agent import DocumentComparisonAgent
from app.ai.agents.recommend_agent import RecommendationAgent

logger = logging.getLogger(__name__)


class AnalysisPipeline:
    """
    Orchestrates the document analysis process through multiple AI agents.
    """
    
    def __init__(self):
        """
        Initialize the analysis pipeline with its component agents.
        """
        self.clause_agent = ClauseDetectionAgent()
        self.risk_agent = RiskAnalysisAgent()
        self.compare_agent = DocumentComparisonAgent()
        self.recommend_agent = RecommendationAgent()
    
    async def process_document(self, document_text: str) -> Dict[str, Any]:
        """
        Process a document through the full analysis pipeline.
        
        Args:
            document_text: The text content of the document to analyze
            
        Returns:
            Dictionary containing all analysis results:
            - clauses: List of detected clauses
            - risks: List of identified risks
            - comparisons: Dictionary of clause comparisons
            - recommendations: List of recommendations
            - summary: Document summary
        """
        logger.info("Starting document analysis pipeline")
        
        try:
            # Step 1: Detect clauses
            logger.info("Detecting clauses")
            clauses = await self.clause_agent.detect_clauses(document_text)
            
            # Step 2: Analyze risks
            logger.info("Analyzing risks")
            risks = await self.risk_agent.analyze_risks(clauses)
            
            # Step 3: Compare to standard clauses
            logger.info("Comparing to standard clauses")
            comparisons = await self.compare_agent.compare_clauses(clauses)
            
            # Step 4: Generate recommendations
            logger.info("Generating recommendations")
            recommendations = await self.recommend_agent.generate_recommendations(risks, clauses, comparisons)
            
            # Step 5: Generate summary
            logger.info("Generating document summary")
            summary = await self.generate_summary(document_text, clauses, risks)
            
            logger.info("Document analysis complete")
            
            # Return combined results
            return {
                "clauses": clauses,
                "risks": risks,
                "comparisons": comparisons,
                "recommendations": recommendations,
                "summary": summary
            }
        
        except Exception as e:
            logger.error(f"Error in analysis pipeline: {e}")
            # Re-raise to be handled by the caller
            raise
    
    async def generate_summary(
        self, document_text: str, clauses: List[Dict[str, Any]], risks: List[Dict[str, Any]]
    ) -> str:
        """
        Generate a summary of the document based on detected clauses and risks.
        
        Args:
            document_text: Full document text
            clauses: Detected clauses
            risks: Identified risks
            
        Returns:
            Document summary
        """
        # In a full implementation, this would use a text summarization model
        # For now, we'll generate a simple summary based on the clauses and risks
        
        # Get document length estimate
        word_count = len(document_text.split())
        
        # Count clauses by type
        clause_types = {}
        for clause in clauses:
            clause_type = clause["type"]
            if clause_type in clause_types:
                clause_types[clause_type] += 1
            else:
                clause_types[clause_type] = 1
        
        # Count risks by level
        risk_levels = {"high": 0, "medium": 0, "low": 0}
        for risk in risks:
            level = risk["risk_level"]
            if level in risk_levels:
                risk_levels[level] += 1
        
        # Format the summary
        summary_parts = [
            f"Document analysis summary:",
            f"- Document length: Approximately {word_count} words",
            f"- Detected {len(clauses)} clauses across {len(clause_types)} different types",
        ]
        
        # Add clause types if present
        if clause_types:
            clause_list = ", ".join([f"{count} {type}" for type, count in clause_types.items()])
            summary_parts.append(f"- Clause types: {clause_list}")
        
        # Add risk summary if risks present
        if risks:
            summary_parts.append(
                f"- Identified risks: {risk_levels['high']} high, "
                f"{risk_levels['medium']} medium, and {risk_levels['low']} low priority"
            )
            
            # Add high risk details
            high_risks = [risk for risk in risks if risk["risk_level"] == "high"]
            if high_risks:
                summary_parts.append("- High priority risks include:")
                for risk in high_risks[:3]:  # Limit to top 3
                    summary_parts.append(f"  * {risk['risk_type']} in {risk['clause_type']} clause")
        else:
            summary_parts.append("- No significant risks identified")
        
        return "\n".join(summary_parts)