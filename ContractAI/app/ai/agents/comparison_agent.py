"""
Document comparison agent for ContractAI.

This module provides an agent for comparing contract documents.
"""

import logging
import json
from typing import Dict, Any, List, Optional, Union

from app.ai.agents.base_agent import BaseAgent
from app.services.cache_service import LLMResponseCache
from app.monitoring.llm_metrics import LLMMetricsTracker

logger = logging.getLogger(__name__)

class DocumentComparisonAgent(BaseAgent):
    """
    Agent for comparing contract documents.
    
    This agent uses LLMs to compare different versions of contracts,
    identify changes, and analyze their significance.
    """
    
    def __init__(
        self,
        cache_service: LLMResponseCache,
        metrics_tracker: LLMMetricsTracker,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """
        Initialize the document comparison agent.
        
        Args:
            cache_service: Cache service for LLM responses
            metrics_tracker: Metrics tracker for LLM usage
            max_retries: Maximum number of retries for LLM calls
            retry_delay: Delay between retries in seconds
        """
        super().__init__(
            agent_name="document_comparison",
            cache_service=cache_service,
            metrics_tracker=metrics_tracker,
            max_retries=max_retries,
            retry_delay=retry_delay
        )
        
        logger.info("Initialized document comparison agent")
    
    async def compare_documents(
        self,
        document1_text: str,
        document2_text: str,
        focus_areas: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Compare two contract documents.
        
        Args:
            document1_text: Text of the first document
            document2_text: Text of the second document
            focus_areas: Optional list of areas to focus on in the comparison
            
        Returns:
            Dictionary with comparison results
        """
        # Create prompt for document comparison
        base_prompt = self._create_document_comparison_prompt(
            document1_text,
            document2_text,
            focus_areas
        )
        
        # Format prompt based on provider
        prompt = self._format_prompt_for_provider(base_prompt, self.provider, "json")
        
        # System prompt instructs the LLM on its role and expected output format
        system_prompt = """You are a legal expert specialized in contract comparison.
Your task is to compare two contract documents and identify key differences.
Provide your analysis in a structured JSON format as specified."""
        
        # Call LLM
        response = await self._call_llm(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.0,
            max_tokens=4000,
            operation="compare_documents"
        )
        
        # Parse response
        return self.parse_llm_json_response(response)
    
    def _create_document_comparison_prompt(
        self,
        document1_text: str,
        document2_text: str,
        focus_areas: Optional[List[str]]
    ) -> str:
        """
        Create prompt for document comparison.
        
        Args:
            document1_text: Text of the first document
            document2_text: Text of the second document
            focus_areas: Optional list of areas to focus on
            
        Returns:
            Prompt for document comparison
        """
        focus_areas_str = ""
        if focus_areas:
            focus_areas_str = f"Focus particularly on the following areas: {', '.join(focus_areas)}."
        
        prompt = f"""Compare the following two contract documents and identify key differences.
{focus_areas_str}

{document1_name}:
```
{document1_text}
```

{document2_name}:
```
{document2_text}
```

For each significant difference you identify, provide:
1. The section or clause where the difference occurs
2. The text from {document1_name}
3. The text from {document2_name}
4. An analysis of the significance of the change
5. Which version is more favorable (if applicable)

Provide your analysis in the following JSON format:
{{
  "document_summary": {{
    "document1_name": "{document1_name}",
    "document2_name": "{document2_name}",
    "total_differences": 0
  }},
  "key_differences": [
    {{
      "section": "Section or clause name",
      "document1_text": "Text from {document1_name}",
      "document2_text": "Text from {document2_name}",
      "analysis": "Analysis of the significance of the change",
      "more_favorable": "{document1_name}" or "{document2_name}" or "Neither"
    }},
    ...
  ],
  "added_sections": [
    {{
      "section": "Section added in {document2_name}",
      "text": "Text of the added section",
      "analysis": "Analysis of the significance of the addition"
    }},
    ...
  ],
  "removed_sections": [
    {{
      "section": "Section removed from {document1_name}",
      "text": "Text of the removed section",
      "analysis": "Analysis of the significance of the removal"
    }},
    ...
  ],
  "overall_assessment": {{
    "summary": "Overall summary of the differences",
    "recommendation": "Recommendation based on the comparison"
  }}
}}"""

        return prompt
    
    async def compare_versions(
        self,
        versions: List[Dict[str, str]],
        focus_areas: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Compare multiple versions of a contract.
        
        Args:
            versions: List of dictionaries with 'name' and 'text' keys
            focus_areas: Optional list of areas to focus on
            
        Returns:
            Dictionary with version comparison results
        """
        if len(versions) < 2:
            return {
                "error": "At least two versions are required for comparison"
            }
            
        # Create prompt for version comparison
        prompt = self._create_version_comparison_prompt(versions, focus_areas)
        
        # Call LLM
        system_prompt = """You are a legal expert specialized in contract analysis.
Your task is to compare multiple versions of a contract and track changes across versions.
Provide your analysis in a structured JSON format as specified."""
        
        response = await self._call_llm(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.0,
            max_tokens=4000
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
            logger.error(f"Error parsing version comparison response: {str(e)}")
            return {
                "error": "Failed to parse response",
                "raw_response": response["content"]
            }
    
    def _create_version_comparison_prompt(
        self,
        versions: List[Dict[str, str]],
        focus_areas: Optional[List[str]]
    ) -> str:
        """
        Create prompt for version comparison.
        
        Args:
            versions: List of dictionaries with 'name' and 'text' keys
            focus_areas: Optional list of areas to focus on
            
        Returns:
            Prompt for version comparison
        """
        focus_areas_str = ""
        if focus_areas:
            focus_areas_str = f"Focus particularly on the following areas: {', '.join(focus_areas)}."
        
        versions_text = ""
        for i, version in enumerate(versions):
            versions_text += f"\nVersion {i+1} ({version['name']}):\n```\n{version['text']}\n```\n"
        
        prompt = f"""Compare the following versions of a contract and track changes across versions.
{focus_areas_str}

{versions_text}

For each significant change between versions, provide:
1. The version where the change was introduced
2. The section or clause that changed
3. The nature of the change (addition, removal, modification)
4. An analysis of the significance of the change

Provide your analysis in the following JSON format:
{{
  "version_summary": {{
    "total_versions": {len(versions)},
    "version_names": [{', '.join([f'"{v["name"]}"' for v in versions])}],
    "total_changes": 0
  }},
  "changes_by_version": [
    {{
      "from_version": "Previous version name",
      "to_version": "Current version name",
      "changes": [
        {{
          "section": "Section or clause name",
          "change_type": "Addition" or "Removal" or "Modification",
          "previous_text": "Text in previous version (if applicable)",
          "current_text": "Text in current version (if applicable)",
          "analysis": "Analysis of the significance of the change"
        }},
        ...
      ]
    }},
    ...
  ],
  "evolution_by_section": [
    {{
      "section": "Section or clause name",
      "versions": [
        {{
          "version": "Version name",
          "text": "Text in this version",
          "changes_from_previous": "Description of changes from previous version"
        }},
        ...
      ],
      "analysis": "Analysis of how this section evolved across versions"
    }},
    ...
  ],
  "overall_assessment": {{
    "summary": "Overall summary of the evolution across versions",
    "key_trends": ["Trend 1", "Trend 2", ...],
    "recommendation": "Recommendation based on the version history"
  }}
}}"""

        return prompt
    
    async def find_similar_clauses(
        self,
        target_clause: str,
        document_text: str,
        clause_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Find clauses in a document similar to a target clause.
        
        Args:
            target_clause: The target clause to find similar clauses for
            document_text: The document text to search in
            clause_type: Optional type of clause to focus on
            
        Returns:
            Dictionary with similar clauses
        """
        # Create prompt for finding similar clauses
        clause_type_str = f" of type {clause_type}" if clause_type else ""
        
        prompt = f"""Find clauses in the document that are similar to the target clause{clause_type_str}.

Target Clause:
```
{target_clause}
```

Document:
```
{document_text}
```

For each similar clause you find, provide:
1. The text of the similar clause
2. The section or location in the document
3. A similarity score (0-100)
4. An analysis of the similarities and differences

Provide your analysis in the following JSON format:
{{
  "target_clause": {{
    "text": "{target_clause}",
    "type": "{clause_type or 'Not specified'}"
  }},
  "similar_clauses": [
    {{
      "text": "Text of the similar clause",
      "section": "Section or location in the document",
      "similarity_score": 85,
      "similarities": ["Similarity 1", "Similarity 2", ...],
      "differences": ["Difference 1", "Difference 2", ...]
    }},
    ...
  ],
  "best_match": {{
    "text": "Text of the best matching clause",
    "section": "Section or location in the document",
    "similarity_score": 92,
    "analysis": "Analysis of why this is the best match"
  }}
}}"""
        
        # Call LLM
        system_prompt = """You are a legal expert specialized in contract analysis.
Your task is to find clauses in a document that are similar to a target clause.
Provide your analysis in a structured JSON format as specified."""
        
        response = await self._call_llm(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.0,
            max_tokens=3000
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
            logger.error(f"Error parsing similar clauses response: {str(e)}")
            return {
                "error": "Failed to parse response",
                "raw_response": response["content"]
            }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and return results.
        
        Args:
            input_data: Input data for processing, should contain:
                - "operation": One of "compare_documents", "compare_versions", "find_similar_clauses"
                - Operation-specific parameters
            
        Returns:
            Processing results
        """
        operation = input_data.get("operation")
        
        if operation == "compare_documents":
            return await self.compare_documents(
                document1_text=input_data.get("document1_text", ""),
                document2_text=input_data.get("document2_text", ""),
                focus_areas=input_data.get("focus_areas")
            )
        elif operation == "compare_versions":
            return await self.compare_versions(
                versions=input_data.get("versions", []),
                focus_areas=input_data.get("focus_areas")
            )
        elif operation == "find_similar_clauses":
            return await self.find_similar_clauses(
                target_clause=input_data.get("target_clause", ""),
                document_text=input_data.get("document_text", ""),
                clause_type=input_data.get("clause_type")
            )
        else:
            return {
                "error": f"Unsupported operation: {operation}",
                "supported_operations": ["compare_documents", "compare_versions", "find_similar_clauses"]
            } 