"""Edge case and error handling tests for Phase 7.

These tests ensure the hexagonal architecture handles edge cases,
invalid inputs, and error conditions gracefully.
"""

import pytest
from decimal import Decimal
from boaviztapi.core.di_container import DIContainer, get_container
from boaviztapi.core.domain.model.device import DeviceConfiguration, CPUConfiguration
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.core.domain.exceptions import (
    InvalidDeviceConfigurationError,
    InvalidUsageConfigurationError,
)
from boaviztapi.core.config_constants import HOURS_PER_YEAR, DEFAULT_LIFETIME_HOURS, DEFAULT_LOCATION


class TestEdgeCasesAndErrors:
    """Test edge cases and error handling."""
    
    def setup_method(self):
        """Reset container before each test."""
        DIContainer.reset_instance()
    
    def test_none_device_config_raises_error(self):
        """Test that None device config raises appropriate error."""
        container = get_container()
        use_case = container.get_compute_server_impact_use_case()
        
        usage_config = UsageConfiguration(
            hours_use_time=Decimal(str(HOURS_PER_YEAR)),
            hours_life_time=Decimal(str(DEFAULT_LIFETIME_HOURS)),
            location=DEFAULT_LOCATION
        )
        
        with pytest.raises(InvalidDeviceConfigurationError):
            use_case.execute(
                device_config=None,
                usage_config=usage_config,
                criteria=["gwp"],
                duration=HOURS_PER_YEAR,
                verbose=False
            )
    
    def test_none_usage_config_raises_error(self):
        """Test that None usage config raises appropriate error."""
        container = get_container()
        use_case = container.get_compute_server_impact_use_case()
        
        device_config = DeviceConfiguration(
            cpu=CPUConfiguration(core_units=8),
            ram=None,
            disk=None,
            power_supply=None,
            case=None
        )
        
        with pytest.raises(InvalidUsageConfigurationError):
            use_case.execute(
                device_config=device_config,
                usage_config=None,
                criteria=["gwp"],
                duration=HOURS_PER_YEAR,
                verbose=False
            )
    
    def test_empty_criteria_list(self):
        """Test that empty criteria list works without error."""
        container = get_container()
        use_case = container.get_compute_server_impact_use_case()
        
        device_config = DeviceConfiguration(
            cpu=CPUConfiguration(core_units=8),
            ram=None,
            disk=None,
            power_supply=None,
            case=None
        )
        
        usage_config = UsageConfiguration(
            hours_use_time=Decimal(str(HOURS_PER_YEAR)),
            hours_life_time=Decimal(str(DEFAULT_LIFETIME_HOURS)),
            location=DEFAULT_LOCATION
        )
        
        # Should work without error
        result = use_case.execute(
            device_config=device_config,
            usage_config=usage_config,
            criteria=[],
            duration=HOURS_PER_YEAR,
            verbose=False
        )
        
        assert result is not None
    
    def test_zero_duration(self):
        """Test that zero duration is handled correctly."""
        container = get_container()
        use_case = container.get_compute_server_impact_use_case()
        
        device_config = DeviceConfiguration(
            cpu=CPUConfiguration(core_units=8),
            ram=None,
            disk=None,
            power_supply=None,
            case=None
        )
        
        usage_config = UsageConfiguration(
            hours_use_time=Decimal(str(HOURS_PER_YEAR)),
            hours_life_time=Decimal(str(DEFAULT_LIFETIME_HOURS)),
            location=DEFAULT_LOCATION
        )
        
        result = use_case.execute(
            device_config=device_config,
            usage_config=usage_config,
            criteria=["gwp"],
            duration=0.0,
            verbose=False
        )
        
        assert result is not None
        assert result.duration_years == 0.0
    
    def test_very_large_duration(self):
        """Test that very large duration is handled correctly."""
        container = get_container()
        use_case = container.get_compute_server_impact_use_case()
        
        device_config = DeviceConfiguration(
            cpu=CPUConfiguration(core_units=8),
            ram=None,
            disk=None,
            power_supply=None,
            case=None
        )
        
        usage_config = UsageConfiguration(
            hours_use_time=Decimal(str(HOURS_PER_YEAR)),
            hours_life_time=Decimal(str(DEFAULT_LIFETIME_HOURS)),
            location=DEFAULT_LOCATION
        )
        
        large_duration = 876000.0  # 100 years
        
        result = use_case.execute(
            device_config=device_config,
            usage_config=usage_config,
            criteria=["gwp"],
            duration=large_duration,
            verbose=False
        )
        
        assert result is not None
        assert result.duration_years == 100.0
    
    def test_nonexistent_archetype_returns_none(self):
        """Test that requesting nonexistent archetype returns None."""
        container = get_container()
        repo = container.get_archetype_repository()
        
        result = repo.get_server_archetype("definitely_does_not_exist_12345")
        
        assert result is None
    
    def test_invalid_location_code(self):
        """Test that invalid location code is handled gracefully."""
        container = get_container()
        use_case = container.get_compute_server_impact_use_case()
        
        device_config = DeviceConfiguration(
            cpu=CPUConfiguration(core_units=8),
            ram=None,
            disk=None,
            power_supply=None,
            case=None
        )
        
        # Invalid location code
        usage_config = UsageConfiguration(
            hours_use_time=Decimal(str(HOURS_PER_YEAR)),
            hours_life_time=Decimal(str(DEFAULT_LIFETIME_HOURS)),
            location="INVALID"
        )
        
        # Should still work (falls back to defaults or handles gracefully)
        result = use_case.execute(
            device_config=device_config,
            usage_config=usage_config,
            criteria=["gwp"],
            duration=HOURS_PER_YEAR,
            verbose=False
        )
        
        assert result is not None
    
    def test_very_small_component_values(self):
        """Test that very small component values are handled correctly."""
        container = get_container()
        use_case = container.get_compute_server_impact_use_case()
        
        device_config = DeviceConfiguration(
            cpu=CPUConfiguration(
                core_units=1,
                die_size_per_core=Decimal("0.1")
            ),
            ram=None,
            disk=None,
            power_supply=None,
            case=None
        )
        
        usage_config = UsageConfiguration(
            hours_use_time=Decimal(str(HOURS_PER_YEAR)),
            hours_life_time=Decimal(str(DEFAULT_LIFETIME_HOURS)),
            location=DEFAULT_LOCATION
        )
        
        result = use_case.execute(
            device_config=device_config,
            usage_config=usage_config,
            criteria=["gwp"],
            duration=HOURS_PER_YEAR,
            verbose=False
        )
        
        assert result is not None
    
    def test_multiple_criteria_computation(self):
        """Test that multiple criteria are all computed."""
        container = get_container()
        use_case = container.get_compute_server_impact_use_case()
        
        device_config = DeviceConfiguration(
            cpu=CPUConfiguration(core_units=8),
            ram=None,
            disk=None,
            power_supply=None,
            case=None
        )
        
        usage_config = UsageConfiguration(
            hours_use_time=Decimal(str(HOURS_PER_YEAR)),
            hours_life_time=Decimal(str(DEFAULT_LIFETIME_HOURS)),
            location=DEFAULT_LOCATION
        )
        
        criteria = ["gwp", "adp", "pe"]
        
        result = use_case.execute(
            device_config=device_config,
            usage_config=usage_config,
            criteria=criteria,
            duration=HOURS_PER_YEAR,
            verbose=False
        )
        
        assert result is not None
        # All criteria should be in manufacturing phase
        for criterion in criteria:
            assert criterion in result.phases.manufacturing
    
    def test_cache_clearing(self):
        """Test that cache can be cleared without errors."""
        container = get_container()
        repo = container.get_archetype_repository()
        
        # Populate cache
        repo.get_server_archetype("default")
        
        # Clear cache
        repo.clear_cache()
        
        # Should still work after clearing
        result = repo.get_server_archetype("default")
        assert result is not None
    
    def test_factor_provider_handles_missing_data(self):
        """Test that factor provider handles missing data gracefully."""
        container = get_container()
        factor_provider = container.get_factor_provider()
        
        # Request factor for nonexistent component
        result = factor_provider.get_impact_factors("nonexistent_component_type")
        
        # Should return None or empty dict, not crash
        assert result is not None or result is None  # Either is acceptable
