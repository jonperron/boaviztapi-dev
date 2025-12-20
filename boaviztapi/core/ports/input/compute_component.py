"""Input port for computing component environmental impact.

This interface defines the contract for computing environmental impact
of individual hardware components.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from boaviztapi.core.domain.model.device import ComponentConfiguration
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.core.domain.model.impact import ImpactResult


class IComputeComponentImpact(ABC):
    """Input Port: Interface for computing component environmental impact.
    
    This interface is called by driving adapters to compute environmental 
    impact of individual hardware components (CPU, RAM, disk, etc.).
    """
    
    @abstractmethod
    def execute(
        self,
        component_config: ComponentConfiguration,
        usage_config: UsageConfiguration,
        criteria: List[str],
        duration: Optional[float] = None,
        verbose: bool = False
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
        """
        pass