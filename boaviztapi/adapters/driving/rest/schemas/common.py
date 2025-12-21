"""
Common API schemas shared across endpoints.
"""
from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class ImpactValueSchema(BaseModel):
    """API schema for a single impact value."""
    value: float = Field(description="Impact value")
    min: Optional[float] = Field(None, description="Minimum value (uncertainty)")
    max: Optional[float] = Field(None, description="Maximum value (uncertainty)")
    unit: str = Field(description="Unit of measurement")


class PhaseImpactSchema(BaseModel):
    """API schema for impacts grouped by phase (manufacture, use, etc.)."""
    impacts: Dict[str, ImpactValueSchema] = Field(
        description="Impact values by criteria (gwp, adp, pe, etc.)"
    )


class ImpactResponseSchema(BaseModel):
    """API schema for impact computation results."""
    manufacture: Optional[PhaseImpactSchema] = Field(
        None, 
        description="Manufacturing phase impacts"
    )
    use: Optional[PhaseImpactSchema] = Field(
        None, 
        description="Use phase impacts"
    )
    end_of_life: Optional[PhaseImpactSchema] = Field(
        None, 
        description="End of life phase impacts"
    )
    verbose: Optional[Dict[str, Any]] = Field(
        None, 
        description="Detailed information about the computation"
    )


class UsageSchema(BaseModel):
    """API schema for usage configuration."""
    usage_location: Optional[str] = Field(
        None,
        description="ISO 3166-1 alpha-3 country code"
    )
    hours_life_time: Optional[float] = Field(
        None,
        description="Expected lifetime in hours",
        gt=0
    )
    time_workload: Optional[float] = Field(
        None,
        description="Percentage of time at workload",
        ge=0,
        le=100
    )
    workload: Optional[Dict[str, float]] = Field(
        None,
        description="Workload profile percentages"
    )
    
    @staticmethod
    def to_domain(usage_schema: 'UsageSchema'):
        """Convert UsageSchema to domain UsageConfiguration."""
        from boaviztapi.core.domain.model.usage import UsageConfiguration
        from boaviztapi.core.config_constants import (
            HOURS_PER_YEAR,
            DEFAULT_LIFETIME_HOURS,
            DEFAULT_LOCATION
        )
        from decimal import Decimal
        
        # Use provided values or defaults from config
        hours_life_time = usage_schema.hours_life_time if usage_schema.hours_life_time else DEFAULT_LIFETIME_HOURS
        
        workload_dict = None
        if usage_schema.workload:
            workload_dict = {k: Decimal(str(v)) for k, v in usage_schema.workload.items()}
        
        return UsageConfiguration(
            hours_use_time=Decimal(str(HOURS_PER_YEAR)),
            hours_life_time=Decimal(str(hours_life_time)),
            location=usage_schema.usage_location if usage_schema.usage_location else DEFAULT_LOCATION,
            workload=workload_dict
        )
