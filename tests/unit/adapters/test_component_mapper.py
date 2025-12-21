"""
Unit tests for ComponentMapper.
"""
import pytest
from decimal import Decimal
from boaviztapi.adapters.driving.rest.mappers.component_mapper import ComponentMapper
from boaviztapi.adapters.driving.rest.schemas.component import (
    ComponentCPURequestSchema,
    ComponentRAMRequestSchema,
    ComponentSSDRequestSchema
)
from boaviztapi.adapters.driving.rest.schemas.common import UsageSchema


class TestComponentMapper:
    """Test suite for ComponentMapper."""
    
    def test_to_cpu_configuration_complete(self):
        """Test converting complete CPU component request to domain model."""
        request = ComponentCPURequestSchema(
            units=1,
            core_units=12,
            die_size_per_core=24.5,
            name="Intel Core i7",
            tdp=95.0,
            manufacturer="Intel",
            family="Core"
        )
        
        cpu_config = ComponentMapper.to_cpu_configuration(request)
        
        assert cpu_config is not None
        assert cpu_config.core_units == 12
        assert cpu_config.die_size_per_core == Decimal("24.5")
        assert cpu_config.name == "Intel Core i7"
        assert cpu_config.tdp == Decimal("95.0")
        assert cpu_config.manufacturer == "Intel"
        assert cpu_config.family == "Core"
    
    def test_to_cpu_configuration_minimal(self):
        """Test converting minimal CPU component request (as in existing tests)."""
        request = ComponentCPURequestSchema(
            core_units=12,
            die_size_per_core=24.5
        )
        
        cpu_config = ComponentMapper.to_cpu_configuration(request)
        
        assert cpu_config is not None
        assert cpu_config.core_units == 12
        assert cpu_config.die_size_per_core == Decimal("24.5")
        assert cpu_config.name is None
        assert cpu_config.tdp is None
    
    def test_to_ram_configuration_complete(self):
        """Test converting complete RAM component request to domain model."""
        request = ComponentRAMRequestSchema(
            units=8,
            capacity=16.0,
            density=2.0,
            manufacturer="Samsung"
        )
        
        ram_config = ComponentMapper.to_ram_configuration(request)
        
        assert ram_config is not None
        assert ram_config.capacity_gb == Decimal("16.0")
        assert ram_config.density == Decimal("2.0")
        assert ram_config.manufacturer == "Samsung"
    
    def test_to_ram_configuration_minimal(self):
        """Test converting minimal RAM component request."""
        request = ComponentRAMRequestSchema(
            capacity=8.0
        )
        
        ram_config = ComponentMapper.to_ram_configuration(request)
        
        assert ram_config is not None
        assert ram_config.capacity_gb == Decimal("8.0")
        assert ram_config.density is None
        assert ram_config.manufacturer is None
    
    def test_to_ssd_configuration_complete(self):
        """Test converting complete SSD component request to domain model."""
        request = ComponentSSDRequestSchema(
            units=2,
            capacity=500.0,
            density=50.0,
            manufacturer="Samsung"
        )
        
        ssd_config = ComponentMapper.to_ssd_configuration(request)
        
        assert ssd_config is not None
        assert ssd_config.type == "ssd"
        assert ssd_config.capacity_gb == Decimal("500.0")
        assert ssd_config.manufacturer == "Samsung"
    
    def test_to_ssd_configuration_minimal(self):
        """Test converting minimal SSD component request."""
        request = ComponentSSDRequestSchema(
            capacity=256.0
        )
        
        ssd_config = ComponentMapper.to_ssd_configuration(request)
        
        assert ssd_config is not None
        assert ssd_config.type == "ssd"
        assert ssd_config.capacity_gb == Decimal("256.0")
        assert ssd_config.manufacturer is None
    
    def test_to_usage_configuration_complete(self):
        """Test converting complete usage schema to domain model."""
        usage_schema = UsageSchema(
            usage_location="FRA",
            hours_life_time=26280.0,
            time_workload=50.0,
            workload={"idle": 10.0, "50%": 50.0, "100%": 40.0}
        )
        
        usage_config = ComponentMapper.to_usage_configuration(usage_schema)
        
        assert usage_config is not None
        assert usage_config.location == "FRA"
        assert usage_config.hours_life_time == Decimal("26280.0")
        assert usage_config.workload is not None
        assert usage_config.workload["idle"] == Decimal("10.0")
    
    def test_to_usage_configuration_minimal(self):
        """Test converting minimal usage schema."""
        usage_schema = UsageSchema(
            usage_location="USA"
        )
        
        usage_config = ComponentMapper.to_usage_configuration(usage_schema)
        
        assert usage_config is not None
        assert usage_config.location == "USA"
        assert usage_config.hours_life_time is None
        assert usage_config.workload is None
    
    def test_to_usage_configuration_none(self):
        """Test converting None usage schema."""
        usage_config = ComponentMapper.to_usage_configuration(None)
        
        assert usage_config is not None
        assert usage_config.location is None
        assert usage_config.hours_life_time is None
        assert usage_config.workload is None
