"""
Mapper to convert component API requests to domain models.
"""
from typing import Optional
from decimal import Decimal
from boaviztapi.core.domain.model.device import (
    CPUConfiguration,
    RAMConfiguration,
    DiskConfiguration
)
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.adapters.driving.rest.schemas.component import (
    ComponentCPURequestSchema,
    ComponentRAMRequestSchema,
    ComponentSSDRequestSchema
)
from boaviztapi.adapters.driving.rest.schemas.common import UsageSchema


class ComponentMapper:
    """Maps component API requests to domain models."""
    
    @staticmethod
    def to_cpu_configuration(request: ComponentCPURequestSchema) -> CPUConfiguration:
        """
        Convert component CPU API request to domain CPUConfiguration.
        
        Args:
            request: Component CPU API request
            
        Returns:
            Domain CPU configuration
        """
        return CPUConfiguration(
            core_units=request.core_units,
            die_size_per_core=Decimal(str(request.die_size_per_core)) 
                if request.die_size_per_core is not None else None,
            name=request.name,
            tdp=Decimal(str(request.tdp)) if request.tdp is not None else None,
            manufacturer=request.manufacturer,
            family=request.family
        )
    
    @staticmethod
    def to_ram_configuration(request: ComponentRAMRequestSchema) -> RAMConfiguration:
        """
        Convert component RAM API request to domain RAMConfiguration.
        
        Args:
            request: Component RAM API request
            
        Returns:
            Domain RAM configuration
        """
        return RAMConfiguration(
            capacity_gb=Decimal(str(request.capacity)) if request.capacity is not None else None,
            density=Decimal(str(request.density)) if request.density is not None else None,
            manufacturer=request.manufacturer
        )
    
    @staticmethod
    def to_ssd_configuration(request: ComponentSSDRequestSchema) -> DiskConfiguration:
        """
        Convert component SSD API request to domain DiskConfiguration.
        
        Args:
            request: Component SSD API request
            
        Returns:
            Domain disk configuration (SSD type)
        """
        return DiskConfiguration(
            type="ssd",
            capacity_gb=Decimal(str(request.capacity)) if request.capacity is not None else None,
            manufacturer=request.manufacturer
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
