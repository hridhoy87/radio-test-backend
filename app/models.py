# app/models.py
from sqlalchemy import Column, String, Float, Boolean, BigInteger, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .database import Base

class LocationSample(Base):
    __tablename__ = "location_samples"
    __table_args__ = {'schema': 'public'}  # ADD THIS LINE

    # Server-side primary key
    server_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Client-provided ID (from Android app) - this matches Android's 'id' field
    client_id = Column(String, unique=True, nullable=False, index=True)
    
    # Location data
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    acc = Column(Float, nullable=False, default=0.0)
    
    # Timestamps
    sample_date = Column(String, nullable=False)
    sample_time = Column(String, nullable=False)
    captured_at_utc = Column(BigInteger, nullable=False)
    
    # Communication data
    provider = Column(String, nullable=False, default="FUSED")
    freq = Column(String, nullable=False)
    rf_pwr = Column(String, nullable=False)
    comm_state = Column(String, nullable=False)
    user = Column(String, nullable=False)
    station = Column(String, nullable=False)
    
    # Device information
    device_id = Column(String, nullable=False, index=True)
    
    # === CRITICAL: ADD THESE SYNC FIELDS TO MATCH ANDROID ===
    sync = Column(Boolean, default=False, nullable=False)  # Matches Android's sync field
    attempt_count = Column(Integer, default=0, nullable=False)  # Matches Android's attempt_count
    last_error = Column(Text, nullable=True)  # Matches Android's last_error
    synced_at_utc = Column(BigInteger, nullable=True)  # Matches Android's synced_at_utc
    
    # Server metadata
    received_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed = Column(Boolean, default=False, nullable=False)