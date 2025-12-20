"""Unit tests for domain exceptions."""

import pytest

from boaviztapi.core.domain.exceptions import (
    DomainException,
    ArchetypeNotFoundError,
    InvalidComponentConfigurationError,
    InvalidDeviceConfigurationError,
    ImpactComputationError,
    CountryNotSupportedError,
    InvalidUsageConfigurationError,
    MissingRequiredDataError,
)


class TestDomainExceptions:
    """Test suite for domain exceptions."""
    
    def test_domain_exception_is_base_exception(self):
        """Test that DomainException is the base exception."""
        exc = DomainException("test message")
        assert isinstance(exc, Exception)
        assert str(exc) == "test message"
    
    def test_archetype_not_found_error_contains_details(self):
        """Test ArchetypeNotFoundError includes archetype details."""
        exc = ArchetypeNotFoundError("default_cpu", "cpu")
        
        assert isinstance(exc, DomainException)
        assert exc.archetype_name == "default_cpu"
        assert exc.archetype_type == "cpu"
        assert "default_cpu" in str(exc)
        assert "cpu" in str(exc)
    
    def test_invalid_component_configuration_error(self):
        """Test InvalidComponentConfigurationError includes details."""
        exc = InvalidComponentConfigurationError("cpu", "TDP must be positive")
        
        assert isinstance(exc, DomainException)
        assert exc.component_type == "cpu"
        assert exc.reason == "TDP must be positive"
        assert "cpu" in str(exc)
        assert "TDP must be positive" in str(exc)
    
    def test_invalid_device_configuration_error(self):
        """Test InvalidDeviceConfigurationError includes reason."""
        exc = InvalidDeviceConfigurationError("Missing CPU configuration")
        
        assert isinstance(exc, DomainException)
        assert exc.reason == "Missing CPU configuration"
        assert "Missing CPU configuration" in str(exc)
    
    def test_impact_computation_error_contains_details(self):
        """Test ImpactComputationError includes computation details."""
        exc = ImpactComputationError("manufacturing", "gwp", "Missing impact factors")
        
        assert isinstance(exc, DomainException)
        assert exc.phase == "manufacturing"
        assert exc.criteria == "gwp"
        assert exc.reason == "Missing impact factors"
        assert "manufacturing" in str(exc)
        assert "gwp" in str(exc)
    
    def test_country_not_supported_error(self):
        """Test CountryNotSupportedError includes country code."""
        exc = CountryNotSupportedError("XX")
        
        assert isinstance(exc, DomainException)
        assert exc.country_code == "XX"
        assert "XX" in str(exc)
    
    def test_invalid_usage_configuration_error(self):
        """Test InvalidUsageConfigurationError includes reason."""
        exc = InvalidUsageConfigurationError("Duration cannot be negative")
        
        assert isinstance(exc, DomainException)
        assert exc.reason == "Duration cannot be negative"
        assert "Duration cannot be negative" in str(exc)
    
    def test_missing_required_data_error(self):
        """Test MissingRequiredDataError includes data type and context."""
        exc = MissingRequiredDataError("impact factor", "GWP calculation")
        
        assert isinstance(exc, DomainException)
        assert exc.data_type == "impact factor"
        assert exc.context == "GWP calculation"
        assert "impact factor" in str(exc)
        assert "GWP calculation" in str(exc)
    
    def test_exceptions_can_be_caught_as_domain_exception(self):
        """Test that all exceptions can be caught as DomainException."""
        exceptions = [
            ArchetypeNotFoundError("test", "cpu"),
            InvalidComponentConfigurationError("cpu", "test"),
            InvalidDeviceConfigurationError("test"),
            ImpactComputationError("use", "gwp", "test"),
            CountryNotSupportedError("XX"),
            InvalidUsageConfigurationError("test"),
            MissingRequiredDataError("factor", "calc"),
        ]
        
        for exc in exceptions:
            with pytest.raises(DomainException):
                raise exc