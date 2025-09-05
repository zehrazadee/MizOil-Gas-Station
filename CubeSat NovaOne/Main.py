#!/usr/bin/env python3
"""
CubeSat Telemetry Backend System
Professional grade backend for CubeSat competition
"""

import os
import json
import logging
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from contextlib import asynccontextmanager

import asyncpg
import psycopg
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, validator
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/cubesat")

# Data Models
class TelemetryPayload(BaseModel):
    """Incoming telemetry data payload"""
    
    # Mandatory meta fields
    sequenceNumber: int = Field(..., description="Unique sequence number")
    sentAt: datetime = Field(..., description="Device timestamp")
    schemaVersion: str = Field(default="1.0", description="Schema version")
    
    # Optional environmental sensors
    temperatureC_dht22: Optional[float] = None
    humidityPercent_dht22: Optional[float] = None
    pressurePa_bmp180: Optional[float] = None
    altitudeM_bmp180: Optional[float] = None
    altitudeM_gps: Optional[float] = None
    
    # Optional acceleration sensors
    accelX_lsm303: Optional[float] = None
    accelY_lsm303: Optional[float] = None
    accelZ_lsm303: Optional[float] = None
    accelX_mpu6050: Optional[float] = None
    accelY_mpu6050: Optional[float] = None
    accelZ_mpu6050: Optional[float] = None
    
    # Optional magnetic field sensors
    magX_lsm303: Optional[float] = None
    magY_lsm303: Optional[float] = None
    magZ_lsm303: Optional[float] = None
    
    # Optional gyroscope sensors
    gyroX_mpu6050: Optional[float] = None
    gyroY_mpu6050: Optional[float] = None
    gyroZ_mpu6050: Optional[float] = None
    
    # Optional GPS data
    gpsLatitude: Optional[float] = None
    gpsLongitude: Optional[float] = None
    gpsAltitudeM: Optional[float] = None
    gpsSpeedKmh: Optional[float] = None
    gpsUtcTime: Optional[datetime] = None
    gpsSatellites: Optional[int] = None
    gpsHdop: Optional[float] = None
    
    @validator('gpsLatitude')
    def validate_latitude(cls, v):
        if v is not None and not (-90 <= v <= 90):
            logger.warning(f"Invalid latitude: {v}")
        return v
    
    @validator('gpsLongitude')
    def validate_longitude(cls, v):
        if v is not None and not (-180 <= v <= 180):
            logger.warning(f"Invalid longitude: {v}")
        return v
    
    @validator('gpsSatellites')
    def validate_satellites(cls, v):
        if v is not None and v < 0:
            logger.warning(f"Invalid satellite count: {v}")
        return v

@dataclass
class DerivedFields:
    """Calculated derived fields"""
    altitudeM_avg: Optional[float] = None
    accelX_avg: Optional[float] = None
    accelY_avg: Optional[float] = None
    accelZ_avg: Optional[float] = None

class LatestResponse(BaseModel):
    """Response model for latest data"""
    sentAt: Optional[datetime] = None
    
    # All sensor fields
    temperatureC_dht22: Optional[float] = None
    humidityPercent_dht22: Optional[float] = None
    pressurePa_bmp180: Optional[float] = None
    altitudeM_bmp180: Optional[float] = None
    altitudeM_gps: Optional[float] = None
    altitudeM_avg: Optional[float] = None
    
    accelX_lsm303: Optional[float] = None
    accelY_lsm303: Optional[float] = None
    accelZ_lsm303: Optional[float] = None
    accelX_mpu6050: Optional[float] = None
    accelY_mpu6050: Optional[float] = None
    accelZ_mpu6050: Optional[float] = None
    accelX_avg: Optional[float] = None
    accelY_avg: Optional[float] = None
    accelZ_avg: Optional[float] = None
    
    magX_lsm303: Optional[float] = None
    magY_lsm303: Optional[float] = None
    magZ_lsm303: Optional[float] = None
    
    gyroX_mpu6050: Optional[float] = None
    gyroY_mpu6050: Optional[float] = None
    gyroZ_mpu6050: Optional[float] = None
    
    gpsLatitude: Optional[float] = None
    gpsLongitude: Optional[float] = None
    gpsAltitudeM: Optional[float] = None
    gpsSpeedKmh: Optional[float] = None
    gpsUtcTime: Optional[datetime] = None
    gpsSatellites: Optional[int] = None
    gpsHdop: Optional[float] = None

