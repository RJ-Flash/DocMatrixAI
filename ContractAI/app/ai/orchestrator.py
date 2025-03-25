import logging
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import numpy as np

from app.ai.agents.clause_agent import ClauseDetectionAgent
from app.ai.agents.risk_agent import RiskAnalysisAgent
from app.ai.agents.comparison_agent import ComparisonAgent
from app.ai.agents.recommendation_agent import RecommendationAgent
from app.services.service_factory import ServiceFactory
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


@dataclass
class DocumentSection:
    """Represents a section of a document for parallel processing."""
    text: str
    start_char: int
    end_char: int
    section_type: Optional[str] = None


class DocumentChunker:
    """Splits documents into semantic sections for parallel processing."""
    
    def __init__(self, max_section_length: int = 5000, overlap: int = 500):
        """
        Initialize the document chunker.
        
        Args:
            max_section_length: Maximum length of each section
            overlap: Number of characters to overlap between sections
        """
        self.max_section_length = max_section_length
        self.overlap = overlap
    
    def split_by_semantic_sections(self, text: str) -> List[DocumentSection]:
        """
        Split document into semantic sections.
        
        Args:
            text: Document text to split
            
        Returns:
            List of document sections
        """
        sections = []
        current_pos = 0
        
        while current_pos < len(text):
            # Calculate end position for this section
            end_pos = min(current_pos + self.max_section_length, len(text))
            
            # If not at end of document, find a good break point
            if end_pos < len(text):
                # Look for paragraph break
                break_pos = text.rfind('\n\n', current_pos, end_pos)
                if break_pos == -1:
                    # Look for sentence break
                    break_pos = text.rfind('. ', current_pos, end_pos)
                if break_pos == -1:
                    # Fall back to word break
                    break_pos = text.rfind(' ', current_pos, end_pos)
                if break_pos != -1:
                    end_pos = break_pos
            
            # Create section
            section = DocumentSection(
                text=text[current_pos:end_pos],
                start_char=current_pos,
                end_char=end_pos
            )
            sections.append(section)
            
            # Move position for next section, including overlap
            current_pos = max(current_pos, end_pos - self.overlap)
        
        return sections


class ClauseMerger:
    """Merges clause detection results from different sections."""
    
    def merge_with_context(
        self,
        section_results: List[List[Dict[str, Any]]],
        sections: List[DocumentSection]
    ) -> List[Dict[str, Any]]:
        """
        Merge clause detection results from different sections.
        
        Args:
            section_results: List of clause detection results from each section
            sections: List of document sections
            
        Returns:
            Merged list of clauses with preserved context
        """
        # Flatten all clauses
        all_clauses = []
        for section_idx, clauses in enumerate(section_results):
            section = sections[section_idx]
            for clause in clauses:
                # Adjust positions to account for section offsets
                if "position" in clause:
                    clause["position"]["start_char"] += section.start_char
                    clause["position"]["end_char"] += section.start_char
                all_clauses.append(clause)
        
        # Sort by position
        all_clauses.sort(key=lambda x: x["position"]["start_char"])
        
        # Deduplicate overlapping clauses
        merged_clauses = []
        for clause in all_clauses:
            # Skip if this clause overlaps significantly with the previous one
            if merged_clauses and self._clauses_overlap(merged_clauses[-1], clause):
                # Keep the one with higher confidence
                if clause["confidence"] > merged_clauses[-1]["confidence"]:
                    merged_clauses[-1] = clause
            else:
                merged_clauses.append(clause)
        
        return merged_clauses
    
    def _clauses_overlap(
        self,
        clause1: Dict[str, Any],
        clause2: Dict[str, Any],
        overlap_threshold: float = 0.5
    ) -> bool:
        """
        Check if two clauses overlap significantly.
        
        Args:
            clause1: First clause
            clause2: Second clause
            overlap_threshold: Minimum overlap ratio to consider clauses as overlapping
            
        Returns:
            True if clauses overlap significantly
        """
        pos1 = clause1["position"]
        pos2 = clause2["position"]
        
        # Calculate overlap
        overlap_start = max(pos1["start_char"], pos2["start_char"])
        overlap_end = min(pos1["end_char"], pos2["end_char"])
        overlap_length = max(0, overlap_end - overlap_start)
        
        # Calculate overlap ratios
        length1 = pos1["end_char"] - pos1["start_char"]
        length2 = pos2["end_char"] - pos2["start_char"]
        
        overlap_ratio1 = overlap_length / length1
        overlap_ratio2 = overlap_length / length2
        
        return max(overlap_ratio1, overlap_ratio2) > overlap_threshold


