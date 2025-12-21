"""Dependency Injection Container for the hexagonal architecture.

This module provides a simple DI container that instantiates and wires
together all the components of the hexagonal architecture:
- Driven adapters (output port implementations)
- Use cases (business logic)
- Makes them available to the driving adapters (API routers)
"""

from typing import Optional

from boaviztapi.core.use_cases.compute_server_impact import ComputeServerImpactUseCase
from boaviztapi.adapters.driven.persistence.archetype_repository import ArchetypeRepository
from boaviztapi.adapters.driven.persistence.factor_provider import FactorProvider


class DIContainer:
    """Simple dependency injection container.
    
    This container follows the singleton pattern and provides instances
    of use cases with their dependencies properly wired.
    """
    
    _instance: Optional['DIContainer'] = None
    
    def __init__(self):
        """Initialize the DI container with all dependencies."""
        # Initialize driven adapters (output ports)
        self._archetype_repository = ArchetypeRepository()
        self._factor_provider = FactorProvider()
        
        # Initialize use cases with dependencies
        self._compute_server_impact_use_case = ComputeServerImpactUseCase(
            archetype_repository=self._archetype_repository,
            factor_provider=self._factor_provider
        )
    
    @classmethod
    def get_instance(cls) -> 'DIContainer':
        """Get the singleton instance of the DI container.
        
        Returns:
            The singleton DIContainer instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (useful for testing)."""
        cls._instance = None
    
    def get_compute_server_impact_use_case(self) -> ComputeServerImpactUseCase:
        """Get the compute server impact use case.
        
        Returns:
            Fully wired ComputeServerImpactUseCase instance
        """
        return self._compute_server_impact_use_case
    
    def get_archetype_repository(self) -> ArchetypeRepository:
        """Get the archetype repository.
        
        Returns:
            ArchetypeRepository instance
        """
        return self._archetype_repository
    
    def get_factor_provider(self) -> FactorProvider:
        """Get the factor provider.
        
        Returns:
            FactorProvider instance
        """
        return self._factor_provider


# Convenience function to get the container instance
def get_container() -> DIContainer:
    """Get the DI container instance.
    
    Returns:
        The singleton DIContainer instance
    """
    return DIContainer.get_instance()