class DatabaseManager:
    """Database connection and operations manager"""
    
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
    
    async def initialize(self):
        """Initialize database connection pool and create tables"""
        try:
            self.pool = await asyncpg.create_pool(DATABASE_URL, min_size=5, max_size=20)
            await self.create_tables()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    async def close(self):
        """Close database connections"""
        if self.pool:
            await self.pool.close()
            logger.info("Database connections closed")
    
    async def create_tables(self):
        """Create necessary database tables"""
        
        # Telemetry table schema
        telemetry_sql = """
        CREATE TABLE IF NOT EXISTS telemetry (
            sequenceNumber BIGINT PRIMARY KEY,
            sentAt TIMESTAMP WITH TIME ZONE NOT NULL,
            receivedAt TIMESTAMP WITH TIME ZONE NOT NULL,
            schemaVersion VARCHAR(10) NOT NULL,
            
            -- Environmental sensors
            temperatureC_dht22 DOUBLE PRECISION,
            humidityPercent_dht22 DOUBLE PRECISION,
            pressurePa_bmp180 DOUBLE PRECISION,
            altitudeM_bmp180 DOUBLE PRECISION,
            altitudeM_gps DOUBLE PRECISION,
            altitudeM_avg DOUBLE PRECISION,
            
            -- Acceleration sensors
            accelX_lsm303 DOUBLE PRECISION,
            accelY_lsm303 DOUBLE PRECISION,
            accelZ_lsm303 DOUBLE PRECISION,
            accelX_mpu6050 DOUBLE PRECISION,
            accelY_mpu6050 DOUBLE PRECISION,
            accelZ_mpu6050 DOUBLE PRECISION,
            accelX_avg DOUBLE PRECISION,
            accelY_avg DOUBLE PRECISION,
            accelZ_avg DOUBLE PRECISION,
            
            -- Magnetic field sensors
            magX_lsm303 DOUBLE PRECISION,
            magY_lsm303 DOUBLE PRECISION,
            magZ_lsm303 DOUBLE PRECISION,
            
            -- Gyroscope sensors
            gyroX_mpu6050 DOUBLE PRECISION,
            gyroY_mpu6050 DOUBLE PRECISION,
            gyroZ_mpu6050 DOUBLE PRECISION,
            
            -- GPS data
            gpsLatitude DOUBLE PRECISION,
            gpsLongitude DOUBLE PRECISION,
            gpsAltitudeM DOUBLE PRECISION,
            gpsSpeedKmh DOUBLE PRECISION,
            gpsUtcTime TIMESTAMP WITH TIME ZONE,
            gpsSatellites INTEGER,
            gpsHdop DOUBLE PRECISION
        );
        
        CREATE INDEX IF NOT EXISTS idx_telemetry_sentAt ON telemetry(sentAt DESC);
        """
        
        # State latest table schema
        state_latest_sql = """
        CREATE TABLE IF NOT EXISTS state_latest (
            id INTEGER PRIMARY KEY DEFAULT 1,
            lastSentAt TIMESTAMP WITH TIME ZONE,
            
            -- Environmental sensors
            temperatureC_dht22_value DOUBLE PRECISION,
            temperatureC_dht22_updatedAt TIMESTAMP WITH TIME ZONE,
            humidityPercent_dht22_value DOUBLE PRECISION,
            humidityPercent_dht22_updatedAt TIMESTAMP WITH TIME ZONE,
            pressurePa_bmp180_value DOUBLE PRECISION,
            pressurePa_bmp180_updatedAt TIMESTAMP WITH TIME ZONE,
            altitudeM_bmp180_value DOUBLE PRECISION,
            altitudeM_bmp180_updatedAt TIMESTAMP WITH TIME ZONE,
            altitudeM_gps_value DOUBLE PRECISION,
            altitudeM_gps_updatedAt TIMESTAMP WITH TIME ZONE,
            altitudeM_avg_value DOUBLE PRECISION,
            altitudeM_avg_updatedAt TIMESTAMP WITH TIME ZONE,
            
            -- Acceleration sensors
            accelX_lsm303_value DOUBLE PRECISION,
            accelX_lsm303_updatedAt TIMESTAMP WITH TIME ZONE,
            accelY_lsm303_value DOUBLE PRECISION,
            accelY_lsm303_updatedAt TIMESTAMP WITH TIME ZONE,
            accelZ_lsm303_value DOUBLE PRECISION,
            accelZ_lsm303_updatedAt TIMESTAMP WITH TIME ZONE,
            accelX_mpu6050_value DOUBLE PRECISION,
            accelX_mpu6050_updatedAt TIMESTAMP WITH TIME ZONE,
            accelY_mpu6050_value DOUBLE PRECISION,
            accelY_mpu6050_updatedAt TIMESTAMP WITH TIME ZONE,
            accelZ_mpu6050_value DOUBLE PRECISION,
            accelZ_mpu6050_updatedAt TIMESTAMP WITH TIME ZONE,
            accelX_avg_value DOUBLE PRECISION,
            accelX_avg_updatedAt TIMESTAMP WITH TIME ZONE,
            accelY_avg_value DOUBLE PRECISION,
            accelY_avg_updatedAt TIMESTAMP WITH TIME ZONE,
            accelZ_avg_value DOUBLE PRECISION,
            accelZ_avg_updatedAt TIMESTAMP WITH TIME ZONE,
            
            -- Magnetic field sensors
            magX_lsm303_value DOUBLE PRECISION,
            magX_lsm303_updatedAt TIMESTAMP WITH TIME ZONE,
            magY_lsm303_value DOUBLE PRECISION,
            magY_lsm303_updatedAt TIMESTAMP WITH TIME ZONE,
            magZ_lsm303_value DOUBLE PRECISION,
            magZ_lsm303_updatedAt TIMESTAMP WITH TIME ZONE,
            
            -- Gyroscope sensors
            gyroX_mpu6050_value DOUBLE PRECISION,
            gyroX_mpu6050_updatedAt TIMESTAMP WITH TIME ZONE,
            gyroY_mpu6050_value DOUBLE PRECISION,
            gyroY_mpu6050_updatedAt TIMESTAMP WITH TIME ZONE,
            gyroZ_mpu6050_value DOUBLE PRECISION,
            gyroZ_mpu6050_updatedAt TIMESTAMP WITH TIME ZONE,
            
            -- GPS data
            gpsLatitude_value DOUBLE PRECISION,
            gpsLatitude_updatedAt TIMESTAMP WITH TIME ZONE,
            gpsLongitude_value DOUBLE PRECISION,
            gpsLongitude_updatedAt TIMESTAMP WITH TIME ZONE,
            gpsAltitudeM_value DOUBLE PRECISION,
            gpsAltitudeM_updatedAt TIMESTAMP WITH TIME ZONE,
            gpsSpeedKmh_value DOUBLE PRECISION,
            gpsSpeedKmh_updatedAt TIMESTAMP WITH TIME ZONE,
            gpsUtcTime_value TIMESTAMP WITH TIME ZONE,
            gpsUtcTime_updatedAt TIMESTAMP WITH TIME ZONE,
            gpsSatellites_value INTEGER,
            gpsSatellites_updatedAt TIMESTAMP WITH TIME ZONE,
            gpsHdop_value DOUBLE PRECISION,
            gpsHdop_updatedAt TIMESTAMP WITH TIME ZONE
        );
        
        -- Initialize state_latest with one row
        INSERT INTO state_latest (id) VALUES (1) ON CONFLICT (id) DO NOTHING;
        """
        
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(telemetry_sql)
                await conn.execute(state_latest_sql)

    def calculate_derived_fields(self, payload: TelemetryPayload) -> DerivedFields:
        """Calculate derived/average fields"""
        derived = DerivedFields()
        
        # Calculate altitude average
        if payload.altitudeM_bmp180 is not None and payload.altitudeM_gps is not None:
            derived.altitudeM_avg = (payload.altitudeM_bmp180 + payload.altitudeM_gps) / 2
        elif payload.altitudeM_bmp180 is not None:
            derived.altitudeM_avg = payload.altitudeM_bmp180
        elif payload.altitudeM_gps is not None:
            derived.altitudeM_avg = payload.altitudeM_gps
        
        # Calculate acceleration averages
        if payload.accelX_lsm303 is not None and payload.accelX_mpu6050 is not None:
            derived.accelX_avg = (payload.accelX_lsm303 + payload.accelX_mpu6050) / 2
        elif payload.accelX_lsm303 is not None:
            derived.accelX_avg = payload.accelX_lsm303
        elif payload.accelX_mpu6050 is not None:
            derived.accelX_avg = payload.accelX_mpu6050
            
        if payload.accelY_lsm303 is not None and payload.accelY_mpu6050 is not None:
            derived.accelY_avg = (payload.accelY_lsm303 + payload.accelY_mpu6050) / 2
        elif payload.accelY_lsm303 is not None:
            derived.accelY_avg = payload.accelY_lsm303
        elif payload.accelY_mpu6050 is not None:
            derived.accelY_avg = payload.accelY_mpu6050
            
        if payload.accelZ_lsm303 is not None and payload.accelZ_mpu6050 is not None:
            derived.accelZ_avg = (payload.accelZ_lsm303 + payload.accelZ_mpu6050) / 2
        elif payload.accelZ_lsm303 is not None:
            derived.accelZ_avg = payload.accelZ_lsm303
        elif payload.accelZ_mpu6050 is not None:
            derived.accelZ_avg = payload.accelZ_mpu6050
        
        return derived

    async def ingest_telemetry(self, payload: TelemetryPayload) -> bool:
        """Ingest telemetry data with idempotency and atomic operations"""
        received_at = datetime.now(timezone.utc)
        derived = self.calculate_derived_fields(payload)
        
        try:
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    # Check if sequence number already exists (idempotency)
                    existing = await conn.fetchval(
                        "SELECT sequenceNumber FROM telemetry WHERE sequenceNumber = $1",
                        payload.sequenceNumber
                    )
                    
                    if existing:
                        logger.info(f"Duplicate sequence number {payload.sequenceNumber}, skipping")
                        return True
                    
                    # Insert into telemetry table
                    await conn.execute("""
                        INSERT INTO telemetry (
                            sequenceNumber, sentAt, receivedAt, schemaVersion,
                            temperatureC_dht22, humidityPercent_dht22, pressurePa_bmp180,
                            altitudeM_bmp180, altitudeM_gps, altitudeM_avg,
                            accelX_lsm303, accelY_lsm303, accelZ_lsm303,
                            accelX_mpu6050, accelY_mpu6050, accelZ_mpu6050,
                            accelX_avg, accelY_avg, accelZ_avg,
                            magX_lsm303, magY_lsm303, magZ_lsm303,
                            gyroX_mpu6050, gyroY_mpu6050, gyroZ_mpu6050,
                            gpsLatitude, gpsLongitude, gpsAltitudeM,
                            gpsSpeedKmh, gpsUtcTime, gpsSatellites, gpsHdop
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13,
                                  $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25,
                                  $26, $27, $28, $29, $30, $31, $32)
                    """,
                        payload.sequenceNumber, payload.sentAt, received_at, payload.schemaVersion,
                        payload.temperatureC_dht22, payload.humidityPercent_dht22, payload.pressurePa_bmp180,
                        payload.altitudeM_bmp180, payload.altitudeM_gps, derived.altitudeM_avg,
                        payload.accelX_lsm303, payload.accelY_lsm303, payload.accelZ_lsm303,
                        payload.accelX_mpu6050, payload.accelY_mpu6050, payload.accelZ_mpu6050,
                        derived.accelX_avg, derived.accelY_avg, derived.accelZ_avg,
                        payload.magX_lsm303, payload.magY_lsm303, payload.magZ_lsm303,
                        payload.gyroX_mpu6050, payload.gyroY_mpu6050, payload.gyroZ_mpu6050,
                        payload.gpsLatitude, payload.gpsLongitude, payload.gpsAltitudeM,
                        payload.gpsSpeedKmh, payload.gpsUtcTime, payload.gpsSatellites, payload.gpsHdop
                    )
                    
                    # Update state_latest only with provided fields
                    update_parts = ["lastSentAt = $1"]
                    values = [payload.sentAt]
                    param_idx = 2
                    
                    # Build dynamic update query for non-null fields
                    field_mapping = {
                        'temperatureC_dht22': payload.temperatureC_dht22,
                        'humidityPercent_dht22': payload.humidityPercent_dht22,
                        'pressurePa_bmp180': payload.pressurePa_bmp180,
                        'altitudeM_bmp180': payload.altitudeM_bmp180,
                        'altitudeM_gps': payload.altitudeM_gps,
                        'altitudeM_avg': derived.altitudeM_avg,
                        'accelX_lsm303': payload.accelX_lsm303,
                        'accelY_lsm303': payload.accelY_lsm303,
                        'accelZ_lsm303': payload.accelZ_lsm303,
                        'accelX_mpu6050': payload.accelX_mpu6050,
                        'accelY_mpu6050': payload.accelY_mpu6050,
                        'accelZ_mpu6050': payload.accelZ_mpu6050,
                        'accelX_avg': derived.accelX_avg,
                        'accelY_avg': derived.accelY_avg,
                        'accelZ_avg': derived.accelZ_avg,
                        'magX_lsm303': payload.magX_lsm303,
                        'magY_lsm303': payload.magY_lsm303,
                        'magZ_lsm303': payload.magZ_lsm303,
                        'gyroX_mpu6050': payload.gyroX_mpu6050,
                        'gyroY_mpu6050': payload.gyroY_mpu6050,
                        'gyroZ_mpu6050': payload.gyroZ_mpu6050,
                        'gpsLatitude': payload.gpsLatitude,
                        'gpsLongitude': payload.gpsLongitude,
                        'gpsAltitudeM': payload.gpsAltitudeM,
                        'gpsSpeedKmh': payload.gpsSpeedKmh,
                        'gpsUtcTime': payload.gpsUtcTime,
                        'gpsSatellites': payload.gpsSatellites,
                        'gpsHdop': payload.gpsHdop
                    }
                    
                    for field_name, field_value in field_mapping.items():
                        if field_value is not None:
                            update_parts.append(f"{field_name}_value = ${param_idx}")
                            update_parts.append(f"{field_name}_updatedAt = ${param_idx + 1}")
                            values.extend([field_value, received_at])
                            param_idx += 2
                    
                    if len(update_parts) > 1:  # More than just lastSentAt
                        update_query = f"UPDATE state_latest SET {', '.join(update_parts)} WHERE id = 1"
                        await conn.execute(update_query, *values)
                    
                    logger.info(f"Successfully ingested sequence {payload.sequenceNumber}")
                    return True
                    
        except Exception as e:
            logger.error(f"Failed to ingest telemetry: {e}")
            raise

    async def get_latest(self, max_staleness: Optional[int] = None) -> LatestResponse:
        """Get latest known values for all fields"""
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow("SELECT * FROM state_latest WHERE id = 1")
                
                if not row:
                    return LatestResponse()
                
                now = datetime.now(timezone.utc)
                response = LatestResponse()
                response.sentAt = row['lastsentat']
                
                # Define all fields that need to be extracted
                fields = [
                    'temperatureC_dht22', 'humidityPercent_dht22', 'pressurePa_bmp180',
                    'altitudeM_bmp180', 'altitudeM_gps', 'altitudeM_avg',
                    'accelX_lsm303', 'accelY_lsm303', 'accelZ_lsm303',
                    'accelX_mpu6050', 'accelY_mpu6050', 'accelZ_mpu6050',
                    'accelX_avg', 'accelY_avg', 'accelZ_avg',
                    'magX_lsm303', 'magY_lsm303', 'magZ_lsm303',
                    'gyroX_mpu6050', 'gyroY_mpu6050', 'gyroZ_mpu6050',
                    'gpsLatitude', 'gpsLongitude', 'gpsAltitudeM',
                    'gpsSpeedKmh', 'gpsUtcTime', 'gpsSatellites', 'gpsHdop'
                ]
                
                for field in fields:
                    value_col = f"{field.lower()}_value"
                    updated_col = f"{field.lower()}_updatedat"
                    
                    if value_col in row and row[value_col] is not None:
                        # Check staleness if max_staleness is specified
                        if max_staleness and row[updated_col]:
                            age_seconds = (now - row[updated_col]).total_seconds()
                            if age_seconds > max_staleness:
                                continue  # Skip stale data
                        
                        setattr(response, field, row[value_col])
                
                return response
                
        except Exception as e:
            logger.error(f"Failed to get latest data: {e}")
            raise

    async def get_range(self, from_time: datetime, to_time: datetime, 
                       fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Get time series data within specified range"""
        try:
            # Default to all fields if none specified
            if not fields:
                fields = ['*']
            
            field_str = ', '.join(fields)
            
            async with self.pool.acquire() as conn:
                query = f"""
                    SELECT {field_str} FROM telemetry 
                    WHERE sentAt >= $1 AND sentAt <= $2 
                    ORDER BY sentAt ASC
                """
                rows = await conn.fetch(query, from_time, to_time)
                
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Failed to get range data: {e}")
            raise

# Global database manager
db = DatabaseManager()

# FastAPI application
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    await db.initialize()
    yield
    await db.close()

app = FastAPI(
    title="CubeSat Telemetry Backend",
    description="Professional telemetry backend for CubeSat competition",
    version="1.0.0",
    lifespan=lifespan
)

# API Endpoints
@app.post("/ingest", status_code=200)
async def ingest_telemetry(payload: TelemetryPayload):
    """Ingest telemetry data from CubeSat"""
    try:
        start_time = datetime.now()
        success = await db.ingest_telemetry(payload)
        duration = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"Ingestion completed in {duration:.3f}s for sequence {payload.sequenceNumber}")
        
        return {
            "status": "success",
            "sequenceNumber": payload.sequenceNumber,
            "message": "Telemetry data ingested successfully"
        }
        
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@app.get("/latest", response_model=LatestResponse)
async def get_latest(max_staleness: Optional[int] = Query(None, description="Maximum staleness in seconds")):
    """Get latest known values for all sensors"""
    try:
        return await db.get_latest(max_staleness)
    except Exception as e:
        logger.error(f"Failed to get latest data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get latest data: {str(e)}")

@app.get("/range")
async def get_range(
    from_time: datetime = Query(..., description="Start time (ISO format)"),
    to_time: datetime = Query(..., description="End time (ISO format)"),
    fields: Optional[str] = Query(None, description="Comma-separated field names")
):
    """Get time series data within specified range"""
    try:
        field_list = fields.split(',') if fields else None
        data = await db.get_range(from_time, to_time, field_list)
        
        return {
            "status": "success",
            "count": len(data),
            "data": data
        }
        
    except Exception as e:
        logger.error(f"Failed to get range data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get range data: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "timestamp": datetime.now(timezone.utc)}

@app.get("/stream")
async def stream_telemetry():
    """Server-Sent Events stream for real-time updates"""
    async def event_stream():
        try:
            last_sequence = 0
            while True:
                # Check for new data
                async with db.pool.acquire() as conn:
                    row = await conn.fetchrow(
                        "SELECT * FROM telemetry WHERE sequenceNumber > $1 ORDER BY sequenceNumber ASC LIMIT 1",
                        last_sequence
                    )
                    
                    if row:
                        last_sequence = row['sequencenumber']
                        data = dict(row)
                        # Convert datetime objects to strings for JSON serialization
                        for key, value in data.items():
                            if isinstance(value, datetime):
                                data[key] = value.isoformat()
                        
                        yield f"data: {json.dumps(data)}\n\n"
                    
                await asyncio.sleep(1)  # Check every second
                
        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        }
    )

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return HTTPException(status_code=500, detail="Internal server error")

# Middleware for logging
@app.middleware("http")
async def log_requests(request, call_next):
    """Log all requests"""
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Duration: {process_time:.3f}s"
    )
    
    return response

# Additional utility functions
class TelemetryValidator:
    """Utility class for validating telemetry data"""
    
    @staticmethod
    def validate_ranges(payload: TelemetryPayload) -> Dict[str, str]:
        """Validate sensor value ranges"""
        warnings = {}
        
        # Temperature validation
        if payload.temperatureC_dht22 is not None:
            if payload.temperatureC_dht22 < -40 or payload.temperatureC_dht22 > 80:
                warnings['temperatureC_dht22'] = f"Temperature out of range: {payload.temperatureC_dht22}°C"
        
        # Humidity validation
        if payload.humidityPercent_dht22 is not None:
            if payload.humidityPercent_dht22 < 0 or payload.humidityPercent_dht22 > 100:
                warnings['humidityPercent_dht22'] = f"Humidity out of range: {payload.humidityPercent_dht22}%"
        
        # Pressure validation (sea level: ~101325 Pa)
        if payload.pressurePa_bmp180 is not None:
            if payload.pressurePa_bmp180 < 30000 or payload.pressurePa_bmp180 > 110000:
                warnings['pressurePa_bmp180'] = f"Pressure out of range: {payload.pressurePa_bmp180} Pa"
        
        # Acceleration validation (reasonable ranges for CubeSat)
        accel_fields = [
            'accelX_lsm303', 'accelY_lsm303', 'accelZ_lsm303',
            'accelX_mpu6050', 'accelY_mpu6050', 'accelZ_mpu6050'
        ]
        
        for field in accel_fields:
            value = getattr(payload, field, None)
            if value is not None and (value < -50 or value > 50):  # ±50 m/s² seems reasonable
                warnings[field] = f"Acceleration out of expected range: {value} m/s²"
        
        return warnings

# Database maintenance functions
class DatabaseMaintenance:
    """Database maintenance and cleanup utilities"""
    
    @staticmethod
    async def cleanup_old_records(days_to_keep: int = 30):
        """Clean up old telemetry records"""
        try:
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_to_keep)
            
            async with db.pool.acquire() as conn:
                deleted_count = await conn.fetchval(
                    "DELETE FROM telemetry WHERE receivedAt < $1",
                    cutoff_date
                )
                
                logger.info(f"Cleaned up {deleted_count} old records (older than {days_to_keep} days)")
                return deleted_count
                
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
            raise
    
    @staticmethod
    async def get_database_stats():
        """Get database statistics"""
        try:
            async with db.pool.acquire() as conn:
                stats = {}
                
                # Total record count
                stats['total_records'] = await conn.fetchval("SELECT COUNT(*) FROM telemetry")
                
                # Date range
                date_range = await conn.fetchrow(
                    "SELECT MIN(sentAt) as earliest, MAX(sentAt) as latest FROM telemetry"
                )
                stats['earliest_record'] = date_range['earliest']
                stats['latest_record'] = date_range['latest']
                
                # Records per day (last 7 days)
                stats['records_last_7_days'] = await conn.fetchval("""
                    SELECT COUNT(*) FROM telemetry 
                    WHERE sentAt >= NOW() - INTERVAL '7 days'
                """)
                
                return stats
                
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            raise

# Additional API endpoints for maintenance
@app.get("/stats")
async def get_statistics():
    """Get database and system statistics"""
    try:
        stats = await DatabaseMaintenance.get_database_stats()
        return {
            "status": "success",
            "statistics": stats
        }
    except Exception as e:
        logger.error(f"Failed to get statistics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")

@app.post("/maintenance/cleanup")
async def cleanup_database(days_to_keep: int = Query(30, description="Days of data to keep")):
    """Clean up old telemetry records"""
    try:
        deleted_count = await DatabaseMaintenance.cleanup_old_records(days_to_keep)
        return {
            "status": "success",
            "deleted_records": deleted_count,
            "days_kept": days_to_keep
        }
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")

# Configuration and startup
def create_app():
    """Create and configure the FastAPI application"""
    return app

if __name__ == "__main__":
    import sys
    from datetime import timedelta
    
    # Configuration from environment variables
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    logger.info(f"Starting CubeSat Telemetry Backend")
    logger.info(f"Database URL: {DATABASE_URL}")
    logger.info(f"Server: {HOST}:{PORT}")
    logger.info(f"Debug mode: {DEBUG}")
    
    try:
        uvicorn.run(
            "main:app" if __name__ == "__main__" else app,
            host=HOST,
            port=PORT,
            reload=DEBUG,
            log_level="info" if not DEBUG else "debug",
            access_log=True
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server failed to start: {e}")
        sys.exit(1)

#Mükəmməl! Backend sistemini tam yazdım. İndi də requirements.txt faylını yarataq ki, bütün lazımlı kitabxanaları install edə biləsən:

# CubeSat Telemetry Backend Requirements

# FastAPI and ASGI server
# fastapi==0.104.1
# uvicorn[standard]==0.24.0

# # Database
# asyncpg==0.29.0
# psycopg2-binary==2.9.9

# # Data validation and serialization
# pydantic==2.5.0
# pydantic[email]==2.5.0

# # Utilities
# python-dateutil==2.8.2
# python-multipart==0.0.6
# aiofiles==23.2.1

# # Logging and monitoring
# structlog==23.2.0

# # Optional: For development
# pytest==7.4.3
# pytest-asyncio==0.21.1
# black==23.11.0
# isort==5.12.0
# flake8==6.1.0

# # Optional: For production deployment
# gunicorn==21.2.0
# redis==5.0.1

# İndi də setup və run etmək üçün script yarataq:
# echo "=================================="

# # Check if Python 3.8+ is installed
# python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
# if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 1 ]]; then
#     echo " Python $python_version detected"
# else
#     echo " Python 3.8+ required. Please install Python 3.8 or higher"
#     exit 1
# fi

# # Create virtual environment
# echo " Creating virtual environment..."
# python3 -m venv cubesat_env
# source cubesat_env/bin/activate

# # Install dependencies
# echo " Installing dependencies..."
# pip install --upgrade pip
# pip install -r requirements.txt

# # Set default environment variables if not already set
# export DATABASE_URL=${DATABASE_URL:-"postgresql://cubesat_user:cubesat_password@localhost:5432/cubesat_db"}
# export HOST=${HOST:-"0.0.0.0"}
# export PORT=${PORT:-"8000"}
# export DEBUG=${DEBUG:-"false"}

# echo " Environment Configuration:"
# echo "   DATABASE_URL: $DATABASE_URL"
# echo "   HOST: $HOST"
# echo "   PORT: $PORT"
# echo "   DEBUG: $DEBUG"

# # Check PostgreSQL connection (optional)
# echo " Checking PostgreSQL connection..."
# python3 -c "
# import asyncio
# import asyncpg
# import os
# import sys

# async def test_connection():
#     try:
#         conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
#         await conn.close()
#         print(' PostgreSQL connection successful')
#         return True
#     except Exception as e:
#         print(f' PostgreSQL connection failed: {e}')
#         print(' Please ensure PostgreSQL is running and the DATABASE_URL is correct')
#         return False

# result = asyncio.run(test_connection())
# sys.exit(0 if result else 1)
# " || {
#     echo "    Database connection test failed, but continuing anyway..."
#     echo "   Make sure PostgreSQL is running before starting the server"
# }

# echo ""
# echo "   Setup completed successfully!"
# echo ""
# echo "   To start the server:"
# echo "   source cubesat_env/bin/activate"
# echo "   python main.py"
# echo ""
# echo "   API will be available at:"
# echo "   http://localhost:$PORT/docs (Swagger UI)"
# echo "   http://localhost:$PORT/redoc (ReDoc)"
# echo ""
# echo "   Main endpoints:"
# echo "   POST /ingest - Ingest telemetry data"
# echo "   GET  /latest - Get latest sensor values"
# echo "   GET  /range  - Get time series data"
# echo "   GET  /stream - Real-time SSE stream"
# echo "   GET  /health - Health check"
# echo "   GET  /stats  - Database statistics"

# İndi də PostgreSQL database yaratmaq üçün SQL script:
# -- CubeSat Telemetry Database Setup Script
# -- Run this as PostgreSQL superuser (postgres)

# -- Create database and user
# CREATE DATABASE cubesat_db;
# CREATE USER cubesat_user WITH PASSWORD 'cubesat_password';

# -- Grant privileges
# GRANT ALL PRIVILEGES ON DATABASE cubesat_db TO cubesat_user;

# -- Connect to the database
# \c cubesat_db;

# -- Grant schema privileges
# GRANT ALL ON SCHEMA public TO cubesat_user;
# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cubesat_user;
# GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO cubesat_user;

# -- Enable required extensions
# CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

# -- The application will create the tables automatically
# -- But you can also create them manually if needed:

# /*
# CREATE TABLE IF NOT EXISTS telemetry (
#     sequenceNumber BIGINT PRIMARY KEY,
#     sentAt TIMESTAMP WITH TIME ZONE NOT NULL,
#     receivedAt TIMESTAMP WITH TIME ZONE NOT NULL,
#     schemaVersion VARCHAR(10) NOT NULL,
    
#     -- Environmental sensors
#     temperatureC_dht22 DOUBLE PRECISION,
#     humidityPercent_dht22 DOUBLE PRECISION,
#     pressurePa_bmp180 DOUBLE PRECISION,
#     altitudeM_bmp180 DOUBLE PRECISION,
#     altitudeM_gps DOUBLE PRECISION,
#     altitudeM_avg DOUBLE PRECISION,
    
#     -- Acceleration sensors
#     accelX_lsm303 DOUBLE PRECISION,
#     accelY_lsm303 DOUBLE PRECISION,
#     accelZ_lsm303 DOUBLE PRECISION,
#     accelX_mpu6050 DOUBLE PRECISION,
#     accelY_mpu6050 DOUBLE PRECISION,
#     accelZ_mpu6050 DOUBLE PRECISION,
#     accelX_avg DOUBLE PRECISION,
#     accelY_avg DOUBLE PRECISION,
#     accelZ_avg DOUBLE PRECISION,
    
#     -- Magnetic field sensors
#     magX_lsm303 DOUBLE PRECISION,
#     magY_lsm303 DOUBLE PRECISION,
#     magZ_lsm303 DOUBLE PRECISION,
    
#     -- Gyroscope sensors
#     gyroX_mpu6050 DOUBLE PRECISION,
#     gyroY_mpu6050 DOUBLE PRECISION,
#     gyroZ_mpu6050 DOUBLE PRECISION,
    
#     -- GPS data
#     gpsLatitude DOUBLE PRECISION,
#     gpsLongitude DOUBLE PRECISION,
#     gpsAltitudeM DOUBLE PRECISION,
#     gpsSpeedKmh DOUBLE PRECISION,
#     gpsUtcTime TIMESTAMP WITH TIME ZONE,
#     gpsSatellites INTEGER,
#     gpsHdop DOUBLE PRECISION
# );

# CREATE INDEX IF NOT EXISTS idx_telemetry_sentAt ON telemetry(sentAt DESC);

# CREATE TABLE IF NOT EXISTS state_latest (
#     id INTEGER PRIMARY KEY DEFAULT 1,
#     lastSentAt TIMESTAMP WITH TIME ZONE,
    
#     -- Environmental sensors
#     temperatureC_dht22_value DOUBLE PRECISION,
#     temperatureC_dht22_updatedAt TIMESTAMP WITH TIME ZONE,
#     humidityPercent_dht22_value DOUBLE PRECISION,
#     humidityPercent_dht22_updatedAt TIMESTAMP WITH TIME ZONE,
#     pressurePa_bmp180_value DOUBLE PRECISION,
#     pressurePa_bmp180_updatedAt TIMESTAMP WITH TIME ZONE,
#     altitudeM_bmp180_value DOUBLE PRECISION,
#     altitudeM_bmp180_updatedAt TIMESTAMP WITH TIME ZONE,
#     altitudeM_gps_value DOUBLE PRECISION,
#     altitudeM_gps_updatedAt TIMESTAMP WITH TIME ZONE,
#     altitudeM_avg_value DOUBLE PRECISION,
#     altitudeM_avg_updatedAt TIMESTAMP WITH TIME ZONE,
    
#     -- Acceleration sensors
#     accelX_lsm303_value DOUBLE PRECISION,
#     accelX_lsm303_updatedAt TIMESTAMP WITH TIME ZONE,
#     accelY_lsm303_value DOUBLE PRECISION,
#     accelY_lsm303_updatedAt TIMESTAMP WITH TIME ZONE,
#     accelZ_lsm303_value DOUBLE PRECISION,
#     accelZ_lsm303_updatedAt TIMESTAMP WITH TIME ZONE,
#     accelX_mpu6050_value DOUBLE PRECISION,
#     accelX_mpu6050_updatedAt TIMESTAMP WITH TIME ZONE,
#     accelY_mpu6050_value DOUBLE PRECISION,
#     accelY_mpu6050_updatedAt TIMESTAMP WITH TIME ZONE,
#     accelZ_mpu6050_value DOUBLE PRECISION,
#     accelZ_mpu6050_updatedAt TIMESTAMP WITH TIME ZONE,
#     accelX_avg_value DOUBLE PRECISION,
#     accelX_avg_updatedAt TIMESTAMP WITH TIME ZONE,
#     accelY_avg_value DOUBLE PRECISION,
#     accelY_avg_updatedAt TIMESTAMP WITH TIME ZONE,
#     accelZ_avg_value DOUBLE PRECISION,
#     accelZ_avg_updatedAt TIMESTAMP WITH TIME ZONE,
    
#     -- Magnetic field sensors
#     magX_lsm303_value DOUBLE PRECISION,
#     magX_lsm303_updatedAt TIMESTAMP WITH TIME ZONE,
#     magY_lsm303_value DOUBLE PRECISION,
#     magY_lsm303_updatedAt TIMESTAMP WITH TIME ZONE,
#     magZ_lsm303_value DOUBLE PRECISION,
#     magZ_lsm303_updatedAt TIMESTAMP WITH TIME ZONE,
    
#     -- Gyroscope sensors
#     gyroX_mpu6050_value DOUBLE PRECISION,
#     gyroX_mpu6050_updatedAt TIMESTAMP WITH TIME ZONE,
#     gyroY_mpu6050_value DOUBLE PRECISION,
#     gyroY_mpu6050_updatedAt TIMESTAMP WITH TIME ZONE,
#     gyroZ_mpu6050_value DOUBLE PRECISION,
#     gyroZ_mpu6050_updatedAt TIMESTAMP WITH TIME ZONE,
    
#     -- GPS data
#     gpsLatitude_value DOUBLE PRECISION,
#     gpsLatitude_updatedAt TIMESTAMP WITH TIME ZONE,
#     gpsLongitude_value DOUBLE PRECISION,
#     gpsLongitude_updatedAt TIMESTAMP WITH TIME ZONE,
#     gpsAltitudeM_value DOUBLE PRECISION,
#     gpsAltitudeM_updatedAt TIMESTAMP WITH TIME ZONE,
#     gpsSpeedKmh_value DOUBLE PRECISION,
#     gpsSpeedKmh_updatedAt TIMESTAMP WITH TIME ZONE,
#     gpsUtcTime_value TIMESTAMP WITH TIME ZONE,
#     gpsUtcTime_updatedAt TIMESTAMP WITH TIME ZONE,
#     gpsSatellites_value INTEGER,
#     gpsSatellites_updatedAt TIMESTAMP WITH TIME ZONE,
#     gpsHdop_value DOUBLE PRECISION,
#     gpsHdop_updatedAt TIMESTAMP WITH TIME ZONE
# );

# -- Initialize state_latest with one row
# INSERT INTO state_latest (id) VALUES (1) ON CONFLICT (id) DO NOTHING;
# */

# -- Success message
# SELECT 'CubeSat database setup completed successfully!' as status;

# Son olaraq da test etmək üçün sample client yarataq:
# !/usr/bin/env python3
# !/usr/bin/env python3
"""
CubeSat Telemetry Backend Test Client
Test script to verify backend functionality
"""

import asyncio
import aiohttp
import json
import random
from datetime import datetime, timezone
from typing import Dict, Any
import time

class CubeSatTestClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
        self.sequence_number = 1
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def generate_sample_telemetry(self) -> Dict[str, Any]:
        """Generate realistic sample telemetry data"""
        
        # Base timestamp
        now = datetime.now(timezone.utc)
        
        # Simulate some realistic values
        payload = {
            "sequenceNumber": self.sequence_number,
            "sentAt": now.isoformat(),
            "schemaVersion": "1.0"
        }
        
        # Environmental sensors (randomly include some)
        if random.random() > 0.3:
            payload["temperatureC_dht22"] = round(random.uniform(-20, 50), 2)
        
        if random.random() > 0.3:
            payload["humidityPercent_dht22"] = round(random.uniform(10, 90), 2)
        
        if random.random() > 0.2:
            payload["pressurePa_bmp180"] = round(random.uniform(80000, 105000), 1)
        
        # Altitude sensors
        base_altitude = random.uniform(100, 50000)  # CubeSat altitude range
        if random.random() > 0.4:
            payload["altitudeM_bmp180"] = round(base_altitude + random.uniform(-100, 100), 2)
        
        if random.random() > 0.4:
            payload["altitudeM_gps"] = round(base_altitude + random.uniform(-50, 50), 2)
        
        # Acceleration sensors (LSM303 and MPU6050)
        if random.random() > 0.3:
            payload["accelX_lsm303"] = round(random.uniform(-10, 10), 3)
            payload["accelY_lsm303"] = round(random.uniform(-10, 10), 3)
            payload["accelZ_lsm303"] = round(random.uniform(-15, -5), 3)  # Gravity-influenced
        
        if random.random() > 0.3:
            payload["accelX_mpu6050"] = round(random.uniform(-10, 10), 3)
            payload["accelY_mpu6050"] = round(random.uniform(-10, 10), 3)
            payload["accelZ_mpu6050"] = round(random.uniform(-15, -5), 3)
        
        # Magnetic field sensors
        if random.random() > 0.4:
            payload["magX_lsm303"] = round(random.uniform(-100, 100), 2)
            payload["magY_lsm303"] = round(random.uniform(-100, 100), 2)
            payload["magZ_lsm303"] = round(random.uniform(-200, 200), 2)
        
        # Gyroscope sensors
        if random.random() > 0.3:
            payload["gyroX_mpu6050"] = round(random.uniform(-5, 5), 3)
            payload["gyroY_mpu6050"] = round(random.uniform(-5, 5), 3)
            payload["gyroZ_mpu6050"] = round(random.uniform(-5, 5), 3)
        
        # GPS data (sometimes available)
        if random.random() > 0.6:  # GPS not always available
            payload["gpsLatitude"] = round(random.uniform(40.0, 41.0), 6)  # Baku area
            payload["gpsLongitude"] = round(random.uniform(49.0, 50.5), 6)
            payload["gpsAltitudeM"] = base_altitude
            payload["gpsSpeedKmh"] = round(random.uniform(0, 28000), 2)  # Orbital speed
            payload["gpsUtcTime"] = now.isoformat()
            payload["gpsSatellites"] = random.randint(4, 12)
            payload["gpsHdop"] = round(random.uniform(1.0, 5.0), 2)
        
        self.sequence_number += 1
        return payload
    
    async def test_health(self):
        """Test health endpoint"""
        print(" Testing health endpoint...")
        try:
            async with self.session.get(f"{self.base_url}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f" Health check passed: {data}")
                    return True
                else:
                    print(f" Health check failed: {response.status}")
                    return False
        except Exception as e:
            print(f" Health check error: {e}")
            return False
    
    async def test_ingest(self, payload: Dict[str, Any]):
        """Test telemetry ingestion"""
        try:
            async with self.session.post(
                f"{self.base_url}/ingest",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    print(f" Ingested sequence {payload['sequenceNumber']}: {result['message']}")
                    return True
                else:
                    error_text = await response.text()
                    print(f" Ingestion failed for sequence {payload['sequenceNumber']}: {error_text}")
                    return False
                    
        except Exception as e:
            print(f" Ingestion error for sequence {payload['sequenceNumber']}: {e}")
            return False
    
    async def test_latest(self):
        """Test latest data retrieval"""
        print("\n Testing latest data retrieval...")
        try:
            async with self.session.get(f"{self.base_url}/latest") as response:
                if response.status == 200:
                    data = await response.json()
                    print(" Latest data retrieved:")
                    # Show only non-null fields
                    for key, value in data.items():
                        if value is not None:
                            print(f"   {key}: {value}")
                    return True
                else:
                    error_text = await response.text()
                    print(f" Latest data retrieval failed: {error_text}")
                    return False
                    
        except Exception as e:
            print(f" Latest data error: {e}")
            return False
    
    async def test_stats(self):
        """Test statistics endpoint"""
        print("\n Testing statistics...")
        try:
            async with self.session.get(f"{self.base_url}/stats") as response:
                if response.status == 200:
                    data = await response.json()
                    print(" Statistics retrieved:")
                    stats = data.get('statistics', {})
                    for key, value in stats.items():
                        print(f"   {key}: {value}")
                    return True
                else:
                    error_text = await response.text()
                    print(f" Statistics retrieval failed: {error_text}")
                    return False
                    
        except Exception as e:
            print(f" Statistics error: {e}")
            return False
    
    async def run_continuous_test(self, duration_seconds: int = 60, interval_seconds: float = 2.0):
        """Run continuous telemetry transmission test"""
        print(f"\n Starting continuous test for {duration_seconds} seconds...")
        print(f"   Sending telemetry every {interval_seconds} seconds")
        
        start_time = time.time()
        success_count = 0
        total_count = 0
        
        while time.time() - start_time < duration_seconds:
            payload = self.generate_sample_telemetry()
            total_count += 1
            
            if await self.test_ingest(payload):
                success_count += 1
            
            await asyncio.sleep(interval_seconds)
        
        print(f"\n Continuous test completed:")
        print(f"   Success rate: {success_count}/{total_count} ({100*success_count/total_count:.1f}%)")
        
        return success_count, total_count

async def main():
    """Main test function"""
    print(" CubeSat Telemetry Backend Test Client")
    print("=========================================\n")
    
    async with CubeSatTestClient() as client:
        
        # Test 1: Health check
        if not await client.test_health():
            print(" Backend is not healthy, aborting tests")
            return
        
        print("\n" + "="*50)
        
        # Test 2: Single telemetry ingestion
        print(" Testing single telemetry ingestion...")
        sample_payload = client.generate_sample_telemetry()
        print(f" Sending sample payload with sequence {sample_payload['sequenceNumber']}")
        print(f"   Fields included: {len([k for k, v in sample_payload.items() if v is not None])}")
        
        await client.test_ingest(sample_payload)
        
        # Test 3: Latest data retrieval
        await client.test_latest()
        
        # Test 4: Statistics
        await client.test_stats()
        
        print("\n" + "="*50)
        
        # Test 5: Idempotency (send same payload twice)
        print(" Testing idempotency...")
        print("   Sending the same payload again...")
        await client.test_ingest(sample_payload)  # Should not create duplicate
        
        # Test 6: Multiple rapid insertions
        print("\n🚄 Testing rapid insertions...")
        for i in range(5):
            payload = client.generate_sample_telemetry()
            await client.test_ingest(payload)
            await asyncio.sleep(0.1)  # Small delay
        
        # Test 7: Final statistics
        await client.test_stats()
        
        print("\n" + "="*50)
        
        # Test 8: Ask user for continuous test
        print("\n Optional: Continuous transmission test")
        try:
            user_input = input("Run continuous test? (y/N): ").strip().lower()
            if user_input in ['y', 'yes']:
                duration = input("Duration in seconds (default 30): ").strip()
                duration = int(duration) if duration.isdigit() else 30
                
                interval = input("Interval between transmissions in seconds (default 1.0): ").strip()
                interval = float(interval) if interval.replace('.', '').isdigit() else 1.0
                
                success, total = await client.run_continuous_test(duration, interval)
                
                # Final stats after continuous test
                await client.test_stats()
                await client.test_latest()
                
        except KeyboardInterrupt:
            print("\n  Test interrupted by user")
        except Exception as e:
            print(f"\n Continuous test error: {e}")
    
    print("\n All tests completed!")
    print("\n API Documentation available at:")
    print(f"   {client.base_url}/docs (Swagger UI)")
    print(f"   {client.base_url}/redoc (ReDoc)")

def run_specific_test():
    """Run specific test scenarios"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python test_client.py [test_type]")
        print("Test types: health, ingest, latest, stats, continuous, all")
        return
    
    test_type = sys.argv[1].lower()
    
    async def run_test():
        async with CubeSatTestClient() as client:
            if test_type == "health":
                await client.test_health()
            elif test_type == "ingest":
                payload = client.generate_sample_telemetry()
                await client.test_ingest(payload)
            elif test_type == "latest":
                await client.test_latest()
            elif test_type == "stats":
                await client.test_stats()
            elif test_type == "continuous":
                await client.run_continuous_test(60, 1.0)
            elif test_type == "all":
                await main()
            else:
                print(f"Unknown test type: {test_type}")
    
    asyncio.run(run_test())

