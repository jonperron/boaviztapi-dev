"""Domain models for environmental impact results.

These are pure domain models with no dependencies on external frameworks.
They represent the core business concepts of environmental impact assessment.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from decimal import Decimal


@dataclass
class ImpactValue:
    """Represents a single environmental impact value with uncertainty.
    
    This is a pure domain concept that captures the value, its range,
    and metadata about how it was calculated.
    """
    value: Decimal
    min_value: Optional[Decimal] = None
    max_value: Optional[Decimal] = None
    unit: str = ""
    source: str = "CALCULATED"
    description: Optional[str] = None


@dataclass
class PhaseImpact:
    """Environmental impact for a specific lifecycle phase.
    
    Represents impacts during manufacturing, use, or end-of-life phases.
    """
    manufacturing: Dict[str, ImpactValue]
    use: Dict[str, ImpactValue] 
    end_of_life: Dict[str, ImpactValue]


@dataclass
class ImpactResult:
    """Complete environmental impact assessment result.
    
    This is the main domain model returned by impact computation use cases.
    It contains all calculated environmental impacts organized by criteria
    and lifecycle phases.
    """
    impacts: Dict[str, ImpactValue]  # Total impacts by criteria (gwp, pe, etc.)
    phases: PhaseImpact
    duration_years: float
    verbose_data: Optional[Dict[str, Any]] = None
    
    def get_total_impact(self, criteria: str) -> Optional[ImpactValue]:
        """Get total impact for a specific criteria."""
        return self.impacts.get(criteria)
    
    def get_phase_impact(self, phase: str, criteria: str) -> Optional[ImpactValue]:
        """Get impact for a specific phase and criteria."""
        phase_data = getattr(self.phases, phase, {})
        if isinstance(phase_data, dict):
            return phase_data.get(criteria)
        return None


@dataclass
class ComponentImpact:
    """Environmental impact of a specific component."""
    component_type: str  # 'cpu', 'ram', 'disk', etc.
    component_id: Optional[str] = None
    impacts: Dict[str, ImpactValue] = None
    phases: Optional[PhaseImpact] = None
    
    def __post_init__(self):
        if self.impacts is None:
            self.impacts = {}


@dataclass
class DeviceImpactBreakdown:
    """Detailed breakdown of device impact by component."""
    device_impacts: Dict[str, ImpactValue]  # Total device impacts
    component_impacts: List[ComponentImpact]  # Individual component impacts
    
    def get_component_impact(self, component_type: str) -> Optional[ComponentImpact]:
        """Get impact for a specific component type."""
        for comp in self.component_impacts:
            if comp.component_type == component_type:
                return comp
        return None