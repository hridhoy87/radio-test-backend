from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
import re

class LocationSampleBase(BaseModel):
    id: str = Field(..., description="Client-generated UUID")
    lat: float = Field(..., ge=-90, le=90, description="Latitude between -90 and 90")
    lon: float = Field(..., ge=-180, le=180, description="Longitude between -180 and 180")
    acc: float = Field(0.0, ge=0, description="Accuracy in meters")
    sample_date: str = Field(..., description="Date in YYYY-MM-DD format")
    sample_time: str = Field(..., description="Time in HH:MM:SS format")
    provider: str = Field("FUSED", description="Location provider: GPS_CHIP, NETWORK, FUSED")
    freq: str = Field(..., description="Frequency value")
    rf_pwr: str = Field(..., description="RF Power value")
    comm_state: str = Field(..., description="Communication state")
    user: str = Field(..., description="User identifier")
    station: str = Field(..., description="Station identifier")
    captured_at_utc: int = Field(..., ge=0, description="Epoch milliseconds")
    sync: bool = Field(False)
    attempt_count: int = Field(0)
    last_error: Optional[str] = Field(None)
    synced_at_utc: Optional[int] = Field(None)

    @validator('sample_date')
    def validate_date_format(cls, v):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
            raise ValueError('sample_date must be in YYYY-MM-DD format')
        return v

    @validator('sample_time')
    def validate_time_format(cls, v):
        if not re.match(r'^\d{2}:\d{2}:\d{2}$', v):
            raise ValueError('sample_time must be in HH:MM:SS format')
        return v

class LocationSampleResponse(BaseModel):
    server_id: str
    client_id: str
    lat: float
    lon: float
    acc: float
    sample_date: str
    sample_time: str
    provider: str
    freq: str
    rf_pwr: str
    comm_state: str
    user: str
    station: str
    captured_at_utc: int
    device_id: str
    received_at: datetime
    processed: bool
    synced_at_utc: Optional[int] = None

    class Config:
        from_attributes = True

class BulkUploadRequest(BaseModel):
    deviceId: str = Field(..., description="Unique device identifier")
    samples: List[LocationSampleBase] = Field(..., max_items=1000, description="List of location samples")

class BulkUploadResponse(BaseModel):
    status: str = Field(..., description="success or error")
    message: str = Field(..., description="Human readable message")
    synced_ids: List[str] = Field(..., description="List of successfully synced client IDs")
    timestamp: datetime = Field(..., description="Server processing timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ErrorResponse(BaseModel):
    status: str = Field("error", description="Always 'error' for error responses")
    message: str = Field(..., description="Error description")
    details: Optional[str] = Field(None, description="Additional error details")
    timestamp: datetime = Field(..., description="Error timestamp")