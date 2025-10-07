from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
import logging
from . import models, schemas

logger = logging.getLogger(__name__)

class BulkInsertError(Exception):
    """Custom exception for bulk insert failures"""
    pass

# app/crud.py - Update the create_location_samples_bulk function
def create_location_samples_bulk(db: Session, samples: List[schemas.LocationSampleBase], device_id: str):
    """Bulk insert location samples with proper error handling"""
    successful_ids = []
    failed_samples = []
    
    try:
        for sample_data in samples:
            try:
                # Check if sample already exists (idempotency)
                existing = db.query(models.LocationSample).filter(
                    models.LocationSample.client_id == sample_data.id
                ).first()
                
                if existing:
                    logger.warning(f"Sample {sample_data.id} already exists - skipping")
                    successful_ids.append(sample_data.id)
                    continue
                
                # Create new sample - ensure all fields match
                db_sample = models.LocationSample(
                    client_id=sample_data.id,
                    lat=sample_data.lat,
                    lon=sample_data.lon,
                    acc=sample_data.acc,
                    sample_date=sample_data.sample_date,      # snake_case
                    sample_time=sample_data.sample_time,      # snake_case
                    provider=sample_data.provider,
                    freq=sample_data.freq,
                    rf_pwr=sample_data.rf_pwr,               # snake_case
                    comm_state=sample_data.comm_state,       # snake_case
                    user=sample_data.user,
                    station=sample_data.station,
                    captured_at_utc=sample_data.captured_at_utc,  # snake_case
                    device_id=device_id,
                    # Sync fields
                    sync=sample_data.sync or False,
                    attempt_count=sample_data.attempt_count or 0,
                    last_error=sample_data.last_error,
                    synced_at_utc=sample_data.synced_at_utc
                )
                
                db.add(db_sample)
                successful_ids.append(sample_data.id)
                
            except Exception as e:
                logger.error(f"Failed to process sample {getattr(sample_data, 'id', 'unknown')}: {str(e)}")
                failed_samples.append({
                    'id': getattr(sample_data, 'id', 'unknown'),
                    'error': str(e)
                })
        
        db.commit()
        logger.info(f"Bulk insert completed: {len(successful_ids)} successful, {len(failed_samples)} failed")
        return successful_ids, failed_samples
        
    except Exception as e:
        db.rollback()
        logger.error(f"Bulk insert transaction failed: {str(e)}")
        raise Exception(f"Transaction failed: {str(e)}")

    
def get_samples_by_device(db: Session, device_id: str, skip: int = 0, limit: int = 100):
    """Get samples for a specific device (for debugging/admin)"""
    return db.query(models.LocationSample).filter(
        models.LocationSample.device_id == device_id
    ).offset(skip).limit(limit).all()