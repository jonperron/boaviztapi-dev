"""Integration tests for Phase 7 - comprehensive hexagonal architecture validation.

These tests validate the complete flow from API to domain to data access,
ensuring all components work together correctly with proper config usage.
"""

import pytest
from decimal import Decimal
from boaviztapi.core.di_container import DIContainer, get_container
from boaviztapi.core.domain.model.device import DeviceConfiguration, CPUConfiguration, RAMConfiguration, DiskConfiguration
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.core.config_constants import (
    HOURS_PER_YEAR,
    DEFAULT_LIFETIME_HOURS,
    DEFAULT_LOCATION,
    DEFAULT_SERVER,
    DEFAULT_CRITERIA,
    DEFAULT_WORKLOAD_PERCENTAGE,
)


class TestPhase7Integration:
    """Integration tests for Phase 7 comprehensive validation."""
    
    def setup_method(self):
        """Reset container before each test."""
        DIContainer.reset_instance()
    
    def test_config_constants_loaded(self):
        """Test that config constants are properly loaded from config file."""
        assert HOURS_PER_YEAR == 8760.0
        assert DEFAULT_LIFETIME_HOURS == 35040.0
        assert DEFAULT_LOCATION == "EEE"
        # DEFAULT_SERVER might be "DEFAULT" in test data
        assert DEFAULT_SERVER in ["platform_compute_medium", "DEFAULT"]
        assert DEFAULT_CRITERIA == ["gwp", "adp", "pe"]
    
    def test_complete_server_impact_flow_with_config_defaults(self):
        """Test complete server impact computation using config defaults."""
        container = get_container()
        use_case = container.get_compute_server_impact_use_case()
        
        # Create server config with all components
        cpu_config = CPUConfiguration(
            core_units=24,
            die_size_per_core=Decimal("25.0"),
            name="Intel Xeon Gold 6248R"
        )
        
        ram_configs = [
            RAMConfiguration(capacity_gb=Decimal("32")),
            RAMConfiguration(capacity_gb=Decimal("32")),
        ]
        
        disk_config = DiskConfiguration(
            type="ssd",
            capacity_gb=Decimal("1000")
        )
        
        device_config = DeviceConfiguration(
            cpu=cpu_config,
            ram=ram_configs,
            disk=[disk_config],
            power_supply=None,
            case=None
        )
        
        # Use config defaults for usage
        usage_config = UsageConfiguration(
            hours_use_time=Decimal(str(HOURS_PER_YEAR)),
            hours_life_time=Decimal(str(DEFAULT_LIFETIME_HOURS)),
            location=DEFAULT_LOCATION
        )
        
        # Execute with config defaults
        result = use_case.execute(
            device_config=device_config,
            usage_config=usage_config,
            criteria=DEFAULT_CRITERIA,
            duration=None,  # Should use default (HOURS_PER_YEAR)
            verbose=True
        )
        
        # Validate results
        assert result is not None
        assert result.phases is not None
        assert result.phases.manufacturing is not None
        assert all(criteria in result.phases.manufacturing for criteria in DEFAULT_CRITERIA)
        # When duration is None, it defaults to HOURS_PER_YEAR (1 year)
        assert result.duration_years == 1.0
    
    def test_archetype_repository_uses_config_defaults(self):
        """Test that archetype repository correctly maps 'default' to config value."""
        container = get_container()
        repo = container.get_archetype_repository()
        
        # Request "default" archetype
        default_archetype = repo.get_server_archetype("default")
        
        # Should map to DEFAULT_SERVER from config
        specific_archetype = repo.get_server_archetype(DEFAULT_SERVER)
        
        assert default_archetype is not None
        assert specific_archetype is not None
        # They should be the same (from cache)
        assert default_archetype == specific_archetype
    
    def test_minimal_config_with_defaults(self):
        """Test that minimal config works with all defaults from config."""
        container = get_container()
        use_case = container.get_compute_server_impact_use_case()
        
        # Minimal device config - only CPU
        device_config = DeviceConfiguration(
            cpu=CPUConfiguration(core_units=8),
            ram=None,
            disk=None,
            power_supply=None,
            case=None
        )
        
        # Minimal usage config using defaults
        usage_config = UsageConfiguration(
            hours_use_time=Decimal(str(HOURS_PER_YEAR)),
            hours_life_time=Decimal(str(DEFAULT_LIFETIME_HOURS)),
            location=DEFAULT_LOCATION
        )
        
        result = use_case.execute(
            device_config=device_config,
            usage_config=usage_config,
            criteria=DEFAULT_CRITERIA,
            duration=HOURS_PER_YEAR,
            verbose=False
        )
        
        assert result is not None
        assert result.phases is not None
    
    def test_custom_duration_overrides_default(self):
        """Test that custom duration overrides config default."""
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
        
        custom_duration = 17520.0  # 2 years
        
        result = use_case.execute(
            device_config=device_config,
            usage_config=usage_config,
            criteria=DEFAULT_CRITERIA,
            duration=custom_duration,
            verbose=False
        )
        
        assert result.duration_years == custom_duration / HOURS_PER_YEAR
        assert result.duration_years == 2.0
    
    def test_custom_location_overrides_default(self):
        """Test that custom location overrides config default."""
        container = get_container()
        use_case = container.get_compute_server_impact_use_case()
        
        device_config = DeviceConfiguration(
            cpu=CPUConfiguration(core_units=8),
            ram=None,
            disk=None,
            power_supply=None,
            case=None
        )
        
        custom_location = "FRA"
        usage_config = UsageConfiguration(
            hours_use_time=Decimal(str(HOURS_PER_YEAR)),
            hours_life_time=Decimal(str(DEFAULT_LIFETIME_HOURS)),
            location=custom_location
        )
        
        # Should work without error (location is used in use phase calculation)
        result = use_case.execute(
            device_config=device_config,
            usage_config=usage_config,
            criteria=DEFAULT_CRITERIA,
            duration=HOURS_PER_YEAR,
            verbose=False
        )
        
        assert result is not None
    
    def test_verbose_mode_includes_config_based_data(self):
        """Test that verbose mode includes data based on config values."""
        container = get_container()
        use_case = container.get_compute_server_impact_use_case()
        
        device_config = DeviceConfiguration(
            cpu=CPUConfiguration(core_units=16),
            ram=[RAMConfiguration(capacity_gb=Decimal("64"))],
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
            criteria=DEFAULT_CRITERIA,
            duration=HOURS_PER_YEAR,
            verbose=True
        )
        
        assert result.verbose_data is not None
        assert isinstance(result.verbose_data, dict)
    
    def test_all_criteria_from_config(self):
        """Test that all criteria from config are computed."""
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
            criteria=DEFAULT_CRITERIA,
            duration=HOURS_PER_YEAR,
            verbose=False
        )
        
        # All default criteria should be present in manufacturing phase
        assert result.phases.manufacturing is not None
        for criteria in DEFAULT_CRITERIA:
            assert criteria in result.phases.manufacturing
