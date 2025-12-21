"""
Unit tests for ServerMapper.
"""
import pytest
from decimal import Decimal
from boaviztapi.adapters.driving.rest.mappers.server_mapper import ServerMapper
from boaviztapi.adapters.driving.rest.schemas.server import (
    ServerRequestSchema,
    ServerConfigurationSchema,
    CPUSchema,
    RAMSchema,
    DiskSchema,
    PowerSupplySchema,
    MotherboardSchema,
    AssemblySchema,
    CaseSchema
)
from boaviztapi.adapters.driving.rest.schemas.common import UsageSchema


class TestServerMapper:
    """Test suite for ServerMapper."""
    
    def test_to_cpu_configuration_complete(self):
        """Test converting complete CPU schema to domain model."""
        cpu_schema = CPUSchema(
            units=2,
            core_units=24,
            die_size_per_core=24.5,
            name="Intel Xeon Gold",
            tdp=150.0,
            manufacturer="Intel",
            family="Xeon"
        )
        
        cpu_config = ServerMapper.to_cpu_configuration(cpu_schema)
        
        assert cpu_config is not None
        assert cpu_config.core_units == 24
        assert cpu_config.die_size_per_core == Decimal("24.5")
        assert cpu_config.name == "Intel Xeon Gold"
        assert cpu_config.tdp == Decimal("150.0")
        assert cpu_config.manufacturer == "Intel"
        assert cpu_config.family == "Xeon"
    
    def test_to_cpu_configuration_minimal(self):
        """Test converting minimal CPU schema to domain model."""
        cpu_schema = CPUSchema(
            core_units=12,
            die_size_per_core=24.5
        )
        
        cpu_config = ServerMapper.to_cpu_configuration(cpu_schema)
        
        assert cpu_config is not None
        assert cpu_config.core_units == 12
        assert cpu_config.die_size_per_core == Decimal("24.5")
        assert cpu_config.name is None
    
    def test_to_cpu_configuration_none(self):
        """Test converting None CPU schema."""
        cpu_config = ServerMapper.to_cpu_configuration(None)
        assert cpu_config is None
    
    def test_to_ram_configurations_multiple(self):
        """Test converting multiple RAM schemas to domain models."""
        ram_schemas = [
            RAMSchema(units=4, capacity=32, density=1.79),
            RAMSchema(units=4, capacity=16, density=1.79)
        ]
        
        ram_configs = ServerMapper.to_ram_configurations(ram_schemas)
        
        assert ram_configs is not None
        assert len(ram_configs) == 2
        assert ram_configs[0].capacity_gb == Decimal("32")
        assert ram_configs[0].density == Decimal("1.79")
        assert ram_configs[1].capacity_gb == Decimal("16")
    
    def test_to_ram_configurations_none(self):
        """Test converting None RAM schemas."""
        ram_configs = ServerMapper.to_ram_configurations(None)
        assert ram_configs is None
    
    def test_to_disk_configurations_multiple_types(self):
        """Test converting multiple disk schemas with different types."""
        disk_schemas = [
            DiskSchema(units=2, type="ssd", capacity=400, density=50.6),
            DiskSchema(units=2, type="hdd")
        ]
        
        disk_configs = ServerMapper.to_disk_configurations(disk_schemas)
        
        assert disk_configs is not None
        assert len(disk_configs) == 2
        assert disk_configs[0].type == "ssd"
        assert disk_configs[0].capacity_gb == Decimal("400")
        assert disk_configs[1].type == "hdd"
        assert disk_configs[1].capacity_gb is None
    
    def test_to_power_supply_configuration(self):
        """Test converting power supply schema to domain model."""
        ps_schema = PowerSupplySchema(units=2, unit_weight=10)
        
        ps_config = ServerMapper.to_power_supply_configuration(ps_schema)
        
        assert ps_config is not None
        assert ps_config.unit_weight_kg == Decimal("10")
    
    def test_to_case_configuration(self):
        """Test converting case schema to domain model."""
        case_schema = CaseSchema(units=1, case_type="rack")
        
        case_config = ServerMapper.to_case_configuration(case_schema)
        
        assert case_config is not None
        assert case_config.case_type == "rack"
    
    def test_to_device_configuration_complete(self):
        """Test converting complete server request to device configuration."""
        request = ServerRequestSchema(
            configuration=ServerConfigurationSchema(
                cpu=CPUSchema(
                    units=2,
                    core_units=24,
                    die_size_per_core=24.5
                ),
                ram=[
                    RAMSchema(units=4, capacity=32, density=1.79),
                    RAMSchema(units=4, capacity=16, density=1.79)
                ],
                disk=[
                    DiskSchema(units=2, type="ssd", capacity=400, density=50.6),
                    DiskSchema(units=2, type="hdd")
                ],
                power_supply=PowerSupplySchema(units=2, unit_weight=10)
            )
        )
        
        device_config = ServerMapper.to_device_configuration(request)
        
        assert device_config is not None
        assert device_config.cpu is not None
        assert device_config.cpu.core_units == 24
        assert device_config.ram is not None
        assert len(device_config.ram) == 2
        assert device_config.disk is not None
        assert len(device_config.disk) == 2
        assert device_config.power_supply is not None
    
    def test_to_device_configuration_empty(self):
        """Test converting empty server request to device configuration."""
        request = ServerRequestSchema()
        
        device_config = ServerMapper.to_device_configuration(request)
        
        assert device_config is not None
        assert device_config.cpu is None
        assert device_config.ram == []
        assert device_config.disk == []
    
    def test_to_usage_configuration_complete(self):
        """Test converting complete usage schema to domain model."""
        usage_schema = UsageSchema(
            usage_location="FRA",
            hours_life_time=35040.0,
            time_workload=50.0,
            workload={"10": 10.0, "50": 50.0, "100": 40.0}
        )
        
        usage_config = ServerMapper.to_usage_configuration(usage_schema)
        
        assert usage_config is not None
        assert usage_config.location == "FRA"
        assert usage_config.hours_life_time == Decimal("35040.0")
        assert usage_config.workload is not None
        assert usage_config.workload["10"] == Decimal("10.0")
        assert usage_config.workload["50"] == Decimal("50.0")
        assert usage_config.workload["100"] == Decimal("40.0")
    
    def test_to_usage_configuration_minimal(self):
        """Test converting minimal usage schema to domain model."""
        usage_schema = UsageSchema(usage_location="USA")
        
        usage_config = ServerMapper.to_usage_configuration(usage_schema)
        
        assert usage_config is not None
        assert usage_config.location == "USA"
        assert usage_config.hours_life_time is None
        assert usage_config.workload is None
    
    def test_to_usage_configuration_none(self):
        """Test converting None usage schema."""
        usage_config = ServerMapper.to_usage_configuration(None)
        
        assert usage_config is not None
        assert usage_config.location is None
        assert usage_config.hours_life_time is None
