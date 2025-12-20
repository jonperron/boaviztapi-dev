"""
Unit tests for CloudMapper.
"""
import pytest
from decimal import Decimal
from boaviztapi.adapters.driving.rest.mappers.cloud_mapper import CloudMapper
from boaviztapi.adapters.driving.rest.schemas.cloud import CloudRequestSchema
from boaviztapi.adapters.driving.rest.schemas.common import UsageSchema


class TestCloudMapper:
    """Test suite for CloudMapper."""
    
    def test_to_cloud_instance_configuration_complete(self):
        """Test converting complete cloud request to domain model."""
        request = CloudRequestSchema(
            provider="aws",
            instance_type="t3.medium"
        )
        
        cloud_config = CloudMapper.to_cloud_instance_configuration(request)
        
        assert cloud_config is not None
        assert cloud_config.provider == "aws"
        assert cloud_config.instance_type == "t3.medium"
    
    def test_to_cloud_instance_configuration_minimal(self):
        """Test converting minimal cloud request."""
        request = CloudRequestSchema(
            provider="azure"
        )
        
        cloud_config = CloudMapper.to_cloud_instance_configuration(request)
        
        assert cloud_config is not None
        assert cloud_config.provider == "azure"
        assert cloud_config.instance_type is None
    
    def test_to_cloud_instance_configuration_gcp(self):
        """Test converting GCP cloud request."""
        request = CloudRequestSchema(
            provider="gcp",
            instance_type="n1-standard-4"
        )
        
        cloud_config = CloudMapper.to_cloud_instance_configuration(request)
        
        assert cloud_config is not None
        assert cloud_config.provider == "gcp"
        assert cloud_config.instance_type == "n1-standard-4"
    
    def test_to_usage_configuration_complete(self):
        """Test converting complete usage schema to domain model."""
        usage_schema = UsageSchema(
            usage_location="USA",
            hours_life_time=8760.0,
            time_workload=75.0,
            workload={"idle": 20.0, "50%": 30.0, "100%": 50.0}
        )
        
        usage_config = CloudMapper.to_usage_configuration(usage_schema)
        
        assert usage_config is not None
        assert usage_config.usage_location == "USA"
        assert usage_config.hours_life_time == Decimal("8760.0")
        assert usage_config.time_workload == Decimal("75.0")
        assert usage_config.workload_profile is not None
        assert usage_config.workload_profile.percentages["idle"] == Decimal("20.0")
        assert usage_config.workload_profile.percentages["50%"] == Decimal("30.0")
        assert usage_config.workload_profile.percentages["100%"] == Decimal("50.0")
    
    def test_to_usage_configuration_minimal(self):
        """Test converting minimal usage schema."""
        usage_schema = UsageSchema(
            usage_location="EEE"
        )
        
        usage_config = CloudMapper.to_usage_configuration(usage_schema)
        
        assert usage_config is not None
        assert usage_config.usage_location == "EEE"
        assert usage_config.hours_life_time is None
        assert usage_config.time_workload is None
        assert usage_config.workload_profile is None
    
    def test_to_usage_configuration_none(self):
        """Test converting None usage schema."""
        usage_config = CloudMapper.to_usage_configuration(None)
        
        assert usage_config is not None
        assert usage_config.usage_location is None
        assert usage_config.hours_life_time is None
        assert usage_config.time_workload is None
        assert usage_config.workload_profile is None
    
    def test_to_usage_configuration_with_location_only(self):
        """Test converting usage schema with only location."""
        usage_schema = UsageSchema(
            usage_location="FRA"
        )
        
        usage_config = CloudMapper.to_usage_configuration(usage_schema)
        
        assert usage_config is not None
        assert usage_config.usage_location == "FRA"
        assert usage_config.hours_life_time is None
        assert usage_config.workload_profile is None
