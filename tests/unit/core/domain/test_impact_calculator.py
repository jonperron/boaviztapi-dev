"""Unit tests for ImpactCalculator domain service."""

import pytest
from decimal import Decimal

from boaviztapi.core.domain.services.impact_calculator import ImpactCalculator
from boaviztapi.core.domain.model.device import DeviceConfiguration, CPUConfiguration
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.core.domain.model.impact import ImpactValue


class TestImpactCalculator:
    """Test suite for ImpactCalculator domain service."""
    
    @pytest.fixture
    def calculator(self):
        """Create an ImpactCalculator instance."""
        return ImpactCalculator()
    
    @pytest.fixture
    def device_config(self):
        """Create a sample device configuration."""
        return DeviceConfiguration(
            cpu=CPUConfiguration(
                core_units=4,
                tdp=Decimal('95')
            )
        )
    
    @pytest.fixture
    def usage_config(self):
        """Create a sample usage configuration."""
        return UsageConfiguration(
            location="FR",
            usage_time_ratio=Decimal('0.5')
        )
    
    def test_calculator_instantiation(self, calculator):
        """Test that calculator can be instantiated."""
        assert calculator is not None
        assert isinstance(calculator, ImpactCalculator)
    
    def test_calculate_manufacturing_impact_returns_dict(self, calculator, device_config):
        """Test that manufacturing impact calculation returns a dict."""
        result = calculator.calculate_manufacturing_impact(
            device_config=device_config,
            criteria=["gwp", "pe"],
            impact_factors={"gwp": {"value": 1.2}}
        )
        
        assert isinstance(result, dict)
    
    def test_calculate_use_impact_returns_dict(
        self, calculator, device_config, usage_config
    ):
        """Test that use impact calculation returns a dict."""
        result = calculator.calculate_use_impact(
            device_config=device_config,
            usage_config=usage_config,
            criteria=["gwp"],
            duration_hours=8760.0,
            electrical_factors={"carbon_intensity": 0.38}
        )
        
        assert isinstance(result, dict)
    
    def test_calculate_end_of_life_impact_returns_dict(self, calculator, device_config):
        """Test that end-of-life impact calculation returns a dict."""
        result = calculator.calculate_end_of_life_impact(
            device_config=device_config,
            criteria=["gwp"],
            impact_factors={"gwp": {"value": 0.1}}
        )
        
        assert isinstance(result, dict)
    
    def test_aggregate_phase_impacts_with_empty_dicts(self, calculator):
        """Test aggregating empty phase impacts."""
        result = calculator.aggregate_phase_impacts(
            manufacturing={},
            use={},
            end_of_life={}
        )
        
        assert isinstance(result, dict)
        assert len(result) == 0
    
    def test_aggregate_phase_impacts_sums_values(self, calculator):
        """Test that aggregation sums values across phases."""
        manufacturing = {
            "gwp": ImpactValue(
                value=Decimal('100'),
                unit='kgCO2eq',
                source='CALC'
            )
        }
        use = {
            "gwp": ImpactValue(
                value=Decimal('50'),
                unit='kgCO2eq',
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
        
        assert "gwp" in result
        assert result["gwp"].value == Decimal('160')
        assert result["gwp"].unit == 'kgCO2eq'
    
    def test_aggregate_phase_impacts_handles_missing_criteria_in_phases(self, calculator):
        """Test aggregation when criteria is missing in some phases."""
        manufacturing = {
            "gwp": ImpactValue(value=Decimal('100'), unit='kgCO2eq', source='CALC'),
            "pe": ImpactValue(value=Decimal('500'), unit='MJ', source='CALC')
        }
        use = {
            "gwp": ImpactValue(value=Decimal('50'), unit='kgCO2eq', source='CALC')
        }
        end_of_life = {}
        
        result = calculator.aggregate_phase_impacts(
            manufacturing=manufacturing,
            use=use,
            end_of_life=end_of_life
        )
        
        assert "gwp" in result
        assert result["gwp"].value == Decimal('150')
        assert "pe" in result
        assert result["pe"].value == Decimal('500')
    
    def test_aggregate_phase_impacts_with_multiple_criteria(self, calculator):
        """Test aggregation with multiple impact criteria."""
        manufacturing = {
            "gwp": ImpactValue(value=Decimal('100'), unit='kgCO2eq', source='CALC'),
            "pe": ImpactValue(value=Decimal('1000'), unit='MJ', source='CALC'),
            "adp": ImpactValue(value=Decimal('0.5'), unit='kgSbeq', source='CALC')
        }
        use = {
            "gwp": ImpactValue(value=Decimal('200'), unit='kgCO2eq', source='CALC'),
            "pe": ImpactValue(value=Decimal('2000'), unit='MJ', source='CALC')
        }
        end_of_life = {
            "gwp": ImpactValue(value=Decimal('20'), unit='kgCO2eq', source='CALC')
        }
        
        result = calculator.aggregate_phase_impacts(
            manufacturing=manufacturing,
            use=use,
            end_of_life=end_of_life
        )
        
        assert len(result) == 3
        assert result["gwp"].value == Decimal('320')
        assert result["pe"].value == Decimal('3000')
        assert result["adp"].value == Decimal('0.5')