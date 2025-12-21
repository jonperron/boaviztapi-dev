"""
Mapper to convert server API requests to domain models.
"""
from typing import Optional, List
from decimal import Decimal
from boaviztapi.core.domain.model.device import (
    DeviceConfiguration,
    CPUConfiguration,
    RAMConfiguration,
    DiskConfiguration,
    PowerSupplyConfiguration,
    CaseConfiguration
)
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.adapters.driving.rest.schemas.server import (
    ServerRequestSchema,
    CPUSchema,
    RAMSchema,
    DiskSchema,
    PowerSupplySchema,
    MotherboardSchema,
    AssemblySchema,
    CaseSchema
)
from boaviztapi.adapters.driving.rest.schemas.common import UsageSchema


class ServerMapper:
    """Maps server API requests to domain models."""
    
    @staticmethod
    def to_cpu_configuration(cpu_schema: Optional[CPUSchema]) -> Optional[CPUConfiguration]:
        """
        Convert API CPU schema to domain CPUConfiguration.
        
        Args:
            cpu_schema: API CPU schema
            
        Returns:
            Domain CPU configuration or None
        """
        if not cpu_schema:
            return None
        
        return CPUConfiguration(
            core_units=cpu_schema.core_units,
            die_size_per_core=Decimal(str(cpu_schema.die_size_per_core)) 
                if cpu_schema.die_size_per_core is not None else None,
            name=cpu_schema.name,
            tdp=Decimal(str(cpu_schema.tdp)) if cpu_schema.tdp is not None else None,
            manufacturer=cpu_schema.manufacturer,
            family=cpu_schema.family
        )
    
    @staticmethod
    def to_ram_configurations(ram_schemas: Optional[List[RAMSchema]]) -> Optional[List[RAMConfiguration]]:
        """
        Convert API RAM schemas to domain RAMConfiguration list.
        
        Args:
            ram_schemas: List of API RAM schemas
            
        Returns:
            List of domain RAM configurations or None
        """
        if not ram_schemas:
            return None
        
        return [
            RAMConfiguration(
                capacity_gb=Decimal(str(ram.capacity)) if ram.capacity is not None else None,
                density=Decimal(str(ram.density)) if ram.density is not None else None,
                manufacturer=ram.manufacturer
            )
            for ram in ram_schemas
        ]
    
    @staticmethod
    def to_disk_configurations(disk_schemas: Optional[List[DiskSchema]]) -> Optional[List[DiskConfiguration]]:
        """
        Convert API disk schemas to domain DiskConfiguration list.
        
        Args:
            disk_schemas: List of API disk schemas
            
        Returns:
            List of domain disk configurations or None
        """
        if not disk_schemas:
            return None
        
        return [
            DiskConfiguration(
                type=disk.type,
                capacity_gb=Decimal(str(disk.capacity)) if disk.capacity is not None else None,
                manufacturer=disk.manufacturer
            )
            for disk in disk_schemas
        ]
    
    @staticmethod
    def to_power_supply_configuration(ps_schema: Optional[PowerSupplySchema]) -> Optional[PowerSupplyConfiguration]:
        """
        Convert API power supply schema to domain PowerSupplyConfiguration.
        
        Args:
            ps_schema: API power supply schema
            
        Returns:
            Domain power supply configuration or None
        """
        if not ps_schema:
            return None
        
        return PowerSupplyConfiguration(
            unit_weight_kg=Decimal(str(ps_schema.unit_weight)) 
                if ps_schema.unit_weight is not None else None
        )
    
    @staticmethod
    def to_case_configuration(case_schema: Optional[CaseSchema]) -> Optional[CaseConfiguration]:
        """
        Convert API case schema to domain CaseConfiguration.
        
        Args:
            case_schema: API case schema
            
        Returns:
            Domain case configuration or None
        """
        if not case_schema:
            return None
        
        return CaseConfiguration(
            case_type=case_schema.case_type
        )
    
    @staticmethod
    def to_device_configuration(request: ServerRequestSchema) -> DeviceConfiguration:
        """
        Convert server API request to domain DeviceConfiguration.
        
        Args:
            request: Server API request
            
        Returns:
            Domain device configuration
        """
        config = request.configuration
        if not config:
            return DeviceConfiguration()
        
        return DeviceConfiguration(
            cpu=ServerMapper.to_cpu_configuration(config.cpu),
            ram=ServerMapper.to_ram_configurations(config.ram),
            disk=ServerMapper.to_disk_configurations(config.disk),
            power_supply=ServerMapper.to_power_supply_configuration(config.power_supply),
            case=ServerMapper.to_case_configuration(config.case)
        )
    
    @staticmethod
    def to_usage_configuration(usage_schema: Optional[UsageSchema]) -> UsageConfiguration:
        """
        Convert API usage schema to domain UsageConfiguration.
        
        Args:
            usage_schema: API usage schema
            
        Returns:
            Domain usage configuration
        """
        if not usage_schema:
            return UsageConfiguration()
        
        workload = None
        if usage_schema.workload:
            workload = {k: Decimal(str(v)) for k, v in usage_schema.workload.items()}
        
        return UsageConfiguration(
            location=usage_schema.usage_location,
            hours_life_time=Decimal(str(usage_schema.hours_life_time)) 
                if usage_schema.hours_life_time is not None else None,
            workload=workload
        )
