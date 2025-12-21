"""Configuration constants for the application.

This module provides constants derived from the configuration file,
ensuring all default values come from a single source of truth.
"""

from boaviztapi import config

# Time constants
HOURS_PER_YEAR = 8760.0  # Standard hours in a year
DEFAULT_LIFETIME_YEARS = 4.0  # Default device lifetime in years
DEFAULT_LIFETIME_HOURS = HOURS_PER_YEAR * DEFAULT_LIFETIME_YEARS  # 35040.0 hours

# Default values from config
DEFAULT_LOCATION = config.get("default_location", "EEE")
DEFAULT_SERVER = config.get("default_server", "platform_compute_medium")
DEFAULT_LAPTOP = config.get("default_laptop", "laptop-pro")
DEFAULT_IOT_DEVICE = config.get("default_iot_device", "iot-device-default")
DEFAULT_CRITERIA = config.get("default_criteria", ["gwp", "adp", "pe"])
DEFAULT_DURATION = config.get("default_duration")  # Usually None, triggering device-specific default

# Workload defaults
DEFAULT_WORKLOAD_PERCENTAGE = 50.0
DEFAULT_USAGE_TIME_RATIO = 1.0  # 100% usage

# Uncertainty
DEFAULT_UNCERTAINTY_PERCENTAGE = config.get("uncertainty", 10)
