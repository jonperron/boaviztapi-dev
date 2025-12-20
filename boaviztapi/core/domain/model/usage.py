"""Domain models for usage configurations.

These models represent the pure business concepts of device usage
patterns and environmental context for impact calculations.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from decimal import Decimal


@dataclass
class WorkloadTime:
    """Time-based workload definition."""
    time_percentage: Decimal  # 0-100
    load_percentage: Decimal  # 0-100


@dataclass
class UsageConfiguration:
    """Usage pattern and environmental context for impact calculation.
    
    This is a pure domain model that captures how a device is used
    and the environmental context (location, duration, etc.).
    """
    # Location and electrical context
    location: Optional[str] = None  # Country code or region
    electrical_consumption_kwh: Optional[Decimal] = None
    
    # Usage duration
    hours_life_time: Optional[Decimal] = None
    hours_use_time: Optional[Decimal] = None
    usage_time_ratio: Optional[Decimal] = None  # 0.0 to 1.0
    
    # Workload patterns
    workload: Optional[Dict[str, Decimal]] = None  # Load percentages by time
    workload_time: Optional[List[WorkloadTime]] = None
    
    # Cloud-specific usage
    instances_number: Optional[int] = None
    
    # Archetype and completion metadata
    archetype: Optional[str] = None
    completed_attributes: Dict[str, str] = None
    
    def __post_init__(self):
        if self.completed_attributes is None:
            self.completed_attributes = {}
        if self.workload_time is None:
            self.workload_time = []
    
    def get_annual_usage_hours(self) -> Optional[Decimal]:
        """Calculate annual usage hours from usage time ratio."""
        if self.hours_use_time is not None and self.hours_life_time is not None:
            return self.hours_use_time
        
        if self.usage_time_ratio is not None:
            # Assume 8760 hours per year
            return Decimal('8760') * self.usage_time_ratio
        
        return None
    
    def get_total_workload_time_percentage(self) -> Decimal:
        """Calculate total time percentage across all workload periods."""
        total = Decimal('0')
        for wt in self.workload_time:
            total += wt.time_percentage
        return total


@dataclass
class ConsumptionProfileConfiguration:
    """Consumption profile configuration for power usage modeling."""
    cpu_consumption_profile: Optional[str] = None
    consumption_per_core: Optional[Dict[str, Decimal]] = None
    
    # Archetype and completion metadata
    archetype: Optional[str] = None
    completed_attributes: Dict[str, str] = None
    
    def __post_init__(self):
        if self.completed_attributes is None:
            self.completed_attributes = {}
        if self.consumption_per_core is None:
            self.consumption_per_core = {}


@dataclass
class CloudUsageConfiguration(UsageConfiguration):
    """Cloud-specific usage configuration."""
    instance_type: Optional[str] = None
    provider: Optional[str] = None
    region: Optional[str] = None
    
    # Cloud service allocation
    allocation_ratio: Optional[Decimal] = None  # Resource allocation ratio


@dataclass
class ServerUsageConfiguration(UsageConfiguration):
    """Server-specific usage configuration."""
    server_type: Optional[str] = None  # 'rack', 'tower', 'blade'
    
    # Datacenter context
    datacenter_pue: Optional[Decimal] = None  # Power Usage Effectiveness


@dataclass
class TerminalUsageConfiguration(UsageConfiguration):
    """Terminal-specific usage configuration."""
    terminal_type: Optional[str] = None
    
    # User behavior patterns
    daily_usage_hours: Optional[Decimal] = None
    power_management_enabled: Optional[bool] = None


@dataclass
class IoTUsageConfiguration(UsageConfiguration):
    """IoT device-specific usage configuration."""
    deployment_context: Optional[str] = None  # 'indoor', 'outdoor', etc.
    
    # Power source
    battery_powered: Optional[bool] = None
    energy_harvesting: Optional[bool] = None