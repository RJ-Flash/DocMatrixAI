"""
Clause detection agent for ContractAI.

This module provides an agent for detecting and extracting clauses from contracts.
"""

import logging
import json
from typing import Dict, Any, List, Optional, Union

from app.ai.agents.base_agent import BaseAgent
from app.services.cache_service import LLMResponseCache
from app.monitoring.llm_metrics import LLMMetricsTracker

logger = logging.getLogger(__name__)

# Standard clause types to detect
STANDARD_CLAUSE_TYPES = [
    "Indemnification",
    "Limitation of Liability",
    "Confidentiality",
    "Termination",
    "Governing Law",
    "Force Majeure",
    "Intellectual Property",
    "Payment Terms",
    "Warranties",
    "Assignment",
    "Non-Compete",
    "Dispute Resolution",
    "Insurance",
    "Compliance with Laws",
    "Data Protection",
    "Audit Rights"
]

class ClauseDetectionAgent(BaseAgent):
    """
    Agent for detecting and extracting clauses from contracts.
    
    This agent uses LLMs to identify different types of clauses in contract text,
    extract their content, and provide a structured representation of the contract.
    """
    
    def __init__(
        self,
        cache_service: LLMResponseCache,
        metrics_tracker: LLMMetricsTracker,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """
        Initialize the clause detection agent.
        
        Args:
            cache_service: Cache service for LLM responses
            metrics_tracker: Metrics tracker for LLM usage
            max_retries: Maximum number of retries for LLM calls
            retry_delay: Delay between retries in seconds
        """
        super().__init__(
            agent_name="clause_detection",
            cache_service=cache_service,
            metrics_tracker=metrics_tracker,
            max_retries=max_retries,
            retry_delay=retry_delay
        )
        
        logger.info("Initialized clause detection agent")
    
    async def detect_clauses(
        self,
        contract_text: str,
        clause_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Detect clauses in contract text.
        
        Args:
            contract_text: The contract text to analyze
            clause_types: Optional list of clause types to detect
            
        Returns:
            Dictionary with detected clauses
        """
        # Use default clause types if none specified
        if not clause_types:
            clause_types = self.STANDARD_CLAUSE_TYPES
        
        # Create prompt for clause detection
        base_prompt = self._create_clause_detection_prompt(contract_text, clause_types)
        
        # Format prompt based on provider
        prompt = self._format_prompt_for_provider(base_prompt, self.provider, "json")
        
        # System prompt instructs the LLM on its role and expected output format
        system_prompt = """You are a legal expert specialized in contract analysis.
Your task is to identify and extract specific clause types from contract text.
Provide your analysis in a structured JSON format as specified."""
        
        # Call LLM with temperature=0 for deterministic outputs
        response = await self._call_llm(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.0,
            max_tokens=3000,  # Allow enough tokens for comprehensive analysis
            operation="detect_clauses"
        )
        
        # Parse response
        return self.parse_llm_json_response(response)
    
    def _create_clause_detection_prompt(
        self,
        contract_text: str,
        clause_types: List[str],
        detailed: bool = False
    ) -> str:
        """
        Create prompt for clause detection.
        
        Args:
            contract_text: The contract text to analyze
            clause_types: List of clause types to detect
            detailed: Whether to include detailed analysis
            
        Returns:
            Prompt for clause detection
        """
        clause_types_str = ", ".join(clause_types)
        
        prompt = f"""Analyze the following contract text and identify the following types of clauses: {clause_types_str}.

For each clause type that you find, extract the relevant text and provide the following information:
1. The clause type
2. The exact text of the clause
3. The section or paragraph number (if available)

Contract Text:
```
{contract_text}
```

Provide your analysis in the following JSON format:
{{
  "contract_summary": {{
    "title": "Title of the contract",
    "parties": ["Party 1", "Party 2", ...],
    "date": "Contract date if specified",
    "total_clauses_found": 0
  }},
  "clauses": [
    {{
      "type": "Clause type",
      "text": "Exact text of the clause",
      "section": "Section or paragraph number if available",
      "location": "Page number or location information if available"
    }},
    ...
  ],
  "missing_clauses": ["List of clause types that were not found in the contract"]
}}"""

        if detailed:
            prompt += """

For each clause, also provide a detailed analysis including:
1. Key obligations and rights
2. Potential risks or concerns
3. Standard vs. non-standard language assessment

Update the JSON format to include these details:
{
  "contract_summary": {
    "title": "Title of the contract",
    "parties": ["Party 1", "Party 2", ...],
    "date": "Contract date if specified",
    "total_clauses_found": 0
  },
  "clauses": [
    {
      "type": "Clause type",
      "text": "Exact text of the clause",
      "section": "Section or paragraph number if available",
      "location": "Page number or location information if available",
      "analysis": {
        "key_points": ["Key obligation 1", "Key right 1", ...],
        "risks": ["Potential risk 1", "Potential concern 1", ...],
        "standard_assessment": "Assessment of whether the clause uses standard language or contains unusual provisions"
      }
    },
    ...
  ],
  "missing_clauses": ["List of clause types that were not found in the contract"]
}"""

        return prompt
    
    async def extract_clause(
        self,
        contract_text: str,
        clause_type: str
    ) -> Dict[str, Any]:
        """
        Extract a specific clause from contract text.
        
        Args:
            contract_text: The contract text to analyze
            clause_type: The type of clause to extract
            
        Returns:
            Dictionary with extracted clause information
        """
        # Create prompt for clause extraction
        prompt = f"""Extract the {clause_type} clause from the following contract text.
If the clause is found, provide the exact text and any relevant details.
If the clause is not found, indicate that it is missing.

Contract Text:
```
{contract_text}
```

Provide your analysis in the following JSON format:
{{
  "found": true/false,
  "clause_type": "{clause_type}",
  "text": "Exact text of the clause if found",
  "section": "Section or paragraph number if available",
  "analysis": {{
    "key_points": ["Key obligation 1", "Key right 1", ...],
    "risks": ["Potential risk 1", "Potential concern 1", ...],
    "standard_assessment": "Assessment of whether the clause uses standard language or contains unusual provisions"
  }}
}}"""
        
        # Call LLM
        system_prompt = f"""You are a legal expert specialized in contract analysis.
Your task is to extract and analyze the {clause_type} clause from the provided contract text.
Provide your analysis in a structured JSON format as specified."""
        
        response = await self._call_llm(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.0,
            max_tokens=2000
        )
        
        # Parse response
        try:
            # Extract JSON from response
            content = response["content"]
            
            # Find JSON block
            json_start = content.find("{")
            json_end = content.rfind("}")
            
            if json_start >= 0 and json_end >= 0:
                json_str = content[json_start:json_end+1]
                result = json.loads(json_str)
            else:
                # Fallback: try to parse the entire content
                result = json.loads(content)
                
            return result
        except Exception as e:
            logger.error(f"Error parsing clause extraction response: {str(e)}")
            return {
                "error": "Failed to parse response",
                "raw_response": response["content"]
            }
    
    async def compare_clauses(
        self,
        clause1: str,
        clause2: str,
        clause_type: str
    ) -> Dict[str, Any]:
        """
        Compare two clauses of the same type.
        
        Args:
            clause1: First clause text
            clause2: Second clause text
            clause_type: Type of clause being compared
            
        Returns:
            Dictionary with comparison results
        """
        # Create prompt for clause comparison
        prompt = f"""Compare the following two {clause_type} clauses from different contracts.
Identify similarities, differences, and which clause provides better protection or terms.

Clause 1:
```
{clause1}
```

Clause 2:
```
{clause2}
```

Provide your analysis in the following JSON format:
{{
  "clause_type": "{clause_type}",
  "similarities": ["Similarity 1", "Similarity 2", ...],
  "differences": ["Difference 1", "Difference 2", ...],
  "comparison": {{
    "more_favorable": "Clause 1" or "Clause 2" or "Neither",
    "explanation": "Explanation of which clause is more favorable and why",
    "key_advantages": {{
      "clause1": ["Advantage 1", "Advantage 2", ...],
      "clause2": ["Advantage 1", "Advantage 2", ...]
    }},
    "key_disadvantages": {{
      "clause1": ["Disadvantage 1", "Disadvantage 2", ...],
      "clause2": ["Disadvantage 1", "Disadvantage 2", ...]
    }}
  }},
  "recommendation": "Recommendation on which clause to prefer or how to combine the best elements of both"
}}"""
        
        # Call LLM
        system_prompt = f"""You are a legal expert specialized in contract analysis.
Your task is to compare two {clause_type} clauses and provide a detailed analysis of their similarities, differences, and relative strengths.
Provide your analysis in a structured JSON format as specified."""
        
        response = await self._call_llm(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.0,
            max_tokens=2000
        )
        
        # Parse response
        try:
            # Extract JSON from response
            content = response["content"]
            
            # Find JSON block
            json_start = content.find("{")
            json_end = content.rfind("}")
            
            if json_start >= 0 and json_end >= 0:
                json_str = content[json_start:json_end+1]
                result = json.loads(json_str)
            else:
                # Fallback: try to parse the entire content
                result = json.loads(content)
                
            return result
        except Exception as e:
            logger.error(f"Error parsing clause comparison response: {str(e)}")
            return {
                "error": "Failed to parse response",
                "raw_response": response["content"]
            }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and return results.
        
        Args:
            input_data: Input data for processing, should contain:
                - "operation": One of "detect_clauses", "extract_clause", "compare_clauses"
                - Operation-specific parameters
            
        Returns:
            Processing results
        """
        operation = input_data.get("operation")
        
        if operation == "detect_clauses":
            return await self.detect_clauses(
                contract_text=input_data.get("contract_text", ""),
                clause_types=input_data.get("clause_types"),
                detailed=input_data.get("detailed", False)
            )
        elif operation == "extract_clause":
            return await self.extract_clause(
                contract_text=input_data.get("contract_text", ""),
                clause_type=input_data.get("clause_type", "")
            )
        elif operation == "compare_clauses":
            return await self.compare_clauses(
                clause1=input_data.get("clause1", ""),
                clause2=input_data.get("clause2", ""),
                clause_type=input_data.get("clause_type", "")
            )
        else:
            return {
                "error": f"Unsupported operation: {operation}",
                "supported_operations": ["detect_clauses", "extract_clause", "compare_clauses"]
            } 