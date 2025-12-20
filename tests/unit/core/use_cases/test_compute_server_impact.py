"""Unit tests for ComputeServerImpactUseCase.

These tests verify the use case logic in isolation by mocking output ports.
"""

import pytest
from unittest.mock import Mock
from decimal import Decimal

from boaviztapi.core.use_cases.compute_server_impact import ComputeServerImpactUseCase
from boaviztapi.core.domain.model.device import (
    DeviceConfiguration,
    CPUConfiguration,
    RAMConfiguration,
)
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.core.domain.model.impact import ImpactResult
from boaviztapi.core.domain.exceptions import (
    InvalidDeviceConfigurationError,
    InvalidUsageConfigurationError,
)


class TestComputeServerImpactUseCase:
    """Test suite for ComputeServerImpactUseCase."""
    
    @pytest.fixture
    def mock_archetype_repo(self):
        """Create a mock archetype repository."""
        repo = Mock()
        repo.get_server_archetype.return_value = {
            "cpu": {"units": 1, "tdp": 120},
            "ram": {"capacity": 32, "units": 4}
        }
        return repo
    
    @pytest.fixture
    def mock_factor_provider(self):
        """Create a mock factor provider."""
        provider = Mock()
        provider.get_impact_factors.return_value = {
            "gwp": {"value": 0.38, "min": 0.30, "max": 0.45},
            "pe": {"value": 3.5, "min": 3.0, "max": 4.0}
        }
        provider.get_electrical_mix.return_value = {
            "carbon_intensity": 0.38
        }
        return provider
    
    @pytest.fixture
    def use_case(self, mock_archetype_repo, mock_factor_provider):
        """Create a use case instance with mocked dependencies."""
        return ComputeServerImpactUseCase(
            archetype_repository=mock_archetype_repo,
            factor_provider=mock_factor_provider
        )
    
    @pytest.fixture
    def valid_device_config(self):
        """Create a valid device configuration."""
        return DeviceConfiguration(
            cpu=CPUConfiguration(
                core_units=4,
                tdp=Decimal('120')
            ),
            ram=[
                RAMConfiguration(capacity_gb=Decimal('16')),
                RAMConfiguration(capacity_gb=Decimal('16'))
            ]
        )
    
    @pytest.fixture
    def valid_usage_config(self):
        """Create a valid usage configuration."""
        return UsageConfiguration(
            location="FR",
            hours_life_time=Decimal('35040'),  # 4 years
            usage_time_ratio=Decimal('0.5')
        )
    
    def test_execute_returns_impact_result(
        self, use_case, valid_device_config, valid_usage_config
    ):
        """Test that execute returns an ImpactResult."""
        result = use_case.execute(
            device_config=valid_device_config,
            usage_config=valid_usage_config,
            criteria=["gwp", "pe"],
            duration=8760.0,
            verbose=False
        )
        
        assert isinstance(result, ImpactResult)
        assert result is not None
        assert result.duration_years == 1.0
    
    def test_execute_with_verbose(
        self, use_case, valid_device_config, valid_usage_config
    ):
        """Test that verbose mode includes verbose data."""
        result = use_case.execute(
            device_config=valid_device_config,
            usage_config=valid_usage_config,
            criteria=["gwp"],
            duration=8760.0,
            verbose=True
        )
        
        # Verbose data should be present (even if empty for stub)
        assert result.verbose_data is not None
    
    def test_execute_without_verbose(
        self, use_case, valid_device_config, valid_usage_config
    ):
        """Test that non-verbose mode excludes verbose data."""
        result = use_case.execute(
            device_config=valid_device_config,
            usage_config=valid_usage_config,
            criteria=["gwp"],
            duration=8760.0,
            verbose=False
        )
        
        assert result.verbose_data is None
    
    def test_execute_with_default_duration(
        self, use_case, valid_device_config, valid_usage_config
    ):
        """Test that default duration is used when not provided."""
        result = use_case.execute(
            device_config=valid_device_config,
            usage_config=valid_usage_config,
            criteria=["gwp"],
            duration=None,
            verbose=False
        )
        
        # Default duration is 8760 hours (1 year)
        assert result.duration_years == 1.0
    
    def test_execute_with_custom_duration(
        self, use_case, valid_device_config, valid_usage_config
    ):
        """Test that custom duration is respected."""
        result = use_case.execute(
            device_config=valid_device_config,
            usage_config=valid_usage_config,
            criteria=["gwp"],
            duration=17520.0,  # 2 years
            verbose=False
        )
        
        assert result.duration_years == 2.0
    
    def test_execute_raises_error_for_none_device_config(
        self, use_case, valid_usage_config
    ):
        """Test that None device config raises InvalidDeviceConfigurationError."""
        with pytest.raises(InvalidDeviceConfigurationError) as exc_info:
            use_case.execute(
                device_config=None,
                usage_config=valid_usage_config,
                criteria=["gwp"],
                duration=8760.0,
                verbose=False
            )
        
        assert "Device configuration is required" in str(exc_info.value)
    
    def test_execute_raises_error_for_none_usage_config(
        self, use_case, valid_device_config
    ):
        """Test that None usage config raises InvalidUsageConfigurationError."""
        with pytest.raises(InvalidUsageConfigurationError) as exc_info:
            use_case.execute(
                device_config=valid_device_config,
                usage_config=None,
                criteria=["gwp"],
                duration=8760.0,
                verbose=False
            )
        
        assert "Usage configuration is required" in str(exc_info.value)
    
    def test_execute_with_multiple_criteria(
        self, use_case, valid_device_config, valid_usage_config
    ):
        """Test execution with multiple impact criteria."""
        result = use_case.execute(
            device_config=valid_device_config,
            usage_config=valid_usage_config,
            criteria=["gwp", "pe", "adp"],
            duration=8760.0,
            verbose=False
        )
        
        assert isinstance(result, ImpactResult)
    
    def test_use_case_uses_injected_dependencies(
        self, mock_archetype_repo, mock_factor_provider, valid_device_config, valid_usage_config
    ):
        """Test that use case properly uses injected dependencies."""
        use_case = ComputeServerImpactUseCase(
            archetype_repository=mock_archetype_repo,
            factor_provider=mock_factor_provider
        )
        
        result = use_case.execute(
            device_config=valid_device_config,
            usage_config=valid_usage_config,
            criteria=["gwp"],
            duration=8760.0,
            verbose=False
        )
        
        # Verify dependencies were properly stored
        assert use_case._archetype_repo is mock_archetype_repo
        assert use_case._factor_provider is mock_factor_provider