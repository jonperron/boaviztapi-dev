"""Use case for computing component environmental impact.

This use case implements the IComputeComponentImpact input port and orchestrates
the computation of environmental impacts for individual hardware components.
"""

from typing import List, Optional

from boaviztapi.core.ports.input.compute_component import IComputeComponentImpact
from boaviztapi.core.ports.output.archetype_repository import IArchetypeRepository
from boaviztapi.core.ports.output.factor_provider import IFactorProvider
from boaviztapi.core.domain.model.device import ComponentConfiguration
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.core.domain.model.impact import ImpactResult
from boaviztapi.core.domain.exceptions import (
    InvalidComponentConfigurationError,
    InvalidUsageConfigurationError,
    MissingRequiredDataError,
)


class ComputeComponentImpactUseCase(IComputeComponentImpact):
    """Use case for computing component environmental impact.
    
    This implementation follows the hexagonal architecture pattern:
    - It implements an Input Port (IComputeComponentImpact)
    - It uses Output Ports for data access
    - It contains pure business logic with no framework dependencies
    """
    
    def __init__(
        self,
        archetype_repository: IArchetypeRepository,
        factor_provider: IFactorProvider,
    ):
        """Initialize the use case with required dependencies.
        
        Args:
            archetype_repository: Port for accessing archetype data
            factor_provider: Port for accessing impact factors
        """
        self._archetype_repo = archetype_repository
        self._factor_provider = factor_provider
    
    def execute(
        self,
        component_config: ComponentConfiguration,
        usage_config: UsageConfiguration,
        criteria: List[str],
        duration: Optional[float] = None,
        verbose: bool = False,
    ) -> ImpactResult:
        """Compute environmental impact of a hardware component.
        
        Args:
            component_config: Component configuration (CPU, RAM, etc.)
            usage_config: Usage patterns and location
            criteria: Environmental impact criteria to compute
            duration: Duration in years for usage phase calculation
            verbose: Whether to include detailed calculation information
            
        Returns:
            ImpactResult: Computed environmental impacts
            
        Raises:
            InvalidComponentConfigurationError: If component configuration is invalid
            MissingRequiredDataError: If required data is not available
        """
        # Validate inputs
        self._validate_component_config(component_config)
        self._validate_usage_config(usage_config)
        
        # Use default duration if not provided
        if duration is None:
            duration = 8760.0  # hours per year
        
        # TODO: Implement actual computation logic
        # This is a stub implementation
        from boaviztapi.core.domain.model.impact import (
            ImpactValue,
            PhaseImpact,
        )
        from decimal import Decimal
        
        stub_impact = ImpactValue(
            value=Decimal('0'),
            min_value=Decimal('0'),
            max_value=Decimal('0'),
            unit='kgCO2eq',
            source='STUB'
        )
        
        phases = PhaseImpact(
            manufacturing={},
            use={},
            end_of_life={}
        )
        
        return ImpactResult(
            impacts={},
            phases=phases,
            duration_years=duration / 8760.0,
            verbose_data={} if verbose else None
        )
    
    def _validate_component_config(self, config: ComponentConfiguration) -> None:
        """Validate component configuration."""
        if config is None:
            raise InvalidComponentConfigurationError(
                "unknown", "Component configuration is required"
            )
        
        if not config.component_type:
            raise InvalidComponentConfigurationError(
                "unknown", "Component type is required"
            )
    
    def _validate_usage_config(self, config: UsageConfiguration) -> None:
        """Validate usage configuration."""
        if config is None:
            raise InvalidUsageConfigurationError("Usage configuration is required")