"""
Mapper to convert cloud API requests to domain models.
"""
from typing import Optional
from decimal import Decimal
from boaviztapi.core.domain.model.device import CloudInstanceConfiguration
from boaviztapi.core.domain.model.usage import UsageConfiguration, WorkloadProfile
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
            provider=request.provider,
            instance_type=request.instance_type
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
        
        workload_profile = None
        if usage_schema.workload:
            workload_profile = WorkloadProfile(
                percentages={k: Decimal(str(v)) for k, v in usage_schema.workload.items()}
            )
        
        return UsageConfiguration(
            usage_location=usage_schema.usage_location,
            hours_life_time=Decimal(str(usage_schema.hours_life_time)) 
                if usage_schema.hours_life_time is not None else None,
            time_workload=Decimal(str(usage_schema.time_workload)) 
                if usage_schema.time_workload is not None else None,
            workload_profile=workload_profile
        )
