"""
Mapper to convert cloud API requests to domain models.
"""
from typing import Optional
from decimal import Decimal
from boaviztapi.core.domain.model.device import CloudInstanceConfiguration
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.adapters.driving.rest.schemas.cloud import CloudRequestSchema
from boaviztapi.adapters.driving.rest.schemas.common import UsageSchema


class CloudMapper:
    """Maps cloud API requests to domain models."""
    
    @staticmethod
    def to_cloud_instance_configuration(request: CloudRequestSchema) -> CloudInstanceConfiguration:
        """
        Convert cloud API request to domain CloudInstanceConfiguration.
        
        Args:
            request: Cloud API request
            
        Returns:
            Domain cloud instance configuration
        """
        return CloudInstanceConfiguration(
            provider=request.provider or "",
            instance_type=request.instance_type or ""
        )
    
    @staticmethod
    def to_usage_configuration(usage_schema: Optional[UsageSchema]) -> UsageConfiguration:
        """
        Convert API usage schema to domain UsageConfiguration.
        
        Args:
            usage_schema: API usage schema
            
        Returns:
            Domain usage configuration
        """
        if not usage_schema:
            return UsageConfiguration()
        
        workload = None
        if usage_schema.workload:
            workload = {k: Decimal(str(v)) for k, v in usage_schema.workload.items()}
        
        return UsageConfiguration(
            location=usage_schema.usage_location,
            hours_life_time=Decimal(str(usage_schema.hours_life_time)) 
                if usage_schema.hours_life_time is not None else None,
            workload=workload
        )
