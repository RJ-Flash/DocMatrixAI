"""
Risk analysis agent for ContractAI.

This module provides an agent for analyzing risks in contracts.
"""

import logging
import json
from typing import Dict, Any, List, Optional, Union

from app.ai.agents.base_agent import BaseAgent
from app.services.cache_service import LLMResponseCache
from app.monitoring.llm_metrics import LLMMetricsTracker

logger = logging.getLogger(__name__)

# Standard risk categories
RISK_CATEGORIES = [
    "Financial",
    "Legal",
    "Operational",
    "Compliance",
    "Reputational",
    "Strategic"
]

# Risk severity levels
RISK_SEVERITY = [
    "Critical",
    "High",
    "Medium",
    "Low",
    "Negligible"
]

class RiskAnalysisAgent(BaseAgent):
    """
    Agent for analyzing risks in contracts.
    
    This agent uses LLMs to identify, assess, and prioritize risks in contract text,
    providing detailed analysis and recommendations for risk mitigation.
    """
    
    def __init__(
        self,
        cache_service: LLMResponseCache,
        metrics_tracker: LLMMetricsTracker,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """
        Initialize the risk analysis agent.
        
        Args:
            cache_service: Cache service for LLM responses
            metrics_tracker: Metrics tracker for LLM usage
            max_retries: Maximum number of retries for LLM calls
            retry_delay: Delay between retries in seconds
        """
        super().__init__(
            agent_name="risk_analysis",
            cache_service=cache_service,
            metrics_tracker=metrics_tracker,
            max_retries=max_retries,
            retry_delay=retry_delay
        )
        
        logger.info("Initialized risk analysis agent")
    
    async def analyze_contract_risks(
        self,
        contract_text: str,
        risk_categories: Optional[List[str]] = None,
        company_perspective: Optional[str] = None,
        industry_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze risks in a contract.
        
        Args:
            contract_text: The contract text to analyze
            risk_categories: Optional list of risk categories to focus on
            company_perspective: Optional company perspective (e.g., "buyer", "seller")
            industry_context: Optional industry context
            
        Returns:
            Dictionary with risk analysis
        """
        # Use default risk categories if none specified
        if not risk_categories:
            risk_categories = self.RISK_CATEGORIES
        
        # Create prompt for risk analysis
        base_prompt = self._create_risk_analysis_prompt(
            contract_text,
            risk_categories,
            company_perspective,
            industry_context
        )
        
        # Format prompt based on provider
        prompt = self._format_prompt_for_provider(base_prompt, self.provider, "json")
        
        # System prompt instructs the LLM on its role and expected output format
        system_prompt = """You are a legal and risk analysis expert specialized in contract review.
Your task is to identify and analyze risks in contract text.
Provide your analysis in a structured JSON format as specified."""
        
        # Call LLM
        response = await self._call_llm(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.0,
            max_tokens=4000,
            operation="analyze_contract_risks"
        )
        
        # Parse response
        return self.parse_llm_json_response(response)
    
    def _create_risk_analysis_prompt(
        self,
        contract_text: str,
        risk_categories: List[str],
        company_perspective: Optional[str],
        industry_context: Optional[str]
    ) -> str:
        """
        Create prompt for risk analysis.
        
        Args:
            contract_text: The contract text to analyze
            risk_categories: List of risk categories to focus on
            company_perspective: Perspective to analyze from
            industry_context: Industry context for risk analysis
            
        Returns:
            Prompt for risk analysis
        """
        risk_categories_str = ", ".join(risk_categories)
        perspective_str = f" from the perspective of a {company_perspective}" if company_perspective else ""
        industry_str = f" in the {industry_context} industry" if industry_context else ""
        
        prompt = f"""Analyze the following contract text and identify risks{perspective_str}{industry_str}.
Focus on the following risk categories: {risk_categories_str}.

For each risk you identify, provide:
1. A clear description of the risk
2. The clause or section where the risk is found
3. The category of risk (from the categories provided)
4. The severity of the risk (Critical, High, Medium, Low, or Negligible)
5. Potential impact if the risk materializes
6. Recommendations for mitigating the risk

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
    "total_risks_identified": 0
  }},
  "risk_analysis": [
    {{
      "risk_id": 1,
      "description": "Clear description of the risk",
      "clause": "The exact text of the clause containing the risk",
      "section": "Section or paragraph number if available",
      "category": "Risk category",
      "severity": "Risk severity",
      "impact": "Potential impact if the risk materializes",
      "probability": "Likelihood of the risk occurring (High, Medium, Low)",
      "mitigation": "Recommendations for mitigating the risk"
    }},
    ...
  ],
  "overall_risk_assessment": {{
    "risk_score": "Overall risk score (1-10)",
    "key_concerns": ["Key concern 1", "Key concern 2", ...],
    "summary": "Brief summary of the overall risk profile of the contract"
  }}
}}"""

        return prompt
    
    async def analyze_clause_risk(
        self,
        clause_text: str,
        clause_type: str,
        company_perspective: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze risks in a specific clause.
        
        Args:
            clause_text: The clause text to analyze
            clause_type: The type of clause
            company_perspective: Optional perspective to analyze from
            
        Returns:
            Dictionary with risk analysis results
        """
        # Create prompt for clause risk analysis
        perspective_str = f" from the perspective of a {company_perspective}" if company_perspective else ""
        
        prompt = f"""Analyze the following {clause_type} clause and identify risks{perspective_str}.

For each risk you identify, provide:
1. A clear description of the risk
2. The category of risk
3. The severity of the risk (Critical, High, Medium, Low, or Negligible)
4. Potential impact if the risk materializes
5. Recommendations for mitigating the risk

Clause Text:
```
{clause_text}
```

Provide your analysis in the following JSON format:
{{
  "clause_type": "{clause_type}",
  "risks": [
    {{
      "description": "Clear description of the risk",
      "category": "Risk category",
      "severity": "Risk severity",
      "impact": "Potential impact if the risk materializes",
      "probability": "Likelihood of the risk occurring (High, Medium, Low)",
      "mitigation": "Recommendations for mitigating the risk"
    }},
    ...
  ],
  "overall_assessment": {{
    "risk_level": "Overall risk level of the clause (High, Medium, Low)",
    "key_concerns": ["Key concern 1", "Key concern 2", ...],
    "summary": "Brief summary of the risks in this clause"
  }},
  "improvement_suggestions": [
    "Suggestion 1 for improving the clause to reduce risk",
    "Suggestion 2 for improving the clause to reduce risk",
    ...
  ]
}}"""
        
        # Call LLM
        system_prompt = f"""You are a legal and risk management expert specialized in contract analysis.
Your task is to identify and analyze risks in a {clause_type} clause.
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
            logger.error(f"Error parsing clause risk analysis response: {str(e)}")
            return {
                "error": "Failed to parse response",
                "raw_response": response["content"]
            }
    
    async def generate_risk_report(
        self,
        contract_text: str,
        company_name: str,
        company_perspective: str,
        industry_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive risk report for a contract.
        
        Args:
            contract_text: The contract text to analyze
            company_name: Name of the company
            company_perspective: Perspective to analyze from
            industry_context: Optional industry context
            
        Returns:
            Dictionary with risk report
        """
        # First, analyze contract risks
        risk_analysis = await self.analyze_contract_risks(
            contract_text=contract_text,
            company_perspective=company_perspective,
            industry_context=industry_context
        )
        
        # Create prompt for risk report
        industry_str = f" in the {industry_context} industry" if industry_context else ""
        
        prompt = f"""Generate a comprehensive risk report for the following contract from the perspective of {company_name} as the {company_perspective}{industry_str}.

Use the following risk analysis as input:
```
{json.dumps(risk_analysis, indent=2)}
```

The report should include:
1. Executive summary
2. Key risk findings
3. Detailed risk analysis by category
4. Risk mitigation recommendations
5. Overall risk assessment and conclusion

Provide your report in the following JSON format:
{{
  "report_metadata": {{
    "company_name": "{company_name}",
    "perspective": "{company_perspective}",
    "industry": "{industry_context or 'Not specified'}",
    "date": "Current date",
    "contract_title": "Title from the contract"
  }},
  "executive_summary": "Brief executive summary of the risk assessment",
  "key_findings": [
    "Key finding 1",
    "Key finding 2",
    ...
  ],
  "risk_analysis_by_category": [
    {{
      "category": "Risk category",
      "risks": [
        {{
          "description": "Risk description",
          "severity": "Risk severity",
          "impact": "Potential impact",
          "mitigation": "Mitigation recommendation"
        }},
        ...
      ],
      "category_assessment": "Assessment of risks in this category"
    }},
    ...
  ],
  "mitigation_recommendations": [
    {{
      "recommendation": "Detailed recommendation",
      "priority": "High/Medium/Low",
      "addressed_risks": ["Risk 1", "Risk 2", ...],
      "implementation_difficulty": "High/Medium/Low"
    }},
    ...
  ],
  "conclusion": {{
    "overall_risk_level": "Overall risk level",
    "recommendation": "Proceed/Proceed with caution/Do not proceed",
    "summary": "Final summary of the risk assessment"
  }}
}}"""
        
        # Call LLM
        system_prompt = """You are a legal and risk management expert specialized in contract analysis.
Your task is to generate a comprehensive risk report based on a detailed risk analysis.
Provide your report in a structured JSON format as specified."""
        
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
            logger.error(f"Error parsing risk report response: {str(e)}")
            return {
                "error": "Failed to parse response",
                "raw_response": response["content"]
            }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and return results.
        
        Args:
            input_data: Input data for processing, should contain:
                - "operation": One of "analyze_contract_risks", "analyze_clause_risk", "generate_risk_report"
                - Operation-specific parameters
            
        Returns:
            Processing results
        """
        operation = input_data.get("operation")
        
        if operation == "analyze_contract_risks":
            return await self.analyze_contract_risks(
                contract_text=input_data.get("contract_text", ""),
                risk_categories=input_data.get("risk_categories"),
                company_perspective=input_data.get("company_perspective"),
                industry_context=input_data.get("industry_context")
            )
        elif operation == "analyze_clause_risk":
            return await self.analyze_clause_risk(
                clause_text=input_data.get("clause_text", ""),
                clause_type=input_data.get("clause_type", ""),
                company_perspective=input_data.get("company_perspective")
            )
        elif operation == "generate_risk_report":
            return await self.generate_risk_report(
                contract_text=input_data.get("contract_text", ""),
                company_name=input_data.get("company_name", ""),
                company_perspective=input_data.get("company_perspective", ""),
                industry_context=input_data.get("industry_context")
            )
        else:
            return {
                "error": f"Unsupported operation: {operation}",
                "supported_operations": ["analyze_contract_risks", "analyze_clause_risk", "generate_risk_report"]
            } 