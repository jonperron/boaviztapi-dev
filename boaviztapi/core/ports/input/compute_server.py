"""Input port for computing server environmental impact.

This interface defines the contract for computing environmental impact
of server devices. It follows the hexagonal architecture pattern where
driving adapters (like REST API) call this interface.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from boaviztapi.core.domain.model.device import DeviceConfiguration
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.core.domain.model.impact import ImpactResult


class IComputeServerImpact(ABC):
    """Input Port: Interface for computing server environmental impact.
    
    This interface is called by driving adapters (like FastAPI routers)
    to compute environmental impact of server configurations.
    """
    
    @abstractmethod
    def execute(
        self,
        device_config: DeviceConfiguration,
        usage_config: UsageConfiguration,
        criteria: List[str],
        duration: Optional[float] = None,
        verbose: bool = False
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
        """
        pass