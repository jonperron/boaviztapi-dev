"""Domain models for device configurations.

These models represent the pure business concepts of device hardware
configurations without any dependencies on external frameworks.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from decimal import Decimal


@dataclass
class CPUConfiguration:
    """CPU configuration for environmental impact calculation."""
    name: Optional[str] = None
    manufacturer: Optional[str] = None
    core_units: Optional[int] = None
    die_size_per_core: Optional[Decimal] = None
    tdp: Optional[Decimal] = None  # Thermal Design Power in watts
    process_size_nm: Optional[int] = None
    model_range: Optional[str] = None
    family: Optional[str] = None
    
    # Archetype and completion metadata
    archetype: Optional[str] = None
    completed_attributes: Dict[str, str] = None
    
    def __post_init__(self):
        if self.completed_attributes is None:
            self.completed_attributes = {}


@dataclass 
class RAMConfiguration:
    """RAM configuration for environmental impact calculation."""
    capacity_gb: Optional[Decimal] = None
    density: Optional[Decimal] = None
    manufacturer: Optional[str] = None
    process_size_nm: Optional[int] = None
    
    # Archetype and completion metadata
    archetype: Optional[str] = None
    completed_attributes: Dict[str, str] = None
    
    def __post_init__(self):
        if self.completed_attributes is None:
            self.completed_attributes = {}


@dataclass
class DiskConfiguration:
    """Disk storage configuration for environmental impact calculation."""
    capacity_gb: Optional[Decimal] = None
    type: Optional[str] = None  # 'ssd' or 'hdd'
    manufacturer: Optional[str] = None
    
    # Archetype and completion metadata  
    archetype: Optional[str] = None
    completed_attributes: Dict[str, str] = None
    
    def __post_init__(self):
        if self.completed_attributes is None:
            self.completed_attributes = {}


@dataclass
class PowerSupplyConfiguration:
    """Power supply configuration."""
    unit_weight_kg: Optional[Decimal] = None
    
    # Archetype and completion metadata
    archetype: Optional[str] = None
    completed_attributes: Dict[str, str] = None
    
    def __post_init__(self):
        if self.completed_attributes is None:
            self.completed_attributes = {}


@dataclass
class CaseConfiguration:
    """Case/chassis configuration."""
    case_type: Optional[str] = None  # 'rack', 'tower', etc.
    
    # Archetype and completion metadata
    archetype: Optional[str] = None
    completed_attributes: Dict[str, str] = None
    
    def __post_init__(self):
        if self.completed_attributes is None:
            self.completed_attributes = {}


@dataclass
class DeviceConfiguration:
    """Complete device hardware configuration.
    
    This is a pure domain model with no framework dependencies.
    It represents the essential hardware configuration needed
    for environmental impact calculation.
    """
    # Core components
    cpu: Optional[CPUConfiguration] = None
    ram: List[RAMConfiguration] = None
    disk: List[DiskConfiguration] = None
    power_supply: Optional[PowerSupplyConfiguration] = None
    case: Optional[CaseConfiguration] = None
    
    # Device metadata
    archetype: Optional[str] = None
    completed_attributes: Dict[str, str] = None
    
    def __post_init__(self):
        if self.ram is None:
            self.ram = []
        if self.disk is None:
            self.disk = []
        if self.completed_attributes is None:
            self.completed_attributes = {}
    
    def get_total_ram_capacity(self) -> Decimal:
        """Calculate total RAM capacity across all modules."""
        total = Decimal('0')
        for ram in self.ram:
            if ram.capacity_gb:
                total += ram.capacity_gb
        return total
    
    def get_total_disk_capacity(self) -> Decimal:
        """Calculate total disk capacity across all disks.""" 
        total = Decimal('0')
        for disk in self.disk:
            if disk.capacity_gb:
                total += disk.capacity_gb
        return total


@dataclass
class CloudInstanceConfiguration:
    """Cloud instance configuration for impact calculation."""
    instance_type: str
    provider: str  # 'aws', 'azure', 'gcp', etc.
    region: Optional[str] = None
    
    # Underlying hardware (may be derived from instance type)
    cpu: Optional[CPUConfiguration] = None
    ram: List[RAMConfiguration] = None
    disk: List[DiskConfiguration] = None
    
    # Archetype and completion metadata
    archetype: Optional[str] = None
    completed_attributes: Dict[str, str] = None
    
    def __post_init__(self):
        if self.ram is None:
            self.ram = []
        if self.disk is None:
            self.disk = []
        if self.completed_attributes is None:
            self.completed_attributes = {}


@dataclass
class ComponentConfiguration:
    """Generic component configuration for individual component calculations."""
    component_type: str  # 'cpu', 'ram', 'disk', etc.
    configuration: Dict[str, Any]  # Flexible configuration dict
    
    # Archetype and completion metadata
    archetype: Optional[str] = None
    completed_attributes: Dict[str, str] = None
    
    def __post_init__(self):
        if self.completed_attributes is None:
            self.completed_attributes = {}


@dataclass
class IoTDeviceConfiguration:
    """IoT device configuration."""
    functional_blocks: List[Dict[str, Any]]
    archetype: Optional[str] = None
    completed_attributes: Dict[str, str] = None
    
    def __post_init__(self):
        if self.functional_blocks is None:
            self.functional_blocks = []
        if self.completed_attributes is None:
            self.completed_attributes = {}


@dataclass
class TerminalConfiguration:
    """User terminal configuration (laptop, desktop, tablet, etc.)."""
    terminal_type: str  # 'laptop', 'desktop', 'tablet', 'smartphone'
    
    # Hardware components
    cpu: Optional[CPUConfiguration] = None
    ram: List[RAMConfiguration] = None
    disk: List[DiskConfiguration] = None
    screen_size_inches: Optional[Decimal] = None
    
    # Archetype and completion metadata
    archetype: Optional[str] = None
    completed_attributes: Dict[str, str] = None
    
    def __post_init__(self):
        if self.ram is None:
            self.ram = []
        if self.disk is None:
            self.disk = []
        if self.completed_attributes is None:
            self.completed_attributes = {}