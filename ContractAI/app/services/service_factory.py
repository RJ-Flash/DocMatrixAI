"""
Service factory for ContractAI.
"""

import logging
from typing import Dict, Any, Optional

from app.services.redis_service import RedisService
from app.services.cache_service import LLMResponseCache
from app.monitoring.llm_metrics import LLMMetricsTracker
from app.ai.llm_config import initialize_llm_settings
from app.ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class ServiceFactory:
    """Factory for creating and managing service instances."""
    
    _cache_service: Optional[LLMResponseCache] = None
    _metrics_tracker: Optional[LLMMetricsTracker] = None
    _initialized: bool = False
    
    @classmethod
    async def initialize(cls) -> None:
        """Initialize all services."""
        if cls._initialized:
            return
            
        # Initialize LLM settings
        llm_settings, agent_llm_settings = initialize_llm_settings()
        
        # Initialize LLM factory
        LLMFactory.initialize(llm_settings, agent_llm_settings)
        
        # Mark as initialized
        cls._initialized = True
        logger.info("ServiceFactory initialized")
    
    @classmethod
    async def get_cache_service(cls) -> LLMResponseCache:
        """
        Get the LLM response cache service.
        
        Returns:
            LLM response cache service
        """
        if not cls._initialized:
            await cls.initialize()
            
        if cls._cache_service is None:
            redis = await RedisService.get_redis()
            cls._cache_service = LLMResponseCache(redis)
            logger.info("Initialized LLM response cache service")
            
        return cls._cache_service
    
    @classmethod
    async def get_metrics_tracker(cls) -> LLMMetricsTracker:
        """
        Get the LLM metrics tracker.
        
        Returns:
            LLM metrics tracker
        """
        if not cls._initialized:
            await cls.initialize()
            
        if cls._metrics_tracker is None:
            redis = await RedisService.get_redis()
            cls._metrics_tracker = LLMMetricsTracker(redis)
            logger.info("Initialized LLM metrics tracker")
            
        return cls._metrics_tracker
    
    @classmethod
    async def get_clause_detection_agent(cls):
        """
        Get a clause detection agent instance.
        
        Returns:
            Clause detection agent
        """
        if not cls._initialized:
            await cls.initialize()
            
        from app.ai.agents.clause_agent import ClauseDetectionAgent
        
        cache_service = await cls.get_cache_service()
        metrics_tracker = await cls.get_metrics_tracker()
        
        agent = ClauseDetectionAgent(
            cache_service=cache_service,
            metrics_tracker=metrics_tracker
        )
        await agent.initialize()
        
        return agent
    
    @classmethod
    async def get_risk_analysis_agent(cls):
        """
        Get a risk analysis agent instance.
        
        Returns:
            Risk analysis agent
        """
        if not cls._initialized:
            await cls.initialize()
            
        from app.ai.agents.risk_agent import RiskAnalysisAgent
        
        cache_service = await cls.get_cache_service()
        metrics_tracker = await cls.get_metrics_tracker()
        
        agent = RiskAnalysisAgent(
            cache_service=cache_service,
            metrics_tracker=metrics_tracker
        )
        await agent.initialize()
        
        return agent
    
    @classmethod
    async def get_document_comparison_agent(cls):
        """
        Get a document comparison agent instance.
        
        Returns:
            Document comparison agent
        """
        if not cls._initialized:
            await cls.initialize()
            
        from app.ai.agents.comparison_agent import DocumentComparisonAgent
        
        cache_service = await cls.get_cache_service()
        metrics_tracker = await cls.get_metrics_tracker()
        
        agent = DocumentComparisonAgent(
            cache_service=cache_service,
            metrics_tracker=metrics_tracker
        )
        await agent.initialize()
        
        return agent
    
    @classmethod
    async def get_recommendation_agent(cls):
        """
        Get a recommendation agent instance.
        
        Returns:
            Recommendation agent
        """
        if not cls._initialized:
            await cls.initialize()
            
        from app.ai.agents.recommendation_agent import RecommendationAgent
        
        cache_service = await cls.get_cache_service()
        metrics_tracker = await cls.get_metrics_tracker()
        
        agent = RecommendationAgent(
            cache_service=cache_service,
            metrics_tracker=metrics_tracker
        )
        await agent.initialize()
        
        return agent
    
    @classmethod
    async def shutdown(cls) -> None:
        """Shutdown all services."""
        await RedisService.close()
        logger.info("ServiceFactory shutdown complete") 