"""Unit tests for ComputeCloudImpactUseCase."""

import pytest
from unittest.mock import Mock
from decimal import Decimal

from boaviztapi.core.use_cases.compute_cloud_impact import ComputeCloudImpactUseCase
from boaviztapi.core.domain.model.device import CloudInstanceConfiguration
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.core.domain.model.impact import ImpactResult
from boaviztapi.core.domain.exceptions import (
    InvalidDeviceConfigurationError,
    InvalidUsageConfigurationError,
)


class TestComputeCloudImpactUseCase:
    """Test suite for ComputeCloudImpactUseCase."""
    
    @pytest.fixture
    def mock_archetype_repo(self):
        """Create a mock archetype repository."""
        repo = Mock()
        repo.get_cloud_instance_archetype.return_value = {
            "vcpu": 2,
            "memory": 4,
            "storage": 50
        }
        return repo
    
    @pytest.fixture
    def mock_factor_provider(self):
        """Create a mock factor provider."""
        provider = Mock()
        provider.get_impact_factors.return_value = {
            "gwp": {"value": 0.5}
        }
        return provider
    
    @pytest.fixture
    def use_case(self, mock_archetype_repo, mock_factor_provider):
        """Create a use case instance with mocked dependencies."""
        return ComputeCloudImpactUseCase(
            archetype_repository=mock_archetype_repo,
            factor_provider=mock_factor_provider
        )
    
    @pytest.fixture
    def valid_instance_config(self):
        """Create a valid cloud instance configuration."""
        return CloudInstanceConfiguration(
            instance_type="t2.medium",
            provider="aws",
            region="us-east-1"
        )
    
    @pytest.fixture
    def valid_usage_config(self):
        """Create a valid usage configuration."""
        return UsageConfiguration(
            location="US",
            instances_number=1,
            usage_time_ratio=Decimal('0.8')
        )
    
    def test_execute_returns_impact_result(
        self, use_case, valid_instance_config, valid_usage_config
    ):
        """Test that execute returns an ImpactResult."""
        result = use_case.execute(
            instance_config=valid_instance_config,
            usage_config=valid_usage_config,
            criteria=["gwp"],
            duration=8760.0,
            verbose=False
        )
        
        assert isinstance(result, ImpactResult)
        assert result.duration_years == 1.0
    
    def test_execute_raises_error_for_none_instance_config(
        self, use_case, valid_usage_config
    ):
        """Test that None instance config raises error."""
        with pytest.raises(InvalidDeviceConfigurationError) as exc_info:
            use_case.execute(
                instance_config=None,
                usage_config=valid_usage_config,
                criteria=["gwp"],
                duration=8760.0,
                verbose=False
            )
        
        assert "Instance configuration is required" in str(exc_info.value)
    
    def test_execute_raises_error_for_missing_instance_type(
        self, use_case, valid_usage_config
    ):
        """Test that missing instance type raises error."""
        invalid_config = CloudInstanceConfiguration(
            instance_type="",
            provider="aws"
        )
        
        with pytest.raises(InvalidDeviceConfigurationError) as exc_info:
            use_case.execute(
                instance_config=invalid_config,
                usage_config=valid_usage_config,
                criteria=["gwp"],
                duration=8760.0,
                verbose=False
            )
        
        assert "Instance type is required" in str(exc_info.value)
    
    def test_execute_raises_error_for_missing_provider(
        self, use_case, valid_usage_config
    ):
        """Test that missing provider raises error."""
        invalid_config = CloudInstanceConfiguration(
            instance_type="t2.medium",
            provider=""
        )
        
        with pytest.raises(InvalidDeviceConfigurationError) as exc_info:
            use_case.execute(
                instance_config=invalid_config,
                usage_config=valid_usage_config,
                criteria=["gwp"],
                duration=8760.0,
                verbose=False
            )
        
        assert "Provider is required" in str(exc_info.value)
    
    def test_execute_raises_error_for_none_usage_config(
        self, use_case, valid_instance_config
    ):
        """Test that None usage config raises error."""
        with pytest.raises(InvalidUsageConfigurationError) as exc_info:
            use_case.execute(
                instance_config=valid_instance_config,
                usage_config=None,
                criteria=["gwp"],
                duration=8760.0,
                verbose=False
            )
        
        assert "Usage configuration is required" in str(exc_info.value)