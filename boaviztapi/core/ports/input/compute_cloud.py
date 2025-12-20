"""Input port for computing cloud instance environmental impact.

This interface defines the contract for computing environmental impact
of cloud service instances.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from boaviztapi.core.domain.model.device import CloudInstanceConfiguration
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.core.domain.model.impact import ImpactResult


class IComputeCloudImpact(ABC):
    """Input Port: Interface for computing cloud instance environmental impact.
    
    This interface is called by driving adapters to compute environmental 
    impact of cloud service instances.
    """
    
    @abstractmethod
    def execute(
        self,
        instance_config: CloudInstanceConfiguration,
        usage_config: UsageConfiguration,
        criteria: List[str],
        duration: Optional[float] = None,
        verbose: bool = False
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
        """
        pass