# Additional utility functions
class TelemetryGenerator:
    """Advanced telemetry data generator with realistic patterns"""
    
    @staticmethod
    def generate_orbital_pattern(sequence: int) -> Dict[str, Any]:
        """Generate telemetry following orbital patterns"""
        import math
        
        # Simulate orbital period (90 minutes = 5400 seconds)
        orbital_period = 5400
        phase = (sequence * 2 * math.pi) / (orbital_period / 2)  # Assuming 2-second intervals
        
        # Base timestamp
        now = datetime.now(timezone.utc)
        
        payload = {
            "sequenceNumber": sequence,
            "sentAt": now.isoformat(),
            "schemaVersion": "1.0"
        }
        
        # Temperature variation based on solar exposure
        base_temp = -20 + 40 * (0.5 + 0.5 * math.sin(phase))  # -20°C to +20°C
        payload["temperatureC_dht22"] = round(base_temp + random.uniform(-5, 5), 2)
        
        # Pressure decreases with altitude
        altitude = 400000 + 50000 * math.sin(phase * 0.1)  # 400-450 km altitude
        payload["altitudeM_bmp180"] = round(altitude + random.uniform(-1000, 1000), 2)
        payload["altitudeM_gps"] = round(altitude + random.uniform(-500, 500), 2)
        
        # Orbital velocity variations
        orbital_speed = 27000 + 1000 * math.cos(phase * 0.1)  # ~27 km/h orbital speed
        payload["gpsSpeedKmh"] = round(orbital_speed + random.uniform(-100, 100), 2)
        
        # Acceleration due to orbital mechanics
        centripetal_accel = 8.8  # Approximate for LEO
        payload["accelX_lsm303"] = round(random.uniform(-0.5, 0.5), 3)
        payload["accelY_lsm303"] = round(random.uniform(-0.5, 0.5), 3)
        payload["accelZ_lsm303"] = round(-centripetal_accel + random.uniform(-0.2, 0.2), 3)
        
        # Gyroscope showing tumbling
        payload["gyroX_mpu6050"] = round(2 * math.sin(phase * 2), 3)
        payload["gyroY_mpu6050"] = round(2 * math.cos(phase * 2), 3)
        payload["gyroZ_mpu6050"] = round(math.sin(phase), 3)
        
        # GPS availability (sometimes blocked)
        if math.sin(phase) > -0.5:  # GPS available 75% of orbit
            payload["gpsLatitude"] = round(45 * math.sin(phase * 0.2), 6)  # Orbital track
            payload["gpsLongitude"] = round(180 * (phase / math.pi - 1), 6)
            payload["gpsAltitudeM"] = altitude
            payload["gpsUtcTime"] = now.isoformat()
            payload["gpsSatellites"] = random.randint(6, 12)
            payload["gpsHdop"] = round(random.uniform(1.0, 3.0), 2)
        
        return payload

async def run_orbital_simulation(duration_minutes: int = 5):
    """Run orbital simulation with realistic data patterns"""
    print(f"  Starting orbital simulation for {duration_minutes} minutes...")
    
    async with CubeSatTestClient() as client:
        if not await client.test_health():
            print(" Backend not available")
            return
        
        sequence = 1
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        while time.time() < end_time:
            payload = TelemetryGenerator.generate_orbital_pattern(sequence)
            await client.test_ingest(payload)
            
            sequence += 1
            await asyncio.sleep(2.0)  # 2-second telemetry interval
            
            # Show progress every 30 seconds
            if sequence % 15 == 0:
                elapsed = (time.time() - start_time) / 60
                print(f"    {elapsed:.1f} minutes elapsed, sequence {sequence}")
        
        print(f" Orbital simulation completed - {sequence} telemetry packets sent")
        await client.test_stats()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "orbital":
            duration = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            asyncio.run(run_orbital_simulation(duration))
        else:
            run_specific_test()
    else:
        asyncio.run(main())