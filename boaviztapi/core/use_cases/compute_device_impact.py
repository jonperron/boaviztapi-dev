"""Use cases for computing device environmental impacts (IoT and Terminals).

This module contains use cases for IoT devices and user terminals.
"""

from typing import List, Optional

from boaviztapi.core.ports.input.compute_device import (
    IComputeIoTImpact,
    IComputeTerminalImpact,
)
from boaviztapi.core.ports.output.archetype_repository import IArchetypeRepository
from boaviztapi.core.ports.output.factor_provider import IFactorProvider
from boaviztapi.core.domain.model.device import (
    IoTDeviceConfiguration,
    TerminalConfiguration,
)
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.core.domain.model.impact import ImpactResult, ImpactValue, PhaseImpact
from boaviztapi.core.domain.exceptions import (
    InvalidDeviceConfigurationError,
    InvalidUsageConfigurationError,
)
from decimal import Decimal
from boaviztapi.core.config_constants import HOURS_PER_YEAR


class ComputeIoTImpactUseCase(IComputeIoTImpact):
    """Use case for computing IoT device environmental impact."""
    
    def __init__(
        self,
        archetype_repository: IArchetypeRepository,
        factor_provider: IFactorProvider,
    ):
        self._archetype_repo = archetype_repository
        self._factor_provider = factor_provider
    
    def execute(
        self,
        device_config: IoTDeviceConfiguration,
        usage_config: UsageConfiguration,
        criteria: List[str],
        duration: Optional[float] = None,
        verbose: bool = False,
    ) -> ImpactResult:
        """Compute environmental impact of an IoT device."""
        if device_config is None:
            raise InvalidDeviceConfigurationError("IoT device configuration is required")
        
        if usage_config is None:
            raise InvalidUsageConfigurationError("Usage configuration is required")
        
        if duration is None:
            duration = HOURS_PER_YEAR
        
        # TODO: Implement actual computation logic
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


class ComputeTerminalImpactUseCase(IComputeTerminalImpact):
    """Use case for computing user terminal environmental impact."""
    
    def __init__(
        self,
        archetype_repository: IArchetypeRepository,
        factor_provider: IFactorProvider,
    ):
        self._archetype_repo = archetype_repository
        self._factor_provider = factor_provider
    
    def execute(
        self,
        terminal_config: TerminalConfiguration,
        usage_config: UsageConfiguration,
        criteria: List[str],
        duration: Optional[float] = None,
        verbose: bool = False,
    ) -> ImpactResult:
        """Compute environmental impact of a user terminal."""
        if terminal_config is None:
            raise InvalidDeviceConfigurationError("Terminal configuration is required")
        
        if usage_config is None:
            raise InvalidUsageConfigurationError("Usage configuration is required")
        
        if duration is None:
            duration = HOURS_PER_YEAR
        
        # TODO: Implement actual computation logic
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