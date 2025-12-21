"""Use case for computing cloud instance environmental impact.

This use case implements the IComputeCloudImpact input port and orchestrates
the computation of environmental impacts for cloud service instances.
"""

from typing import List, Optional

from boaviztapi.core.ports.input.compute_cloud import IComputeCloudImpact
from boaviztapi.core.ports.output.archetype_repository import IArchetypeRepository
from boaviztapi.core.ports.output.factor_provider import IFactorProvider
from boaviztapi.core.domain.model.device import CloudInstanceConfiguration
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.core.domain.model.impact import ImpactResult
from boaviztapi.core.domain.exceptions import (
    InvalidDeviceConfigurationError,
    InvalidUsageConfigurationError,
    MissingRequiredDataError,
)
from boaviztapi.core.config_constants import HOURS_PER_YEAR


class ComputeCloudImpactUseCase(IComputeCloudImpact):
    """Use case for computing cloud instance environmental impact.
    
    This implementation follows the hexagonal architecture pattern:
    - It implements an Input Port (IComputeCloudImpact)
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
        instance_config: CloudInstanceConfiguration,
        usage_config: UsageConfiguration,
        criteria: List[str],
        duration: Optional[float] = None,
        verbose: bool = False,
    ) -> ImpactResult:
        """Compute environmental impact of a cloud instance.
        
        Args:
            instance_config: Cloud instance configuration
            usage_config: Usage patterns and location
            criteria: Environmental impact criteria to compute
            duration: Duration in years for usage phase calculation
            verbose: Whether to include detailed calculation information
            
        Returns:
            ImpactResult: Computed environmental impacts
            
        Raises:
            InvalidDeviceConfigurationError: If instance configuration is invalid
            MissingRequiredDataError: If required data is not available
        """
        # Validate inputs
        self._validate_instance_config(instance_config)
        self._validate_usage_config(usage_config)
        
        # Use default duration if not provided
        if duration is None:
            duration = HOURS_PER_YEAR
        
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
            duration_years=duration / HOURS_PER_YEAR,
            verbose_data={} if verbose else None
        )
    
    def _validate_instance_config(self, config: CloudInstanceConfiguration) -> None:
        """Validate cloud instance configuration."""
        if config is None:
            raise InvalidDeviceConfigurationError("Instance configuration is required")
        
        if not config.instance_type:
            raise InvalidDeviceConfigurationError("Instance type is required")
        
        if not config.provider:
            raise InvalidDeviceConfigurationError("Provider is required")
    
    def _validate_usage_config(self, config: UsageConfiguration) -> None:
        """Validate usage configuration."""
        if config is None:
            raise InvalidUsageConfigurationError("Usage configuration is required")