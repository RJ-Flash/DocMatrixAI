"""
Recommendation agent for ContractAI.

This module provides an agent for generating recommendations based on contract analysis.
"""

import logging
import json
from typing import Dict, Any, List, Optional, Union

from app.ai.agents.base_agent import BaseAgent
from app.services.cache_service import LLMResponseCache
from app.monitoring.llm_metrics import LLMMetricsTracker

logger = logging.getLogger(__name__)

class RecommendationAgent(BaseAgent):
    """
    Agent for generating recommendations based on contract analysis.
    
    This agent uses LLMs to generate recommendations for contract improvements,
    negotiation strategies, and alternative language based on analysis of contract text.
    """
    
    def __init__(
        self,
        cache_service: LLMResponseCache,
        metrics_tracker: LLMMetricsTracker,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """
        Initialize the recommendation agent.
        
        Args:
            cache_service: Cache service for LLM responses
            metrics_tracker: Metrics tracker for LLM usage
            max_retries: Maximum number of retries for LLM calls
            retry_delay: Delay between retries in seconds
        """
        super().__init__(
            agent_name="recommendation",
            cache_service=cache_service,
            metrics_tracker=metrics_tracker,
            max_retries=max_retries,
            retry_delay=retry_delay
        )
        
        logger.info("Initialized recommendation agent")
    
    async def generate_clause_recommendations(
        self,
        clause_text: str,
        clause_type: str,
        company_perspective: str,
        risk_analysis: Optional[Dict[str, Any]] = None,
        industry_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate recommendations for improving a specific clause.
        
        Args:
            clause_text: The clause text to analyze
            clause_type: The type of clause
            company_perspective: Perspective to analyze from (e.g., "buyer", "seller")
            risk_analysis: Optional risk analysis results for the clause
            industry_context: Optional industry context
            
        Returns:
            Dictionary with clause recommendations
        """
        # Create prompt for clause recommendations
        base_prompt = self._create_clause_recommendation_prompt(
            clause_text,
            clause_type,
            company_perspective,
            risk_analysis,
            industry_context
        )
        
        # Format prompt based on provider
        prompt = self._format_prompt_for_provider(base_prompt, self.provider, "json")
        
        # Call LLM
        system_prompt = """You are a legal expert specialized in contract analysis and drafting.
Your task is to provide recommendations for improving a contract clause.
Provide your recommendations in a structured JSON format as specified."""
        
        response = await self._call_llm(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.0,
            max_tokens=3000,
            operation="generate_clause_recommendations"
        )
        
        # Parse response
        return self.parse_llm_json_response(response)
    
    def _create_clause_recommendation_prompt(
        self,
        clause_text: str,
        clause_type: str,
        company_perspective: str,
        risk_analysis: Optional[Dict[str, Any]],
        industry_context: Optional[str]
    ) -> str:
        """
        Create prompt for clause recommendations.
        
        Args:
            clause_text: The clause text to analyze
            clause_type: The type of clause
            company_perspective: Perspective to analyze from
            risk_analysis: Optional risk analysis results
            industry_context: Optional industry context
            
        Returns:
            Prompt for clause recommendations
        """
        industry_str = f" in the {industry_context} industry" if industry_context else ""
        risk_analysis_str = ""
        
        if risk_analysis:
            risk_analysis_str = f"""
Consider the following risk analysis when making your recommendations:
```
{json.dumps(risk_analysis, indent=2)}
```
"""
        
        prompt = f"""Generate recommendations for improving the following {clause_type} clause from the perspective of a {company_perspective}{industry_str}.

Clause Text:
```
{clause_text}
```
{risk_analysis_str}
Provide recommendations for:
1. Improving the clause to better protect the {company_perspective}'s interests
2. Alternative language that would be more favorable
3. Negotiation strategies for this clause
4. Common industry standards for this type of clause

Provide your recommendations in the following JSON format:
{{
  "clause_type": "{clause_type}",
  "perspective": "{company_perspective}",
  "original_text": "{clause_text}",
  "improvement_recommendations": [
    {{
      "recommendation": "Specific recommendation for improvement",
      "rationale": "Explanation of why this improvement is recommended",
      "priority": "High/Medium/Low"
    }},
    ...
  ],
  "alternative_language": [
    {{
      "text": "Suggested alternative language",
      "benefits": ["Benefit 1", "Benefit 2", ...],
      "potential_pushback": "Potential objections from the other party"
    }},
    ...
  ],
  "negotiation_strategies": [
    {{
      "strategy": "Negotiation strategy",
      "talking_points": ["Talking point 1", "Talking point 2", ...],
      "fallback_positions": ["Fallback position 1", "Fallback position 2", ...]
    }},
    ...
  ],
  "industry_standards": {{
    "common_practices": ["Common practice 1", "Common practice 2", ...],
    "benchmark_language": "Example of standard language in the industry",
    "trends": ["Industry trend 1", "Industry trend 2", ...]
  }}
}}"""

        return prompt
    
    async def generate_negotiation_strategy(
        self,
        contract_text: str,
        company_name: str,
        company_perspective: str,
        priority_issues: List[str],
        counterparty_info: Optional[Dict[str, Any]] = None,
        industry_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a negotiation strategy for a contract.
        
        Args:
            contract_text: The contract text to analyze
            company_name: Name of the company
            company_perspective: Perspective to analyze from
            priority_issues: List of priority issues for negotiation
            counterparty_info: Optional information about the counterparty
            industry_context: Optional industry context
            
        Returns:
            Dictionary with negotiation strategy
        """
        # Create prompt for negotiation strategy
        base_prompt = self._create_negotiation_strategy_prompt(
            contract_text,
            company_name,
            company_perspective,
            priority_issues,
            counterparty_info,
            industry_context
        )
        
        # Format prompt based on provider
        prompt = self._format_prompt_for_provider(base_prompt, self.provider, "json")
        
        # Call LLM
        system_prompt = """You are a legal and business expert specialized in contract negotiation.
Your task is to provide a comprehensive negotiation strategy for a contract.
Provide your strategy in a structured JSON format as specified."""
        
        response = await self._call_llm(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.0,
            max_tokens=4000,
            operation="generate_negotiation_strategy"
        )
        
        # Parse response
        return self.parse_llm_json_response(response)
    
    def _create_negotiation_strategy_prompt(
        self,
        contract_text: str,
        company_name: str,
        company_perspective: str,
        priority_issues: List[str],
        counterparty_info: Optional[Dict[str, Any]],
        industry_context: Optional[str]
    ) -> str:
        """
        Create prompt for negotiation strategy.
        
        Args:
            contract_text: The contract text to analyze
            company_name: Name of the company
            company_perspective: Perspective to analyze from
            priority_issues: List of priority issues for negotiation
            counterparty_info: Optional information about the counterparty
            industry_context: Optional industry context
            
        Returns:
            Prompt for negotiation strategy
        """
        industry_str = f" in the {industry_context} industry" if industry_context else ""
        priority_issues_str = ", ".join(priority_issues)
        counterparty_str = ""
        
        if counterparty_info:
            counterparty_str = f"""
Consider the following information about the counterparty:
```
{json.dumps(counterparty_info, indent=2)}
```
"""
        
        prompt = f"""Generate a comprehensive negotiation strategy for {company_name} as the {company_perspective} for the following contract{industry_str}.
The priority issues for negotiation are: {priority_issues_str}.
{counterparty_str}
Contract Text:
```
{contract_text}
```

Provide a negotiation strategy that includes:
1. Overall approach and key objectives
2. Specific strategies for each priority issue
3. Potential concessions and trade-offs
4. Fallback positions
5. Recommended negotiation tactics

Provide your strategy in the following JSON format:
{{
  "strategy_summary": {{
    "company_name": "{company_name}",
    "perspective": "{company_perspective}",
    "key_objectives": ["Objective 1", "Objective 2", ...],
    "overall_approach": "Description of the overall negotiation approach"
  }},
  "priority_issues": [
    {{
      "issue": "Priority issue",
      "current_position": "Current position in the contract",
      "desired_outcome": "Desired outcome",
      "strategy": "Specific strategy for this issue",
      "talking_points": ["Talking point 1", "Talking point 2", ...],
      "potential_concessions": ["Concession 1", "Concession 2", ...],
      "fallback_positions": ["Fallback position 1", "Fallback position 2", ...]
    }},
    ...
  ],
  "negotiation_tactics": [
    {{
      "tactic": "Negotiation tactic",
      "when_to_use": "When to use this tactic",
      "expected_outcome": "Expected outcome"
    }},
    ...
  ],
  "overall_recommendations": [
    "Recommendation 1",
    "Recommendation 2",
    ...
  ]
}}"""

        return prompt
    
    async def generate_alternative_clauses(
        self,
        clause_text: str,
        clause_type: str,
        company_perspective: str,
        improvement_goals: List[str],
        industry_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate alternative clauses.
        
        Args:
            clause_text: The original clause text
            clause_type: The type of clause
            company_perspective: Perspective to analyze from
            improvement_goals: List of goals for improvement
            industry_context: Optional industry context
            
        Returns:
            Dictionary with alternative clauses
        """
        # Create prompt for alternative clauses
        base_prompt = self._create_alternative_clauses_prompt(
            clause_text,
            clause_type,
            company_perspective,
            improvement_goals,
            industry_context
        )
        
        # Format prompt based on provider
        prompt = self._format_prompt_for_provider(base_prompt, self.provider, "json")
        
        # Call LLM
        system_prompt = """You are a legal expert specialized in contract drafting.
Your task is to generate alternative clauses that better serve the client's interests.
Provide your alternatives in a structured JSON format as specified."""
        
        response = await self._call_llm(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.0,
            max_tokens=3000,
            operation="generate_alternative_clauses"
        )
        
        # Parse response
        return self.parse_llm_json_response(response)
    
    def _create_alternative_clauses_prompt(
        self,
        clause_text: str,
        clause_type: str,
        company_perspective: str,
        improvement_goals: List[str],
        industry_context: Optional[str]
    ) -> str:
        """
        Create prompt for alternative clauses.
        
        Args:
            clause_text: The original clause text
            clause_type: The type of clause
            company_perspective: Perspective to analyze from
            improvement_goals: List of goals for improvement
            industry_context: Optional industry context
            
        Returns:
            Prompt for alternative clauses
        """
        industry_str = f" in the {industry_context} industry" if industry_context else ""
        improvement_goals_str = ", ".join(improvement_goals)
        
        prompt = f"""Generate alternative {clause_type} clauses that would better serve a {company_perspective}{industry_str}.
The goals for improvement are: {improvement_goals_str}.

Original Clause:
```
{clause_text}
```

Generate three alternative versions of this clause:
1. A minimally modified version with small improvements
2. A moderately modified version with significant improvements
3. An ideal version that fully addresses all improvement goals

For each alternative, provide:
1. The full text of the alternative clause
2. An explanation of the changes made
3. The benefits of the alternative
4. Potential objections from the counterparty

Provide your alternatives in the following JSON format:
{{
  "original_clause": {{
    "text": "{clause_text}",
    "type": "{clause_type}",
    "perspective": "{company_perspective}",
    "improvement_goals": [{', '.join([f'"{goal}"' for goal in improvement_goals])}]
  }},
  "alternatives": [
    {{
      "version": "Minimal",
      "text": "Full text of the minimally modified clause",
      "changes": ["Change 1", "Change 2", ...],
      "benefits": ["Benefit 1", "Benefit 2", ...],
      "potential_objections": ["Objection 1", "Objection 2", ...]
    }},
    {{
      "version": "Moderate",
      "text": "Full text of the moderately modified clause",
      "changes": ["Change 1", "Change 2", ...],
      "benefits": ["Benefit 1", "Benefit 2", ...],
      "potential_objections": ["Objection 1", "Objection 2", ...]
    }},
    {{
      "version": "Ideal",
      "text": "Full text of the ideal clause",
      "changes": ["Change 1", "Change 2", ...],
      "benefits": ["Benefit 1", "Benefit 2", ...],
      "potential_objections": ["Objection 1", "Objection 2", ...]
    }}
  ],
  "recommendation": "Recommendation on which alternative to use and why"
}}"""

        return prompt
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and return results.
        
        Args:
            input_data: Input data for processing, should contain:
                - "operation": One of "generate_clause_recommendations", "generate_negotiation_strategy", "generate_alternative_clauses"
                - Operation-specific parameters
            
        Returns:
            Processing results
        """
        operation = input_data.get("operation")
        
        if operation == "generate_clause_recommendations":
            return await self.generate_clause_recommendations(
                clause_text=input_data.get("clause_text", ""),
                clause_type=input_data.get("clause_type", ""),
                company_perspective=input_data.get("company_perspective", ""),
                risk_analysis=input_data.get("risk_analysis"),
                industry_context=input_data.get("industry_context")
            )
        elif operation == "generate_negotiation_strategy":
            return await self.generate_negotiation_strategy(
                contract_text=input_data.get("contract_text", ""),
                company_name=input_data.get("company_name", ""),
                company_perspective=input_data.get("company_perspective", ""),
                priority_issues=input_data.get("priority_issues", []),
                counterparty_info=input_data.get("counterparty_info"),
                industry_context=input_data.get("industry_context")
            )
        elif operation == "generate_alternative_clauses":
            return await self.generate_alternative_clauses(
                clause_text=input_data.get("clause_text", ""),
                clause_type=input_data.get("clause_type", ""),
                company_perspective=input_data.get("company_perspective", ""),
                improvement_goals=input_data.get("improvement_goals", []),
                industry_context=input_data.get("industry_context")
            )
        else:
            return {
                "error": f"Unsupported operation: {operation}",
                "supported_operations": ["generate_clause_recommendations", "generate_negotiation_strategy", "generate_alternative_clauses"]
            } 