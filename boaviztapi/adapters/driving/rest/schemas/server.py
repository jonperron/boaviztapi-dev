"""
API schemas for server endpoints.
"""
from typing import Dict, Optional, Any, List
from pydantic import BaseModel, Field
from boaviztapi.adapters.driving.rest.schemas.common import UsageSchema


class CPUSchema(BaseModel):
    """API schema for CPU configuration."""
    units: Optional[int] = Field(None, description="Number of CPU units", ge=1)
    core_units: Optional[int] = Field(None, description="Number of cores per CPU", ge=1)
    die_size_per_core: Optional[float] = Field(None, description="Die size per core in mm²", gt=0)
    name: Optional[str] = Field(None, description="CPU name/model")
    tdp: Optional[float] = Field(None, description="Thermal Design Power in Watts", gt=0)
    manufacturer: Optional[str] = Field(None, description="CPU manufacturer")
    family: Optional[str] = Field(None, description="CPU family")


class RAMSchema(BaseModel):
    """API schema for RAM configuration."""
    units: Optional[int] = Field(None, description="Number of RAM units", ge=1)
    capacity: Optional[float] = Field(None, description="Capacity in GB", gt=0)
    density: Optional[float] = Field(None, description="Density in GB per chip", gt=0)
    manufacturer: Optional[str] = Field(None, description="RAM manufacturer")


class DiskSchema(BaseModel):
    """API schema for disk configuration."""
    units: Optional[int] = Field(None, description="Number of disk units", ge=1)
    type: Optional[str] = Field(None, description="Disk type (ssd, hdd)")
    capacity: Optional[float] = Field(None, description="Capacity in GB", gt=0)
    density: Optional[float] = Field(None, description="Density in GB", gt=0)
    manufacturer: Optional[str] = Field(None, description="Disk manufacturer")


class PowerSupplySchema(BaseModel):
    """API schema for power supply configuration."""
    units: Optional[int] = Field(None, description="Number of power supply units", ge=1)
    unit_weight: Optional[float] = Field(None, description="Weight in kg", gt=0)


class MotherboardSchema(BaseModel):
    """API schema for motherboard configuration."""
    units: Optional[int] = Field(None, description="Number of motherboard units", ge=1)


class AssemblySchema(BaseModel):
    """API schema for assembly configuration."""
    units: Optional[int] = Field(None, description="Number of assembly units", ge=1)


class CaseSchema(BaseModel):
    """API schema for case configuration."""
    units: Optional[int] = Field(None, description="Number of case units", ge=1)
    case_type: Optional[str] = Field(None, description="Case type (rack, blade, tower)")


class ServerConfigurationSchema(BaseModel):
    """API schema for server hardware configuration."""
    cpu: Optional[CPUSchema] = None
    ram: Optional[List[RAMSchema]] = None
    disk: Optional[List[DiskSchema]] = None
    power_supply: Optional[PowerSupplySchema] = None
    motherboard: Optional[MotherboardSchema] = None
    assembly: Optional[AssemblySchema] = None
    case: Optional[CaseSchema] = None


class ServerModelSchema(BaseModel):
    """API schema for server model (archetype)."""
    type: Optional[str] = Field(None, description="Server type/archetype name")
    manufacturer: Optional[str] = Field(None, description="Server manufacturer")
    name: Optional[str] = Field(None, description="Server model name")
    archetype: Optional[str] = Field(None, description="Archetype identifier")


class ServerRequestSchema(BaseModel):
    """API schema for server impact computation request."""
    model: Optional[ServerModelSchema] = None
    configuration: Optional[ServerConfigurationSchema] = None
    usage: Optional[UsageSchema] = None
    verbose: bool = Field(True, description="Include verbose details in response")
