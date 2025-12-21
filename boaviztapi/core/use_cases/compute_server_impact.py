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
from boaviztapi.core.domain.model.impact import ImpactResult, PhaseImpact
from boaviztapi.core.domain.services.impact_calculator import ImpactCalculator
from boaviztapi.core.domain.exceptions import (
    InvalidDeviceConfigurationError,
    InvalidUsageConfigurationError,
    MissingRequiredDataError,
)
from boaviztapi.core.config_constants import HOURS_PER_YEAR


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
        self._calculator = ImpactCalculator()
    
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
        
        # Use default duration if not provided (in hours)
        if duration is None:
            duration = HOURS_PER_YEAR
        
        # Phase 4: Simplified implementation demonstrating hexagonal architecture
        # TODO: Full migration of Boattribute-based logic in Phase 7
        
        # Get impact factors from driven adapter
        impact_factors = self._get_impact_factors()
        
        # Get electrical factors for the usage location
        electrical_factors = self._get_electrical_factors(usage_config.location)
        
        # Calculate impacts for each phase using domain service
        manufacturing_impacts = self._calculator.calculate_manufacturing_impact(
            device_config=device_config,
            criteria=criteria,
            impact_factors=impact_factors
        )
        
        use_impacts = self._calculator.calculate_use_impact(
            device_config=device_config,
            usage_config=usage_config,
            criteria=criteria,
            duration_hours=duration,
            electrical_factors=electrical_factors
        )
        
        end_of_life_impacts = self._calculator.calculate_end_of_life_impact(
            device_config=device_config,
            criteria=criteria,
            impact_factors=impact_factors
        )
        
        # Aggregate total impacts
        total_impacts = self._calculator.aggregate_phase_impacts(
            manufacturing=manufacturing_impacts,
            use=use_impacts,
            end_of_life=end_of_life_impacts
        )
        
        # Build phase impact structure
        phases = self._build_phase_impacts(
            manufacturing_impacts,
            use_impacts,
            end_of_life_impacts
        )
        
        # Build verbose data if requested
        verbose_data = None
        if verbose:
            verbose_data = self._build_verbose_data(device_config, usage_config)
        
        return ImpactResult(
            impacts=total_impacts,
            phases=phases,
            duration_years=duration / HOURS_PER_YEAR,
            verbose_data=verbose_data
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
    
    def _get_impact_factors(self) -> dict:
        """Get impact factors from factor provider.
        
        TODO: Implement actual factor retrieval using self._factor_provider
        For now, return simplified factors for demonstration
        """
        return {
            'cpu': {'impact': 20.0, 'die_impact': 2.0},
            'ram': {'impact': 10.0, 'die_impact': 0.5},
            'ssd': {'impact': 15.0, 'die_impact': 1.0},
            'hdd': {'impact': 12.0},
        }
    
    def _get_electrical_factors(self, location: Optional[str]) -> dict:
        """Get electrical factors for the specified location.
        
        TODO: Implement actual electrical factor retrieval using self._factor_provider
        For now, return simplified factors (world average)
        """
        # Simplified world average electrical factors
        return {
            'gwp': 0.5,  # kgCO2eq/kWh
            'pe': 11.0,  # MJ/kWh
            'adp': 0.00002,  # kgSbeq/kWh
        }
    
    def _build_phase_impacts(self, manufacturing, use, end_of_life) -> PhaseImpact:
        """Build PhaseImpact structure from individual phase impacts."""
        return PhaseImpact(
            manufacturing={k: v for k, v in manufacturing.items()},
            use={k: v for k, v in use.items()},
            end_of_life={k: v for k, v in end_of_life.items()}
        )
    
    def _build_verbose_data(self, device_config, usage_config) -> dict:
        """Build verbose data for detailed output.
        
        TODO: Include detailed component information when verbose=True
        """
        return {
            'device': {
                'cpu': device_config.cpu is not None,
                'ram_count': len(device_config.ram) if device_config.ram else 0,
                'disk_count': len(device_config.disk) if device_config.disk else 0,
            },
            'usage': {
                'location': usage_config.location,
            }
        }