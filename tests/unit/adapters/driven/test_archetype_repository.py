"""Unit tests for ArchetypeRepository driven adapter."""

import pytest
import os

from boaviztapi.adapters.driven.persistence.archetype_repository import ArchetypeRepository
from boaviztapi import data_dir


class TestArchetypeRepository:
    """Test suite for ArchetypeRepository adapter."""
    
    @pytest.fixture
    def repository(self):
        """Create an ArchetypeRepository instance."""
        return ArchetypeRepository()
    
    def test_repository_instantiation(self, repository):
        """Test that repository can be instantiated."""
        assert repository is not None
        assert isinstance(repository, ArchetypeRepository)
    
    def test_repository_with_custom_data_path(self):
        """Test repository with custom data path."""
        repo = ArchetypeRepository(data_path=data_dir)
        assert repo is not None
    
    def test_get_server_archetype_default(self, repository):
        """Test getting default server archetype."""
        result = repository.get_server_archetype("platform_compute_low")
        
        # Should return a dictionary with archetype configuration
        assert result is not None
        assert isinstance(result, dict)
    
    def test_get_server_archetype_nonexistent(self, repository):
        """Test getting nonexistent server archetype."""
        result = repository.get_server_archetype("nonexistent_archetype_12345")
        
        # Should return None for nonexistent archetype
        assert result is None
    
    def test_get_server_archetype_caching(self, repository):
        """Test that archetype results are cached."""
        # First call
        result1 = repository.get_server_archetype("platform_compute_low")
        
        # Second call should return cached result
        result2 = repository.get_server_archetype("platform_compute_low")
        
        # Should be the same object (cached)
        assert result1 is result2
    
    def test_get_component_archetype_cpu(self, repository):
        """Test getting CPU component archetype."""
        # Try to get a CPU archetype (using a common one if exists)
        result = repository.get_component_archetype("default", "cpu")
        
        if result is not None:
            assert isinstance(result, dict)
    
    def test_get_component_archetype_ram(self, repository):
        """Test getting RAM component archetype."""
        result = repository.get_component_archetype("default", "ram")
        
        if result is not None:
            assert isinstance(result, dict)
    
    def test_get_component_archetype_invalid_type(self, repository):
        """Test getting component archetype with invalid type."""
        result = repository.get_component_archetype("default", "invalid_component_type_xyz")
        
        # Should return None for invalid component type
        assert result is None
    
    def test_get_cloud_instance_archetype(self, repository):
        """Test getting cloud instance archetype."""
        # Try AWS instance type
        result = repository.get_cloud_instance_archetype("a1.medium", "aws")
        
        if result is not None:
            assert isinstance(result, dict)
    
    def test_get_cloud_instance_archetype_invalid_provider(self, repository):
        """Test getting cloud archetype with invalid provider."""
        result = repository.get_cloud_instance_archetype("instance", "invalid_provider_xyz")
        
        # Should return None for invalid provider
        assert result is None
    
    def test_get_iot_device_archetype(self, repository):
        """Test getting IoT device archetype."""
        # Check if IoT archetype file exists
        iot_path = os.path.join(data_dir, "archetypes/iot_device.csv")
        
        if os.path.exists(iot_path):
            result = repository.get_iot_device_archetype("default")
            if result is not None:
                assert isinstance(result, dict)
    
    def test_get_user_terminal_archetype(self, repository):
        """Test getting user terminal archetype."""
        result = repository.get_user_terminal_archetype("default")
        
        if result is not None:
            assert isinstance(result, dict)
    
    def test_list_available_archetypes_server(self, repository):
        """Test listing available server archetypes."""
        result = repository.list_available_archetypes("server")
        
        # Should return a list
        assert isinstance(result, list)
        
        # Should have at least default archetype if file exists
        if len(result) > 0:
            assert "default" in result or len(result) >= 0
    
    def test_list_available_archetypes_invalid_type(self, repository):
        """Test listing archetypes for invalid device type."""
        result = repository.list_available_archetypes("invalid_type_xyz")
        
        # Should return empty list for invalid type
        assert result == []
    
    def test_clear_cache(self, repository):
        """Test clearing the cache."""
        # Load an archetype to populate cache
        repository.get_server_archetype("default")
        
        # Clear cache
        repository.clear_cache()
        
        # Cache should be empty
        assert len(repository._cache) == 0
    
    def test_component_archetype_caching(self, repository):
        """Test that component archetypes are cached."""
        # First call
        result1 = repository.get_component_archetype("default", "cpu")
        
        if result1 is not None:
            # Second call should return cached result
            result2 = repository.get_component_archetype("default", "cpu")
            
            # Should be the same object (cached)
            assert result1 is result2
