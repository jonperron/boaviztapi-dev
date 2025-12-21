"""Integration tests for Phase 6 hexagonal architecture wire-up.

These tests verify that the DI container and router integration work correctly.
"""

import pytest
from boaviztapi.core.di_container import DIContainer, get_container
from boaviztapi.core.use_cases.compute_server_impact import ComputeServerImpactUseCase
from boaviztapi.adapters.driven.persistence.archetype_repository import ArchetypeRepository
from boaviztapi.adapters.driven.persistence.factor_provider import FactorProvider


class TestDIContainer:
    """Tests for the DI container."""
    
    def setup_method(self):
        """Reset the container before each test."""
        DIContainer.reset_instance()
    
    def test_container_singleton(self):
        """Test that container follows singleton pattern."""
        container1 = get_container()
        container2 = get_container()
        
        assert container1 is container2
    
    def test_container_provides_use_case(self):
        """Test that container provides compute server impact use case."""
        container = get_container()
        use_case = container.get_compute_server_impact_use_case()
        
        assert isinstance(use_case, ComputeServerImpactUseCase)
    
    def test_container_provides_repositories(self):
        """Test that container provides repository instances."""
        container = get_container()
        archetype_repo = container.get_archetype_repository()
        factor_provider = container.get_factor_provider()
        
        assert isinstance(archetype_repo, ArchetypeRepository)
        assert isinstance(factor_provider, FactorProvider)
    
    def test_use_case_can_execute(self):
        """Test that use case obtained from container can execute."""
        from boaviztapi.core.domain.model.device import DeviceConfiguration
        from boaviztapi.core.domain.model.usage import UsageConfiguration
        
        container = get_container()
        use_case = container.get_compute_server_impact_use_case()
        
        # Create minimal config
        device_config = DeviceConfiguration(
            cpu=None,
            ram=None,
            disk=None,
            power_supply=None,
            case=None
        )
        
        from decimal import Decimal
        
        usage_config = UsageConfiguration(
            hours_use_time=Decimal("8760.0"),
            hours_life_time=Decimal("35040.0"),
            location="EEE"
        )
        
        # Execute use case
        result = use_case.execute(
            device_config=device_config,
            usage_config=usage_config,
            criteria=["gwp", "pe", "adp"],
            duration=8760.0,
            verbose=False
        )
        
        # Verify result structure
        assert result is not None
        assert result.phases is not None
        assert result.phases.manufacturing is not None
        assert "gwp" in result.phases.manufacturing
    
    def test_container_reset(self):
        """Test that container can be reset."""
        container1 = get_container()
        DIContainer.reset_instance()
        container2 = get_container()
        
        assert container1 is not container2
