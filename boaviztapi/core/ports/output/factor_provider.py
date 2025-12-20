"""Output port for accessing environmental impact factors.

This interface defines the contract for retrieving environmental impact
factors and electrical mix data used in impact calculations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class IFactorProvider(ABC):
    """Output Port: Interface for accessing environmental impact factors.
    
    The application core uses this interface to retrieve impact factors
    and electrical mix data needed for environmental calculations.
    """
    
    @abstractmethod
    def get_impact_factors(self, category: str) -> Optional[Dict[str, Any]]:
        """Get environmental impact factors for a category.
        
        Args:
            category: Factor category (e.g., 'cpu', 'ram', 'ssd')
            
        Returns:
            Dictionary containing impact factors or None if not found
        """
        pass
    
    @abstractmethod
    def get_electrical_mix(self, country_code: str) -> Optional[Dict[str, Any]]:
        """Get electrical mix data for a country.
        
        Args:
            country_code: ISO country code (e.g., 'FR', 'US')
            
        Returns:
            Dictionary containing electrical mix data or None if not found
        """
        pass
    
    @abstractmethod
    def get_available_countries(self) -> List[str]:
        """Get list of available country codes for electrical mix data.
        
        Returns:
            List of available country codes
        """
        pass
    
    @abstractmethod
    def get_consumption_profile_factors(
        self, 
        component_type: str
    ) -> Optional[Dict[str, Any]]:
        """Get consumption profile factors for a component type.
        
        Args:
            component_type: Type of component ('cpu', 'ram', etc.)
            
        Returns:
            Dictionary containing consumption profile factors or None if not found
        """
        pass


class IElectricalMixProvider(ABC):
    """Output Port: Interface specifically for electrical mix data.
    
    This could be a separate service or part of IFactorProvider depending
    on the implementation architecture.
    """
    
    @abstractmethod
    def get_electrical_mix_by_country(self, country_code: str) -> Optional[Dict[str, Any]]:
        """Get electrical mix data by country code."""
        pass
    
    @abstractmethod
    def get_default_electrical_mix(self) -> Dict[str, Any]:
        """Get default electrical mix (e.g., world average)."""
        pass