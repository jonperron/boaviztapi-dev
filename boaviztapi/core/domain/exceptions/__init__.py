"""Domain-specific exceptions for BoaviztAPI.

These exceptions represent business rule violations and domain-level errors.
They are independent of any infrastructure or framework concerns.
"""


class DomainException(Exception):
    """Base exception for all domain-level errors."""
    pass


class ArchetypeNotFoundError(DomainException):
    """Raised when a requested archetype cannot be found."""
    
    def __init__(self, archetype_name: str, archetype_type: str):
        self.archetype_name = archetype_name
        self.archetype_type = archetype_type
        super().__init__(
            f"Archetype '{archetype_name}' not found for type '{archetype_type}'"
        )


class InvalidComponentConfigurationError(DomainException):
    """Raised when component configuration violates business rules."""
    
    def __init__(self, component_type: str, reason: str):
        self.component_type = component_type
        self.reason = reason
        super().__init__(f"Invalid {component_type} configuration: {reason}")


class InvalidDeviceConfigurationError(DomainException):
    """Raised when device configuration violates business rules."""
    
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(f"Invalid device configuration: {reason}")


class ImpactComputationError(DomainException):
    """Raised when impact computation fails."""
    
    def __init__(self, phase: str, criteria: str, reason: str):
        self.phase = phase
        self.criteria = criteria
        self.reason = reason
        super().__init__(
            f"Failed to compute {criteria} impact for {phase} phase: {reason}"
        )


class CountryNotSupportedError(DomainException):
    """Raised when impact factors are not available for a country."""
    
    def __init__(self, country_code: str):
        self.country_code = country_code
        super().__init__(
            f"Impact factors not available for country: {country_code}"
        )


class InvalidUsageConfigurationError(DomainException):
    """Raised when usage configuration violates business rules."""
    
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(f"Invalid usage configuration: {reason}")


class MissingRequiredDataError(DomainException):
    """Raised when required data for computation is missing."""
    
    def __init__(self, data_type: str, context: str):
        self.data_type = data_type
        self.context = context
        super().__init__(
            f"Missing required {data_type} data for {context}"
        )