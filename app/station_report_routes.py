# app/station_report_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from pydantic import BaseModel 
import logging
import io

from .database import get_db
from .reports import generate_station_report
from . import models  # FIXED: Added missing import

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["station-reports"])

# ADD THIS MODEL
class StationReportRequest(BaseModel):
    start_date: str
    end_date: str
    station1: str
    station2: str
    
@router.post("/generate-station-report")
async def generate_station_report_route(
    request: StationReportRequest,  # CHANGE TO REQUEST BODY
    db: Session = Depends(get_db)
):
    """
    Generate professional Excel report for station pair analysis
    """
    return await generate_station_report(
        request.start_date, 
        request.end_date, 
        request.station1, 
        request.station2, 
        db
    )

@router.post("/download-station-report")
async def download_station_report(
    request: StationReportRequest,
    db: Session = Depends(get_db)
):
    """
    Download Excel report for station pair analysis
    """
    try:
        logger.info(f"Received report request: {request}")
        
        result = await generate_station_report(
            request.start_date, 
            request.end_date, 
            request.station1, 
            request.station2, 
            db
        )
        
        file_stream = io.BytesIO(result["file_data"])
        
        return StreamingResponse(
            file_stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={result['filename']}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@router.get("/debug-report")
async def debug_report(
    start_date: str,
    end_date: str,
    station1: str,
    station2: str,
    db: Session = Depends(get_db)
):
    """Debug endpoint to check what data is available"""
    try:
        query = db.query(models.LocationSample).filter(
            models.LocationSample.sample_date >= start_date,
            models.LocationSample.sample_date <= end_date,
            models.LocationSample.station.in_([station1, station2])
        )
        
        samples = query.all()
        
        return {
            "total_samples": len(samples),
            "station1_count": len([s for s in samples if str(s.station) == station1]),
            "station2_count": len([s for s in samples if str(s.station) == station2]),
            "sample_dates": list(set([str(s.sample_date) for s in samples])),
            "sample_stations": list(set([str(s.station) for s in samples]))
        }
    except Exception as e:
        return {"error": str(e)}