"""Integration tests for ImpactCalculator with realistic data.

These tests validate the Phase 4 implementation using test data patterns
from the original service layer tests.
"""

import pytest
from decimal import Decimal

from boaviztapi.core.domain.services.impact_calculator import ImpactCalculator
from boaviztapi.core.domain.model.device import (
    DeviceConfiguration,
    CPUConfiguration,
    RAMConfiguration,
    DiskConfiguration
)
from boaviztapi.core.domain.model.usage import UsageConfiguration


class TestImpactCalculatorCalculations:
    """Test suite for ImpactCalculator calculations with realistic data."""
    
    @pytest.fixture
    def calculator(self):
        """Create an ImpactCalculator instance."""
        return ImpactCalculator()
    
    @pytest.fixture
    def complete_server_config(self):
        """Create a complete server configuration (similar to Dell R740)."""
        # Note: Domain model uses lists for components; each item in list = 1 unit
        # To represent 12 RAM modules, we create a list with 12 RAMConfiguration objects
        return DeviceConfiguration(
            cpu=CPUConfiguration(
                core_units=24,
                die_size_per_core=Decimal('24.5'),
                tdp=Decimal('150')
            ),
            ram=[
                RAMConfiguration(
                    capacity_gb=32,
                    density=Decimal('1.79')
                )
                for _ in range(12)  # 12 RAM modules
            ],
            disk=[
                DiskConfiguration(
                    type='ssd',
                    capacity_gb=400
                )
            ]
        )
    
    @pytest.fixture
    def minimal_server_config(self):
        """Create a minimal server configuration."""
        return DeviceConfiguration(
            cpu=CPUConfiguration(
                core_units=4,
                tdp=Decimal('95')
            )
        )
    
    @pytest.fixture
    def typical_usage_config(self):
        """Create a typical usage configuration."""
        return UsageConfiguration(
            location="FR",
            usage_time_ratio=Decimal('0.5'),
            workload={'time_workload': 50}
        )
    
    @pytest.fixture
    def impact_factors(self):
        """Create realistic impact factors."""
        return {
            'cpu': {'impact': 20.0, 'die_impact': 2.0},
            'ram': {'impact': 10.0, 'die_impact': 0.5},
            'ssd': {'impact': 15.0, 'die_impact': 1.0},
            'hdd': {'impact': 12.0}
        }
    
    @pytest.fixture
    def electrical_factors(self):
        """Create realistic electrical factors (world average)."""
        return {
            'gwp': 0.5,  # kgCO2eq/kWh
            'pe': 11.0,  # MJ/kWh
            'adp': 0.00002  # kgSbeq/kWh
        }
    
    def test_manufacturing_impact_complete_server(
        self, calculator, complete_server_config, impact_factors
    ):
        """Test manufacturing impact for a complete server configuration."""
        result = calculator.calculate_manufacturing_impact(
            device_config=complete_server_config,
            criteria=["gwp", "pe", "adp"],
            impact_factors=impact_factors
        )
        
        # Should have results for all criteria
        assert "gwp" in result
        assert "pe" in result
        assert "adp" in result
        
        # Should calculate impact for CPU (2 units)
        # Should calculate impact for RAM (12 units)
        # Should calculate impact for SSD (1 unit)
        # Total impact should be positive
        assert result["gwp"].value > 0
        assert result["pe"].value > 0
        assert result["adp"].value > 0
        
        # Min/max should be present (simplified uncertainty)
        assert result["gwp"].min_value is not None
        assert result["gwp"].max_value is not None
    
    def test_manufacturing_impact_minimal_server(
        self, calculator, minimal_server_config, impact_factors
    ):
        """Test manufacturing impact for a minimal server configuration."""
        result = calculator.calculate_manufacturing_impact(
            device_config=minimal_server_config,
            criteria=["gwp"],
            impact_factors=impact_factors
        )
        
        # Should have result for gwp
        assert "gwp" in result
        
        # Should only calculate CPU impact (no RAM or disk)
        # Impact should be lower than complete server
        # Default units=1 when not provided, so: 1 * 20.0 = 20.0
        assert result["gwp"].value > 0
        assert result["gwp"].value == Decimal('20.0')  # 1 CPU unit * 20.0 impact
    
    def test_use_impact_with_workload(
        self, calculator, complete_server_config, typical_usage_config, electrical_factors
    ):
        """Test use impact calculation with workload time."""
        result = calculator.calculate_use_impact(
            device_config=complete_server_config,
            usage_config=typical_usage_config,
            criteria=["gwp", "pe"],
            duration_hours=8760.0,  # 1 year
            electrical_factors=electrical_factors
        )
        
        # Should have results for requested criteria
        assert "gwp" in result
        assert "pe" in result
        
        # Impact should be positive
        assert result["gwp"].value > 0
        assert result["pe"].value > 0
        
        # Should have units
        assert result["gwp"].unit == "kgCO2eq"
        assert result["pe"].unit == "MJ"
    
    def test_use_impact_power_estimation(
        self, calculator, complete_server_config
    ):
        """Test power estimation for complete server."""
        power = calculator._estimate_device_power(complete_server_config)
        
        # Should estimate power based on:
        # - 1 CPU with TDP 150W = 150W (units defaults to 1)
        # - 12 RAM modules at ~5W each = 60W
        # - 1 SSD at ~5W = 5W
        # - Baseline (motherboard, etc.) = 50W
        # Total should be around 265W
        assert power > 0
        assert power > 150  # At least CPU power
        assert power < 500  # Reasonable upper bound
    
    def test_end_of_life_impact_returns_zero(
        self, calculator, complete_server_config, impact_factors
    ):
        """Test that end-of-life impact returns zero (not implemented yet)."""
        result = calculator.calculate_end_of_life_impact(
            device_config=complete_server_config,
            criteria=["gwp", "pe"],
            impact_factors=impact_factors
        )
        
        # Should return results but with zero values
        assert "gwp" in result
        assert "pe" in result
        assert result["gwp"].value == Decimal('0')
        assert result["pe"].value == Decimal('0')
        assert result["gwp"].source == "NOT_IMPLEMENTED"
    
    def test_aggregate_phase_impacts_all_criteria(self, calculator):
        """Test aggregation with multiple criteria across phases."""
        from boaviztapi.core.domain.model.impact import ImpactValue
        
        manufacturing = {
            "gwp": ImpactValue(
                value=Decimal('100'),
                unit='kgCO2eq',
                source='CALC'
            ),
            "pe": ImpactValue(
                value=Decimal('1500'),
                unit='MJ',
                source='CALC'
            )
        }
        
        use = {
            "gwp": ImpactValue(
                value=Decimal('200'),
                unit='kgCO2eq',
                source='CALC'
            ),
            "pe": ImpactValue(
                value=Decimal('3000'),
                unit='MJ',
                source='CALC'
            )
        }
        
        end_of_life = {
            "gwp": ImpactValue(
                value=Decimal('10'),
                unit='kgCO2eq',
                source='CALC'
            )
        }
        
        result = calculator.aggregate_phase_impacts(
            manufacturing=manufacturing,
            use=use,
            end_of_life=end_of_life
        )
        
        # Should aggregate all criteria
        assert "gwp" in result
        assert "pe" in result
        
        # GWP: 100 + 200 + 10 = 310
        assert result["gwp"].value == Decimal('310')
        
        # PE: 1500 + 3000 = 4500 (no end-of-life PE)
        assert result["pe"].value == Decimal('4500')
        
        # Should preserve units
        assert result["gwp"].unit == 'kgCO2eq'
        assert result["pe"].unit == 'MJ'
        
        # Should mark as aggregated
        assert result["gwp"].source == 'AGGREGATED'
    
    def test_cpu_manufacturing_with_multiple_units(
        self, calculator, impact_factors
    ):
        """Test CPU manufacturing calculation (units default to 1)."""
        cpu_config = CPUConfiguration(
            core_units=12,
            tdp=Decimal('120')
        )
        
        result = calculator._calculate_cpu_manufacturing(
            cpu_config,
            impact_factors['cpu']
        )
        
        # Should use base impact with default units=1: 20.0 * 1 = 20.0
        assert result == Decimal('20.0')
    
    def test_ram_manufacturing_with_multiple_modules(
        self, calculator, impact_factors
    ):
        """Test RAM manufacturing calculation (units default to 1 per module)."""
        ram_config = RAMConfiguration(
            capacity_gb=16,
            density=Decimal('1.5')
        )
        
        result = calculator._calculate_ram_manufacturing(
            ram_config,
            impact_factors['ram']
        )
        
        # Should use base impact with default units=1: 10.0 * 1 = 10.0
        assert result == Decimal('10.0')
    
    def test_disk_manufacturing_ssd(self, calculator, impact_factors):
        """Test SSD manufacturing calculation."""
        ssd_config = DiskConfiguration(
            type='ssd',
            capacity_gb=1000
        )
        
        result = calculator._calculate_disk_manufacturing(
            ssd_config,
            impact_factors['ssd']
        )
        
        # Should use base impact with default units=1: 15.0 * 1 = 15.0
        assert result == Decimal('15.0')
    
    def test_disk_manufacturing_hdd(self, calculator, impact_factors):
        """Test HDD manufacturing calculation."""
        hdd_config = DiskConfiguration(
            type='hdd',
            capacity_gb=2000
        )
        
        result = calculator._calculate_disk_manufacturing(
            hdd_config,
            impact_factors['hdd']
        )
        
        # Should use HDD impact factor with default units=1: 12.0 * 1 = 12.0
        assert result == Decimal('12.0')
    
    def test_power_estimation_with_decimal_values(self, calculator):
        """Test power estimation handles Decimal types correctly."""
        config = DeviceConfiguration(
            cpu=CPUConfiguration(
                tdp=Decimal('150.5')
            ),
            ram=[
                RAMConfiguration(capacity_gb=16)
                for _ in range(4)  # 4 RAM modules
            ]
        )
        
        # Should handle Decimal without errors
        power = calculator._estimate_device_power(config)
        
        # Should return a float
        assert isinstance(power, float)
        assert power > 0
    
    def test_use_impact_scales_with_duration(
        self, calculator, minimal_server_config, typical_usage_config, electrical_factors
    ):
        """Test that use impact scales linearly with duration."""
        # Calculate for 1 year
        result_1year = calculator.calculate_use_impact(
            device_config=minimal_server_config,
            usage_config=typical_usage_config,
            criteria=["gwp"],
            duration_hours=8760.0,
            electrical_factors=electrical_factors
        )
        
        # Calculate for 2 years
        result_2years = calculator.calculate_use_impact(
            device_config=minimal_server_config,
            usage_config=typical_usage_config,
            criteria=["gwp"],
            duration_hours=17520.0,
            electrical_factors=electrical_factors
        )
        
        # 2 years should have ~2x the impact of 1 year
        # (allowing for small floating point differences)
        ratio = float(result_2years["gwp"].value) / float(result_1year["gwp"].value)
        assert 1.95 < ratio < 2.05
