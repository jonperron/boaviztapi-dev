"""
Mapper to convert domain models to API response schemas.
"""
from typing import Dict, Optional, Any
from boaviztapi.core.domain.model.impact import ImpactResult, ImpactValue, PhaseImpact
from boaviztapi.adapters.driving.rest.schemas.common import (
    ImpactValueSchema,
    PhaseImpactSchema,
    ImpactResponseSchema
)


class ResponseMapper:
    """Maps domain impact results to API response schemas."""
    
    @staticmethod
    def to_impact_value_schema(impact_value: ImpactValue) -> ImpactValueSchema:
        """
        Convert domain ImpactValue to API schema.
        
        Args:
            impact_value: Domain impact value
            
        Returns:
            API impact value schema
        """
        return ImpactValueSchema(
            value=float(impact_value.value),
            min=float(impact_value.min_value) if impact_value.min_value is not None else None,
            max=float(impact_value.max_value) if impact_value.max_value is not None else None,
            unit=impact_value.unit
        )
    
    @staticmethod
    def to_phase_impact_schema(phase_impacts: Dict[str, ImpactValue]) -> PhaseImpactSchema:
        """
        Convert domain phase impacts dictionary to API schema.
        
        Args:
            phase_impacts: Dictionary of impact values by criteria
            
        Returns:
            API phase impact schema
        """
        impact_schemas = {
            criteria: ResponseMapper.to_impact_value_schema(value)
            for criteria, value in phase_impacts.items()
        }
        
        return PhaseImpactSchema(impacts=impact_schemas)
    
    @staticmethod
    def to_impact_response_schema(
        impact_result: ImpactResult,
        verbose: bool = True
    ) -> ImpactResponseSchema:
        """
        Convert domain ImpactResult to API response schema.
        
        Args:
            impact_result: Domain impact result
            verbose: Whether to include verbose data
            
        Returns:
            API impact response schema
        """
        response = ImpactResponseSchema(
            manufacture=ResponseMapper.to_phase_impact_schema(impact_result.phases.manufacturing) 
                if impact_result.phases.manufacturing else None,
            use=ResponseMapper.to_phase_impact_schema(impact_result.phases.use) 
                if impact_result.phases.use else None,
            end_of_life=ResponseMapper.to_phase_impact_schema(impact_result.phases.end_of_life) 
                if impact_result.phases.end_of_life else None
        )
        
        if verbose and impact_result.verbose_data:
            response.verbose = impact_result.verbose_data
        
        return response
