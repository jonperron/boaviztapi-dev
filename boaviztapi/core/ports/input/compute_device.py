"""Input port for computing IoT device environmental impact.

This interface defines the contract for computing environmental impact
of IoT devices and terminals.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from boaviztapi.core.domain.model.device import IoTDeviceConfiguration, TerminalConfiguration
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.core.domain.model.impact import ImpactResult


class IComputeIoTImpact(ABC):
    """Input Port: Interface for computing IoT device environmental impact."""
    
    @abstractmethod
    def execute(
        self,
        device_config: IoTDeviceConfiguration,
        usage_config: UsageConfiguration,
        criteria: List[str],
        duration: Optional[float] = None,
        verbose: bool = False
    ) -> ImpactResult:
        """Compute environmental impact of an IoT device."""
        pass


class IComputeTerminalImpact(ABC):
    """Input Port: Interface for computing user terminal environmental impact."""
    
    @abstractmethod
    def execute(
        self,
        terminal_config: TerminalConfiguration,
        usage_config: UsageConfiguration,
        criteria: List[str],
        duration: Optional[float] = None,
        verbose: bool = False
    ) -> ImpactResult:
        """Compute environmental impact of a user terminal (laptop, desktop, etc.)."""
        pass