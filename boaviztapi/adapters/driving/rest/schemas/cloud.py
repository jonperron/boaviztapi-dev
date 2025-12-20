"""
API schemas for cloud endpoints.
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from boaviztapi.adapters.driving.rest.schemas.common import UsageSchema


class CloudInstanceSchema(BaseModel):
    """API schema for cloud instance."""
    provider: Optional[str] = Field(None, description="Cloud provider (aws, azure, gcp)")
    instance_type: Optional[str] = Field(None, description="Instance type identifier")


class CloudRequestSchema(BaseModel):
    """API schema for cloud impact computation request."""
    provider: Optional[str] = Field(None, description="Cloud provider")
    instance_type: Optional[str] = Field(None, description="Instance type")
    usage: Optional[UsageSchema] = None
    verbose: bool = Field(True, description="Include verbose details in response")
