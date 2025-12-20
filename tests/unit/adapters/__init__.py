"""
Unit tests for ResponseMapper.
"""
import pytest
from decimal import Decimal
from boaviztapi.core.domain.model.impact import ImpactResult, ImpactValue, PhaseImpact
from boaviztapi.adapters.driving.rest.mappers.response_mapper import ResponseMapper


class TestResponseMapper:
    """Test suite for ResponseMapper."""
    
    def test_to_impact_value_schema_basic(self):
        """Test converting basic ImpactValue to schema."""
        impact_value = ImpactValue(
            value=Decimal("100.5"),
            unit="kgCO2eq"
        )
        
        schema = ResponseMapper.to_impact_value_schema(impact_value)
        
        assert schema.value == 100.5
        assert schema.unit == "kgCO2eq"
        assert schema.min is None
        assert schema.max is None
    
    def test_to_impact_value_schema_with_uncertainty(self):
        """Test converting ImpactValue with uncertainty to schema."""
        impact_value = ImpactValue(
            value=Decimal("100.5"),
            min=Decimal("90.0"),
            max=Decimal("110.0"),
            unit="kgCO2eq"
        )
        
        schema = ResponseMapper.to_impact_value_schema(impact_value)
        
        assert schema.value == 100.5
        assert schema.min == 90.0
        assert schema.max == 110.0
        assert schema.unit == "kgCO2eq"
    
    def test_to_phase_impact_schema(self):
        """Test converting PhaseImpact to schema."""
        phase_impact = PhaseImpact(
            impacts={
                "gwp": ImpactValue(value=Decimal("1000.0"), unit="kgCO2eq"),
                "adp": ImpactValue(value=Decimal("0.5"), unit="kgSbeq"),
                "pe": ImpactValue(value=Decimal("15000.0"), unit="MJ")
            }
        )
        
        schema = ResponseMapper.to_phase_impact_schema(phase_impact)
        
        assert len(schema.impacts) == 3
        assert "gwp" in schema.impacts
        assert "adp" in schema.impacts
        assert "pe" in schema.impacts
        assert schema.impacts["gwp"].value == 1000.0
        assert schema.impacts["adp"].value == 0.5
        assert schema.impacts["pe"].value == 15000.0
    
    def test_to_impact_response_schema_complete(self):
        """Test converting complete ImpactResult to response schema."""
        manufacture_impact = PhaseImpact(
            impacts={
                "gwp": ImpactValue(
                    value=Decimal("1138.0"),
                    min=Decimal("1074.0"),
                    max=Decimal("1138.0"),
                    unit="kgCO2eq"
                ),
                "adp": ImpactValue(
                    value=Decimal("0.2536"),
                    min=Decimal("0.2536"),
                    max=Decimal("0.2611"),
                    unit="kgSbeq"
                ),
                "pe": ImpactValue(
                    value=Decimal("15420.0"),
                    min=Decimal("14450.0"),
                    max=Decimal("15420.0"),
                    unit="MJ"
                )
            }
        )
        
        use_impact = PhaseImpact(
            impacts={
                "gwp": ImpactValue(
                    value=Decimal("7000.0"),
                    min=Decimal("337.7"),
                    max=Decimal("26430.0"),
                    unit="kgCO2eq"
                ),
                "adp": ImpactValue(
                    value=Decimal("0.0013"),
                    min=Decimal("0.0001938"),
                    max=Decimal("0.007799"),
                    unit="kgSbeq"
                ),
                "pe": ImpactValue(
                    value=Decimal("300000.0"),
                    min=Decimal("190.9"),
                    max=Decimal("13750000.0"),
                    unit="MJ"
                )
            }
        )
        
        impact_result = ImpactResult(
            manufacture=manufacture_impact,
            use=use_impact
        )
        
        schema = ResponseMapper.to_impact_response_schema(impact_result, verbose=False)
        
        assert schema.manufacture is not None
        assert schema.use is not None
        assert schema.end_of_life is None
        assert schema.verbose is None
        
        # Check manufacture impacts
        assert schema.manufacture.impacts["gwp"].value == 1138.0
        assert schema.manufacture.impacts["gwp"].min == 1074.0
        assert schema.manufacture.impacts["gwp"].max == 1138.0
        
        # Check use impacts
        assert schema.use.impacts["gwp"].value == 7000.0
        assert schema.use.impacts["gwp"].min == 337.7
        assert schema.use.impacts["gwp"].max == 26430.0
    
    def test_to_impact_response_schema_with_verbose(self):
        """Test converting ImpactResult with verbose data to response schema."""
        phase_impact = PhaseImpact(
            impacts={
                "gwp": ImpactValue(value=Decimal("100.0"), unit="kgCO2eq")
            }
        )
        
        verbose_data = {
            "cpu": {"units": 2, "cores": 24},
            "computation_details": {"method": "bottom-up"}
        }
        
        impact_result = ImpactResult(
            manufacture=phase_impact,
            verbose_data=verbose_data
        )
        
        schema = ResponseMapper.to_impact_response_schema(impact_result, verbose=True)
        
        assert schema.verbose is not None
        assert schema.verbose["cpu"]["units"] == 2
        assert schema.verbose["cpu"]["cores"] == 24
    
    def test_to_impact_response_schema_minimal(self):
        """Test converting minimal ImpactResult to response schema."""
        impact_result = ImpactResult()
        
        schema = ResponseMapper.to_impact_response_schema(impact_result, verbose=False)
        
        assert schema.manufacture is None
        assert schema.use is None
        assert schema.end_of_life is None
        assert schema.verbose is None
