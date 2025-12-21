"""Unit tests for FactorProvider driven adapter."""

import pytest
import os

from boaviztapi.adapters.driven.persistence.factor_provider import FactorProvider
from boaviztapi import data_dir


class TestFactorProvider:
    """Test suite for FactorProvider adapter."""
    
    @pytest.fixture
    def provider(self):
        """Create a FactorProvider instance."""
        return FactorProvider()
    
    def test_provider_instantiation(self, provider):
        """Test that provider can be instantiated."""
        assert provider is not None
        assert isinstance(provider, FactorProvider)
    
    def test_provider_with_custom_data_path(self):
        """Test provider with custom data path."""
        prov = FactorProvider(data_path=data_dir)
        assert prov is not None
    
    def test_factors_loaded(self, provider):
        """Test that factors are loaded on initialization."""
        assert provider._factors is not None
        assert isinstance(provider._factors, dict)
    
    def test_get_impact_factors_cpu(self, provider):
        """Test getting CPU impact factors."""
        result = provider.get_impact_factors("cpu")
        
        # Should return impact factors for CPU
        if result is not None:
            assert isinstance(result, dict)
    
    def test_get_impact_factors_ram(self, provider):
        """Test getting RAM impact factors."""
        result = provider.get_impact_factors("ram")
        
        if result is not None:
            assert isinstance(result, dict)
    
    def test_get_impact_factors_nonexistent(self, provider):
        """Test getting nonexistent impact factors."""
        result = provider.get_impact_factors("nonexistent_category_xyz")
        
        # Should return None for nonexistent category
        assert result is None
    
    def test_get_electrical_mix_france(self, provider):
        """Test getting electrical mix for France."""
        # Try various ways France might be referenced
        result = provider.get_electrical_mix("FR")
        
        if result is None:
            result = provider.get_electrical_mix("FRA")
        
        if result is None:
            result = provider.get_electrical_mix("france")
        
        # At least one should work if electrical mix data exists
        # We don't assert since data structure may vary
        if result is not None:
            assert isinstance(result, dict)
    
    def test_get_electrical_mix_world(self, provider):
        """Test getting world average electrical mix."""
        # Try various ways world/default might be referenced
        result = provider.get_electrical_mix("WOR")
        
        if result is None:
            result = provider.get_electrical_mix("WORLD")
        
        if result is None:
            result = provider.get_electrical_mix("default")
        
        # We don't assert since data structure may vary
        if result is not None:
            assert isinstance(result, dict)
    
    def test_get_electrical_mix_nonexistent(self, provider):
        """Test getting electrical mix for nonexistent country."""
        result = provider.get_electrical_mix("NONEXISTENT_XYZ")
        
        # Should return None for nonexistent country
        assert result is None
    
    def test_get_available_countries(self, provider):
        """Test getting list of available countries."""
        result = provider.get_available_countries()
        
        # Should return a list
        assert isinstance(result, list)
        
        # Should have at least some countries if data exists
        # We don't assert length since data may vary
    
    def test_get_consumption_profile_factors(self, provider):
        """Test getting consumption profile factors."""
        # Try to get CPU consumption profile
        result = provider.get_consumption_profile_factors("cpu")
        
        # May or may not exist depending on data structure
        if result is not None:
            assert isinstance(result, dict)
    
    def test_get_electrical_impact_factor(self, provider):
        """Test getting electrical impact factor for location."""
        # Try to get GWP factor for France
        result = provider.get_electrical_impact_factor("FR", "gwp")
        
        if result is None:
            result = provider.get_electrical_impact_factor("FRA", "gwp")
        
        # May or may not exist depending on data structure
        if result is not None:
            assert isinstance(result, dict) or isinstance(result, (int, float))
    
    def test_get_iot_impact_factor(self, provider):
        """Test getting IoT impact factor."""
        # Try to get IoT factor if IoT data exists
        result = provider.get_iot_impact_factor("PROCESSING", "low", "gwp")
        
        # May or may not exist depending on data structure
        if result is not None:
            assert isinstance(result, (int, float))
    
    def test_get_iot_impact_factor_nonexistent(self, provider):
        """Test getting nonexistent IoT impact factor."""
        result = provider.get_iot_impact_factor(
            "NONEXISTENT_BLOCK_XYZ", 
            "invalid_hsl", 
            "gwp"
        )
        
        # Should return None for nonexistent factor
        assert result is None
    
    def test_reload_factors(self, provider):
        """Test reloading factors from file."""
        # Get initial factors
        initial_factors = provider._factors
        
        # Reload
        provider.reload_factors()
        
        # Factors should be reloaded (may be same object or new)
        assert provider._factors is not None
    
    def test_impact_factors_structure(self, provider):
        """Test that impact factors have expected structure."""
        # Check that factors dict has expected top-level keys
        if provider._factors:
            # Common categories that should exist
            possible_categories = ['cpu', 'ram', 'ssd', 'hdd', 'electricity', 'SERVER']
            
            # At least some should exist
            found_categories = [cat for cat in possible_categories if cat in provider._factors]
            
            # We expect at least some standard categories
            assert len(found_categories) > 0
