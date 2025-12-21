"""Domain service for impact calculations.

This service contains pure business logic for computing environmental
impacts. It has no dependencies on infrastructure or frameworks.
"""

from typing import Dict, List
from decimal import Decimal

from boaviztapi.core.domain.model.impact import ImpactValue, PhaseImpact
from boaviztapi.core.domain.model.device import DeviceConfiguration
from boaviztapi.core.domain.model.usage import UsageConfiguration


class ImpactCalculator:
    """Domain service for calculating environmental impacts.
    
    This service encapsulates the pure business logic for impact computation.
    It operates on domain models and has no external dependencies.
    """
    
    def calculate_manufacturing_impact(
        self,
        device_config: DeviceConfiguration,
        criteria: List[str],
        impact_factors: Dict[str, Dict[str, float]],
    ) -> Dict[str, ImpactValue]:
        """Calculate manufacturing phase impact.
        
        Args:
            device_config: Device hardware configuration
            criteria: Impact criteria to calculate (gwp, pe, adp, etc.)
            impact_factors: Impact factors from data source
            
        Returns:
            Dictionary of impact values by criteria
        """
        # Simplified stub implementation for Phase 4
        # TODO: Full migration of Boattribute-based logic from service layer
        # For now, demonstrate the pattern with basic calculations
        
        result = {}
        
        for criterion in criteria:
            total_value = Decimal('0')
            
            # Basic CPU manufacturing impact (simplified from cpu_impact_embedded)
            if device_config.cpu and 'cpu' in impact_factors:
                cpu_impact = self._calculate_cpu_manufacturing(
                    device_config.cpu, 
                    impact_factors['cpu']
                )
                total_value += cpu_impact
            
            # Basic RAM manufacturing impact (simplified from ram_impact_embedded)
            if device_config.ram:
                for ram in device_config.ram:
                    ram_impact = self._calculate_ram_manufacturing(
                        ram,
                        impact_factors.get('ram', {})
                    )
                    total_value += ram_impact
            
            # Basic disk manufacturing impact
            if device_config.disk:
                for disk in device_config.disk:
                    disk_impact = self._calculate_disk_manufacturing(
                        disk,
                        impact_factors.get(disk.type, {})
                    )
                    total_value += disk_impact
            
            # Determine unit based on criterion
            unit_map = {
                'gwp': 'kgCO2eq',
                'pe': 'MJ',
                'adp': 'kgSbeq'
            }
            
            result[criterion] = ImpactValue(
                value=total_value,
                min_value=total_value * Decimal('0.9'),  # Simplified uncertainty
                max_value=total_value * Decimal('1.1'),
                unit=unit_map.get(criterion, 'unknown'),
                source='CALCULATED'
            )
        
        return result
    
    def calculate_use_impact(
        self,
        device_config: DeviceConfiguration,
        usage_config: UsageConfiguration,
        criteria: List[str],
        duration_hours: float,
        electrical_factors: Dict[str, float],
    ) -> Dict[str, ImpactValue]:
        """Calculate use phase impact.
        
        Args:
            device_config: Device hardware configuration
            usage_config: Usage patterns
            criteria: Impact criteria to calculate
            duration_hours: Duration of use in hours
            electrical_factors: Electrical mix factors for location
            
        Returns:
            Dictionary of impact values by criteria
        """
        # Simplified stub implementation for Phase 4
        # TODO: Full migration including power modeling from service layer
        
        result = {}
        
        # Estimate average power consumption (simplified)
        avg_power_watts = self._estimate_device_power(device_config)
        
        # Calculate energy consumption in kWh
        energy_kwh = (avg_power_watts / 1000) * duration_hours
        
        # Apply workload if specified
        if usage_config.workload:
            time_workload = usage_config.workload.get('time_workload', 50) / 100
            energy_kwh *= time_workload
        
        for criterion in criteria:
            # Get electrical factor for this criterion
            elec_factor = electrical_factors.get(criterion, 0.0)
            
            impact_value = Decimal(str(energy_kwh * elec_factor))
            
            unit_map = {
                'gwp': 'kgCO2eq',
                'pe': 'MJ',
                'adp': 'kgSbeq'
            }
            
            result[criterion] = ImpactValue(
                value=impact_value,
                min_value=impact_value * Decimal('0.8'),  # Simplified uncertainty
                max_value=impact_value * Decimal('1.2'),
                unit=unit_map.get(criterion, 'unknown'),
                source='CALCULATED'
            )
        
        return result
    
    def calculate_end_of_life_impact(
        self,
        device_config: DeviceConfiguration,
        criteria: List[str],
        impact_factors: Dict[str, Dict[str, float]],
    ) -> Dict[str, ImpactValue]:
        """Calculate end-of-life phase impact.
        
        Args:
            device_config: Device hardware configuration
            criteria: Impact criteria to calculate
            impact_factors: Impact factors from data source
            
        Returns:
            Dictionary of impact values by criteria
        """
        # Simplified stub implementation for Phase 4
        # TODO: Implement end-of-life calculations when data is available
        # For now, return zero impacts (as per existing service layer comments)
        
        result = {}
        unit_map = {
            'gwp': 'kgCO2eq',
            'pe': 'MJ',
            'adp': 'kgSbeq'
        }
        
        for criterion in criteria:
            result[criterion] = ImpactValue(
                value=Decimal('0'),
                min_value=Decimal('0'),
                max_value=Decimal('0'),
                unit=unit_map.get(criterion, 'unknown'),
                source='NOT_IMPLEMENTED'
            )
        
        return result
    
    def _calculate_cpu_manufacturing(
        self,
        cpu_config,
        cpu_factors: Dict[str, float]
    ) -> Decimal:
        """Calculate CPU manufacturing impact (simplified from cpu_impact_embedded).
        
        TODO: Full implementation with die_size calculations and allocation
        """
        # Simplified: use base impact factor
        base_impact = cpu_factors.get('impact', 20.0)
        units = getattr(cpu_config, 'units', 1)
        return Decimal(str(base_impact * units))
    
    def _calculate_ram_manufacturing(
        self,
        ram_config,
        ram_factors: Dict[str, float]
    ) -> Decimal:
        """Calculate RAM manufacturing impact (simplified from ram_impact_embedded).
        
        TODO: Full implementation with capacity/density die impact calculations
        """
        # Simplified: use base impact factor
        base_impact = ram_factors.get('impact', 10.0)
        units = getattr(ram_config, 'units', 1)
        return Decimal(str(base_impact * units))
    
    def _calculate_disk_manufacturing(
        self,
        disk_config,
        disk_factors: Dict[str, float]
    ) -> Decimal:
        """Calculate disk manufacturing impact (simplified).
        
        TODO: Full implementation with capacity/density calculations for SSD
        """
        # Simplified: use base impact factor
        base_impact = disk_factors.get('impact', 15.0)
        units = getattr(disk_config, 'units', 1)
        return Decimal(str(base_impact * units))
    
    def _estimate_device_power(self, device_config: DeviceConfiguration) -> float:
        """Estimate device power consumption in watts (simplified).
        
        TODO: Full implementation using power modeling from service layer
        """
        from boaviztapi.core.config_constants import DEFAULT_WORKLOAD_PERCENTAGE
        total_power = 0.0
        
        # Simplified CPU power estimation
        if device_config.cpu:
            cpu_tdp = getattr(device_config.cpu, 'tdp', None)
            if cpu_tdp is None:
                cpu_tdp = 100.0  # Default TDP if not specified
            if isinstance(cpu_tdp, Decimal):
                cpu_tdp = float(cpu_tdp)
            units = getattr(device_config.cpu, 'units', 1)
            if isinstance(units, Decimal):
                units = float(units)
            total_power += cpu_tdp * units
        
        # Simplified RAM power estimation
        if device_config.ram:
            for ram in device_config.ram:
                ram_power = 5.0  # Simplified: ~5W per RAM module
                units = getattr(ram, 'units', 1)
                if isinstance(units, Decimal):
                    units = float(units)
                total_power += ram_power * units
        
        # Simplified disk power estimation
        if device_config.disk:
            for disk in device_config.disk:
                disk_power = 10.0 if disk.type == 'hdd' else 5.0
                units = getattr(disk, 'units', 1)
                if isinstance(units, Decimal):
                    units = float(units)
                total_power += disk_power * units
        
        # Add baseline for other components (motherboard, power supply, etc.)
        total_power += 50.0
        
        return total_power
    
    def aggregate_phase_impacts(
        self,
        manufacturing: Dict[str, ImpactValue],
        use: Dict[str, ImpactValue],
        end_of_life: Dict[str, ImpactValue],
    ) -> Dict[str, ImpactValue]:
        """Aggregate impacts across all lifecycle phases.
        
        Args:
            manufacturing: Manufacturing phase impacts
            use: Use phase impacts
            end_of_life: End-of-life phase impacts
            
        Returns:
            Total aggregated impacts by criteria
        """
        # TODO: Implement aggregation logic
        total_impacts = {}
        
        # For each criteria, sum up the values from all phases
        all_criteria = set(manufacturing.keys()) | set(use.keys()) | set(end_of_life.keys())
        
        for criteria in all_criteria:
            total_value = Decimal('0')
            unit = 'unknown'
            
            if criteria in manufacturing:
                total_value += manufacturing[criteria].value
                unit = manufacturing[criteria].unit
            
            if criteria in use:
                total_value += use[criteria].value
                unit = use[criteria].unit
            
            if criteria in end_of_life:
                total_value += end_of_life[criteria].value
                unit = end_of_life[criteria].unit
            
            total_impacts[criteria] = ImpactValue(
                value=total_value,
                unit=unit,
                source='AGGREGATED'
            )
        
        return total_impacts