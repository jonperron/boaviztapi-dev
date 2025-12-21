"""Driven adapter: YAML/CSV-based factor provider.

This module implements the IFactorProvider output port by reading
environmental impact factors from YAML and CSV files.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional, List

import yaml

from boaviztapi import data_dir
from boaviztapi.core.ports.output.factor_provider import IFactorProvider


class FactorProvider(IFactorProvider):
    """Driven Adapter: YAML/CSV-based factor provider.
    
    Implements the IFactorProvider output port by loading environmental
    impact factors from YAML configuration files. This adapter bridges
    the application core with the file-based factor data.
    """
    
    def __init__(self, data_path: Optional[str] = None):
        """Initialize the factor provider.
        
        Args:
            data_path: Path to data directory. If None, uses default data_dir
        """
        self._data_path = data_path or data_dir
        self._factors: Optional[Dict[str, Any]] = None
        self._load_factors()
    
    def _load_factors(self) -> None:
        """Load impact factors from YAML file."""
        config_file = os.path.join(self._data_path, 'factors.yml')
        if os.path.exists(config_file):
            self._factors = yaml.safe_load(Path(config_file).read_text())
        else:
            self._factors = {}
    
    def get_impact_factors(self, category: str) -> Optional[Dict[str, Any]]:
        """Get environmental impact factors for a category.
        
        Args:
            category: Factor category (e.g., 'cpu', 'ram', 'ssd')
            
        Returns:
            Dictionary containing impact factors or None if not found
        """
        if not self._factors:
            return None
        
        return self._factors.get(category)
    
    def get_electrical_mix(self, country_code: str) -> Optional[Dict[str, Any]]:
        """Get electrical mix data for a country.
        
        Args:
            country_code: ISO country code (e.g., 'FR', 'US')
            
        Returns:
            Dictionary containing electrical mix data or None if not found
        """
        if not self._factors or 'electricity' not in self._factors:
            return None
        
        electricity = self._factors['electricity']
        
        # Check if country code exists directly
        if country_code in electricity:
            return electricity[country_code]
        
        # Check in available_countries mapping
        available = electricity.get('available_countries', {})
        if country_code in available.values():
            # Find the key that maps to this country code
            for key, value in available.items():
                if value == country_code:
                    return electricity.get(key)
        
        return None
    
    def get_available_countries(self) -> List[str]:
        """Get list of available country codes for electrical mix data.
        
        Returns:
            List of available country codes
        """
        if not self._factors or 'electricity' not in self._factors:
            return []
        
        electricity = self._factors['electricity']
        available = electricity.get('available_countries', {})
        
        # Return list of country codes (values in the mapping)
        return list(available.values())
    
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
        if not self._factors:
            return None
        
        # Check if consumption profiles exist
        consumption_profiles = self._factors.get('consumption_profiles')
        if consumption_profiles and component_type in consumption_profiles:
            return consumption_profiles[component_type]
        
        return None
    
    def get_electrical_impact_factor(
        self, 
        usage_location: str, 
        impact_type: str
    ) -> Optional[Dict[str, Any]]:
        """Get electrical impact factor for a location and impact type.
        
        This is a convenience method that combines electrical mix data
        with impact type retrieval.
        
        Args:
            usage_location: Country code or location identifier
            impact_type: Type of impact (e.g., 'gwp', 'pe', 'adp')
            
        Returns:
            Dictionary containing impact factor data or None if not found
        """
        electrical_mix = self.get_electrical_mix(usage_location)
        
        if not electrical_mix:
            return None
        
        return electrical_mix.get(impact_type)
    
    def get_iot_impact_factor(
        self, 
        functional_block: str, 
        hsl: str, 
        impact_type: str
    ) -> Optional[float]:
        """Get IoT device impact factor.
        
        Args:
            functional_block: IoT functional block (e.g., 'PROCESSING', 'SENSING')
            hsl: Hardware Support Level
            impact_type: Type of impact (e.g., 'gwp', 'pe')
            
        Returns:
            Impact factor value or None if not found
        """
        if not self._factors or 'IoT' not in self._factors:
            return None
        
        iot_factors = self._factors['IoT']
        
        if functional_block not in iot_factors:
            return None
        
        if hsl not in iot_factors[functional_block]:
            return None
        
        hsl_data = iot_factors[functional_block][hsl]
        
        # Combine manufacture and end-of-life impacts
        manufacture = hsl_data.get('manufacture', {}).get(impact_type)
        eol = hsl_data.get('eol', {}).get(impact_type)
        
        if manufacture is not None and eol is not None:
            return manufacture + eol
        
        return None
    
    def reload_factors(self) -> None:
        """Reload factors from file.
        
        Useful for testing or when factors are updated at runtime.
        """
        self._load_factors()
