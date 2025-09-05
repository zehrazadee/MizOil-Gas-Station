from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
import json
import os

app = FastAPI()

# DB faylları
TELEMETRY_FILE = "telemetry.json"
STATE_FILE = "state_latest.json"

# JSON faylı mövcud deyilsə, boş aç
if not os.path.exists(TELEMETRY_FILE):
    with open(TELEMETRY_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(STATE_FILE):
    with open(STATE_FILE, "w") as f:
        json.dump({}, f)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Salam Zehra! FastAPI işləyir 🚀"}

# ----- Model -----
class TelemetryPayload(BaseModel):
    sequenceNumber: int
    sentAt: str
    schemaVersion: str

    # optional fields
    temperatureC_dht22: Optional[float] = None
    humidityPercent_dht22: Optional[float] = None
    pressurePa_bmp180: Optional[float] = None
    altitudeM_bmp180: Optional[float] = None
    altitudeM_gps: Optional[float] = None

    accelX_lsm303: Optional[float] = None
    accelY_lsm303: Optional[float] = None
    accelZ_lsm303: Optional[float] = None
    accelX_mpu6050: Optional[float] = None
    accelY_mpu6050: Optional[float] = None
    accelZ_mpu6050: Optional[float] = None

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
    gpsUtcTime: Optional[str] = None
    gpsSatellites: Optional[int] = None
    gpsHdop: Optional[float] = None


# ----- Helper funksiyalar -----
def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def compute_derived_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    # altitudeM_avg
    if payload.get("altitudeM_bmp180") is not None and payload.get("altitudeM_gps") is not None:
        payload["altitudeM_avg"] = (payload["altitudeM_bmp180"] + payload["altitudeM_gps"]) / 2
    elif payload.get("altitudeM_bmp180") is not None:
        payload["altitudeM_avg"] = payload["altitudeM_bmp180"]
    elif payload.get("altitudeM_gps") is not None:
        payload["altitudeM_avg"] = payload["altitudeM_gps"]

    # accel averages
    for axis in ["X", "Y", "Z"]:
        lsm = payload.get(f"accel{axis}_lsm303")
        mpu = payload.get(f"accel{axis}_mpu6050")
        if lsm is not None and mpu is not None:
            payload[f"accel{axis}_avg"] = (lsm + mpu) / 2
        elif lsm is not None:
            payload[f"accel{axis}_avg"] = lsm
        elif mpu is not None:
            payload[f"accel{axis}_avg"] = mpu

    return payload


# ----- API-lər -----

@app.post("/ingest")
def ingest(data: TelemetryPayload):
    telemetry = load_json(TELEMETRY_FILE)
    state = load_json(STATE_FILE)

    # Duplicate check (idempotency)
    if any(d["sequenceNumber"] == data.sequenceNumber for d in telemetry):
        return {"status": "duplicate", "sequenceNumber": data.sequenceNumber}

    record = data.dict()
    record["receivedAt"] = datetime.utcnow().isoformat()

    # Derived fields
    record = compute_derived_fields(record)

    # Insert telemetry history
    telemetry.append(record)
    save_json(TELEMETRY_FILE, telemetry)

    # Update state_latest (yalnız yeni olan field-ləri yenilə)
    for k, v in record.items():
        if v is not None:
            state[k] = {"value": v, "updatedAt": record["receivedAt"]}
    save_json(STATE_FILE, state)

    return {"status": "ok", "sequenceNumber": data.sequenceNumber}


@app.get("/latest")
def get_latest(maxStaleness: Optional[int] = None):
    state = load_json(STATE_FILE)
    now = datetime.utcnow()

    response = {}
    for k, v in state.items():
        if maxStaleness is not None:
            updated_at = datetime.fromisoformat(v["updatedAt"])
            age = (now - updated_at).total_seconds()
            if age > maxStaleness:
                response[k] = None
                continue
        response[k] = v["value"]

    return response


@app.get("/range")
def get_range(from_ts: str, to_ts: str, fields: Optional[str] = None):
    telemetry = load_json(TELEMETRY_FILE)
    fields_list = fields.split(",") if fields else None

    results = []
    for record in telemetry:
        sentAt = datetime.fromisoformat(record["sentAt"])
        if datetime.fromisoformat(from_ts) <= sentAt <= datetime.fromisoformat(to_ts):
            if fields_list:
                filtered = {f: record.get(f) for f in fields_list}
                filtered["sentAt"] = record["sentAt"]
                results.append(filtered)
            else:
                results.append(record)

    return results


@app.get("/health")
def health():
    return {"status": "OK"}

