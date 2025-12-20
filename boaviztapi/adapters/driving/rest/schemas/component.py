"""
API schemas for component endpoints.
"""
from typing import Optional
from pydantic import BaseModel, Field
from boaviztapi.adapters.driving.rest.schemas.common import UsageSchema


class ComponentCPURequestSchema(BaseModel):
    """API schema for CPU component impact request."""
    units: Optional[int] = Field(None, description="Number of CPU units", ge=1)
    core_units: Optional[int] = Field(None, description="Number of cores", ge=1)
    die_size_per_core: Optional[float] = Field(None, description="Die size per core in mm²", gt=0)
    name: Optional[str] = Field(None, description="CPU name/model")
    tdp: Optional[float] = Field(None, description="Thermal Design Power in Watts", gt=0)
    manufacturer: Optional[str] = Field(None, description="CPU manufacturer")
    family: Optional[str] = Field(None, description="CPU family")
    usage: Optional[UsageSchema] = None
    verbose: bool = Field(True, description="Include verbose details in response")


class ComponentRAMRequestSchema(BaseModel):
    """API schema for RAM component impact request."""
    units: Optional[int] = Field(None, description="Number of RAM units", ge=1)
    capacity: Optional[float] = Field(None, description="Capacity in GB", gt=0)
    density: Optional[float] = Field(None, description="Density in GB per chip", gt=0)
    manufacturer: Optional[str] = Field(None, description="RAM manufacturer")
    usage: Optional[UsageSchema] = None
    verbose: bool = Field(True, description="Include verbose details in response")


class ComponentSSDRequestSchema(BaseModel):
    """API schema for SSD component impact request."""
    units: Optional[int] = Field(None, description="Number of SSD units", ge=1)
    capacity: Optional[float] = Field(None, description="Capacity in GB", gt=0)
    density: Optional[float] = Field(None, description="Density in GB", gt=0)
    manufacturer: Optional[str] = Field(None, description="SSD manufacturer")
    usage: Optional[UsageSchema] = None
    verbose: bool = Field(True, description="Include verbose details in response")
