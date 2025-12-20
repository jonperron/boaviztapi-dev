"""Unit tests for ComputeComponentImpactUseCase."""

import pytest
from unittest.mock import Mock

from boaviztapi.core.use_cases.compute_component_impact import ComputeComponentImpactUseCase
from boaviztapi.core.domain.model.device import ComponentConfiguration
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.core.domain.model.impact import ImpactResult
from boaviztapi.core.domain.exceptions import (
    InvalidComponentConfigurationError,
    InvalidUsageConfigurationError,
)


class TestComputeComponentImpactUseCase:
    """Test suite for ComputeComponentImpactUseCase."""
    
    @pytest.fixture
    def mock_archetype_repo(self):
        """Create a mock archetype repository."""
        repo = Mock()
        repo.get_component_archetype.return_value = {
            "tdp": 95,
            "die_size": 250
        }
        return repo
    
    @pytest.fixture
    def mock_factor_provider(self):
        """Create a mock factor provider."""
        provider = Mock()
        provider.get_impact_factors.return_value = {
            "gwp": {"value": 1.2}
        }
        return provider
    
    @pytest.fixture
    def use_case(self, mock_archetype_repo, mock_factor_provider):
        """Create a use case instance with mocked dependencies."""
        return ComputeComponentImpactUseCase(
            archetype_repository=mock_archetype_repo,
            factor_provider=mock_factor_provider
        )
    
    @pytest.fixture
    def valid_component_config(self):
        """Create a valid component configuration."""
        return ComponentConfiguration(
            component_type="cpu",
            configuration={
                "name": "Intel Core i7",
                "tdp": 95,
                "cores": 8
            }
        )
    
    @pytest.fixture
    def valid_usage_config(self):
        """Create a valid usage configuration."""
        return UsageConfiguration(
            location="FR"
        )
    
    def test_execute_returns_impact_result(
        self, use_case, valid_component_config, valid_usage_config
    ):
        """Test that execute returns an ImpactResult."""
        result = use_case.execute(
            component_config=valid_component_config,
            usage_config=valid_usage_config,
            criteria=["gwp"],
            duration=8760.0,
            verbose=False
        )
        
        assert isinstance(result, ImpactResult)
        assert result.duration_years == 1.0
    
    def test_execute_raises_error_for_none_component_config(
        self, use_case, valid_usage_config
    ):
        """Test that None component config raises error."""
        with pytest.raises(InvalidComponentConfigurationError) as exc_info:
            use_case.execute(
                component_config=None,
                usage_config=valid_usage_config,
                criteria=["gwp"],
                duration=8760.0,
                verbose=False
            )
        
        assert "Component configuration is required" in str(exc_info.value)
    
    def test_execute_raises_error_for_missing_component_type(
        self, use_case, valid_usage_config
    ):
        """Test that missing component type raises error."""
        invalid_config = ComponentConfiguration(
            component_type="",
            configuration={}
        )
        
        with pytest.raises(InvalidComponentConfigurationError) as exc_info:
            use_case.execute(
                component_config=invalid_config,
                usage_config=valid_usage_config,
                criteria=["gwp"],
                duration=8760.0,
                verbose=False
            )
        
        assert "Component type is required" in str(exc_info.value)
    
    def test_execute_raises_error_for_none_usage_config(
        self, use_case, valid_component_config
    ):
        """Test that None usage config raises error."""
        with pytest.raises(InvalidUsageConfigurationError) as exc_info:
            use_case.execute(
                component_config=valid_component_config,
                usage_config=None,
                criteria=["gwp"],
                duration=8760.0,
                verbose=False
            )
        
        assert "Usage configuration is required" in str(exc_info.value)
    
    def test_execute_with_different_component_types(
        self, use_case, valid_usage_config
    ):
        """Test execution with different component types."""
        component_types = ["cpu", "ram", "ssd", "hdd"]
        
        for comp_type in component_types:
            config = ComponentConfiguration(
                component_type=comp_type,
                configuration={"capacity": 500}
            )
            
            result = use_case.execute(
                component_config=config,
                usage_config=valid_usage_config,
                criteria=["gwp"],
                duration=8760.0,
                verbose=False
            )
            
            assert isinstance(result, ImpactResult)