class AgentOrchestrator:
    """Coordinates AI agents for document analysis."""
    
    def __init__(self):
        """Initialize the agent orchestrator."""
        # Initialize components
        self.chunker = DocumentChunker()
        self.merger = ClauseMerger()
        
        # Agent placeholders - will be initialized in initialize() method
        self.clause_agent = None
        self.risk_agent = None
        self.comparison_agent = None
        self.recommendation_agent = None
        self.initialized = False
        
        logger.info("Created AgentOrchestrator instance")
    
    async def initialize(self):
        """Initialize agents asynchronously using ServiceFactory."""
        if self.initialized:
            return
            
        try:
            # Initialize agents using service factory
            self.clause_agent = await ServiceFactory.get_clause_detection_agent()
            self.risk_agent = await ServiceFactory.get_risk_analysis_agent()
            self.comparison_agent = await ServiceFactory.get_document_comparison_agent()
            self.recommendation_agent = await ServiceFactory.get_recommendation_agent()
            
            self.initialized = True
            logger.info("Initialized AgentOrchestrator with all components")
            
        except Exception as e:
            logger.error(f"Error initializing AgentOrchestrator: {e}")
            raise
    
    async def process_document(self, document_text: str) -> Dict[str, Any]:
        """
        Process a document using parallel agent coordination.
        
        Args:
            document_text: Text content of the document
            
        Returns:
            Analysis results including clauses, risks, comparisons, and recommendations
        """
        logger.info("Starting parallel document processing")
        
        # Ensure agents are initialized
        if not self.initialized:
            await self.initialize()
        
        try:
            # Split document into sections
            sections = self.chunker.split_by_semantic_sections(document_text)
            logger.info(f"Split document into {len(sections)} sections")
            
            # Process sections in parallel with clause detection
            clause_tasks = [
                self.clause_agent.detect_clauses(section.text)
                for section in sections
            ]
            section_results = await asyncio.gather(*clause_tasks)
            
            # Merge clause results
            clauses = self.merger.merge_with_context(section_results, sections)
            logger.info(f"Detected and merged {len(clauses)} clauses")
            
            # Process risks and comparisons in parallel
            risk_task = self.risk_agent.analyze_risks(clauses)
            comparison_task = self.comparison_agent.compare_clauses(clauses)
            
            risks, comparisons = await asyncio.gather(risk_task, comparison_task)
            logger.info(f"Analyzed {len(risks)} risks and {len(comparisons)} comparisons")
            
            # Generate recommendations
            recommendations = await self.recommendation_agent.generate_recommendations(
                risks, comparisons
            )
            logger.info(f"Generated {len(recommendations)} recommendations")
            
            # Prepare analysis results
            results = {
                "clauses": clauses,
                "risks": risks,
                "comparisons": comparisons,
                "recommendations": recommendations,
                "summary": self._generate_summary(clauses, risks, recommendations)
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Error in parallel document processing: {e}")
            raise
    
    def _generate_summary(
        self,
        clauses: List[Dict[str, Any]],
        risks: List[Dict[str, Any]],
        recommendations: List[Dict[str, Any]]
    ) -> str:
        """
        Generate an executive summary of the analysis.
        
        Args:
            clauses: Detected clauses
            risks: Identified risks
            recommendations: Generated recommendations
            
        Returns:
            Executive summary text
        """
        # Count clauses by type
        clause_types = {}
        for clause in clauses:
            clause_type = clause["type"]
            clause_types[clause_type] = clause_types.get(clause_type, 0) + 1
        
        # Count risks by level
        risk_levels = {"high": 0, "medium": 0, "low": 0}
        for risk in risks:
            level = risk["risk_level"]
            risk_levels[level] = risk_levels.get(level, 0) + 1
        
        # Format summary
        summary = [
            "Document Analysis Summary:",
            f"- Analyzed {len(clauses)} clauses across {len(clause_types)} categories",
            f"- Identified {len(risks)} risks:",
            f"  • {risk_levels['high']} high-risk issues",
            f"  • {risk_levels['medium']} medium-risk issues",
            f"  • {risk_levels['low']} low-risk issues",
            f"- Generated {len(recommendations)} recommendations for improvement"
        ]
        
        # Add high-priority recommendations
        high_priority = [r for r in recommendations if r["priority"] == "high"]
        if high_priority:
            summary.append("\nKey Recommendations:")
            for rec in high_priority[:3]:  # Top 3 high-priority recommendations
                summary.append(f"- {rec['suggested_action']}")
        
        return "\n".join(summary) 