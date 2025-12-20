"""Use case for computing server environmental impact.

This use case implements the IComputeServerImpact input port and orchestrates
the computation of environmental impacts for server devices.
"""

from typing import List, Optional

from boaviztapi.core.ports.input.compute_server import IComputeServerImpact
from boaviztapi.core.ports.output.archetype_repository import IArchetypeRepository
from boaviztapi.core.ports.output.factor_provider import IFactorProvider
from boaviztapi.core.domain.model.device import DeviceConfiguration
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.core.domain.model.impact import ImpactResult
from boaviztapi.core.domain.exceptions import (
    InvalidDeviceConfigurationError,
    InvalidUsageConfigurationError,
    MissingRequiredDataError,
)


class ComputeServerImpactUseCase(IComputeServerImpact):
    """Use case for computing server environmental impact.
    
    This implementation follows the hexagonal architecture pattern:
    - It implements an Input Port (IComputeServerImpact)
    - It uses Output Ports (IArchetypeRepository, IFactorProvider) for data access
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
        device_config: DeviceConfiguration,
        usage_config: UsageConfiguration,
        criteria: List[str],
        duration: Optional[float] = None,
        verbose: bool = False,
    ) -> ImpactResult:
        """Compute environmental impact of a server configuration.
        
        Args:
            device_config: Server hardware configuration
            usage_config: Usage patterns and location
            criteria: Environmental impact criteria to compute (e.g., ['gwp', 'pe'])
            duration: Duration in years for usage phase calculation
            verbose: Whether to include detailed calculation information
            
        Returns:
            ImpactResult: Computed environmental impacts
            
        Raises:
            InvalidDeviceConfigurationError: If device configuration is invalid
            MissingRequiredDataError: If required data is not available
        """
        # Validate inputs
        self._validate_device_config(device_config)
        self._validate_usage_config(usage_config)
        
        # Use default duration if not provided
        if duration is None:
            duration = 8760.0  # hours per year
        
        # TODO: Implement actual computation logic
        # This is a stub implementation that will be completed in later phases
        # The actual implementation will:
        # 1. Load archetype defaults if needed
        # 2. Complete missing configuration values
        # 3. Compute manufacturing impact
        # 4. Compute usage impact
        # 5. Compute end-of-life impact
        # 6. Aggregate results
        
        # For now, return a stub result to maintain interface compatibility
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
    
    def _validate_device_config(self, config: DeviceConfiguration) -> None:
        """Validate device configuration."""
        if config is None:
            raise InvalidDeviceConfigurationError("Device configuration is required")
        
        # Add more validation as needed
        # For now, we accept any configuration
    
    def _validate_usage_config(self, config: UsageConfiguration) -> None:
        """Validate usage configuration."""
        if config is None:
            raise InvalidUsageConfigurationError("Usage configuration is required")