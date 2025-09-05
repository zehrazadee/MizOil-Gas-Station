# import asyncio
# import json
# import logging
# import sqlite3
# import threading
# import time
# from dataclasses import dataclass, asdict
# from datetime import datetime, timezone
# from typing import Optional, Dict, Any, List
# import queue
# import statistics
# from http.server import HTTPServer, BaseHTTPRequestHandler
# import urllib.parse
# import traceback

# # Logging Configuration
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('cubesat_telemetry.log'),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger('CubeSat')

# @dataclass
# class TelemetryData:
#     """Complete telemetry data structure"""
#     # Meta fields (required)
#     sequenceNumber: int
#     sentAt: str
#     receivedAt: str
#     schemaVersion: str = "1.0"
#     deviceId: str = "CUBESAT-001"
    
#     # Environment Sensors
#     temperatureC_dht22: Optional[float] = None
#     humidityPercent_dht22: Optional[float] = None
#     pressurePa_bmp180: Optional[float] = None
#     altitudeM_bmp180: Optional[float] = None
    
#     # Motion & Orientation - LSM303
#     accelX_lsm303: Optional[float] = None
#     accelY_lsm303: Optional[float] = None
#     accelZ_lsm303: Optional[float] = None
#     magX_lsm303: Optional[float] = None
#     magY_lsm303: Optional[float] = None
#     magZ_lsm303: Optional[float] = None
    
#     # Motion & Orientation - MPU6050
#     accelX_mpu6050: Optional[float] = None
#     accelY_mpu6050: Optional[float] = None
#     accelZ_mpu6050: Optional[float] = None
#     gyroX_mpu6050: Optional[float] = None
#     gyroY_mpu6050: Optional[float] = None
#     gyroZ_mpu6050: Optional[float] = None
    
#     # GPS Data
#     gpsLatitude: Optional[float] = None
#     gpsLongitude: Optional[float] = None
#     altitudeM_gps: Optional[float] = None
#     gpsSpeedKmh: Optional[float] = None
#     gpsUtcTime: Optional[str] = None
#     gpsSatellites: Optional[int] = None
#     gpsHdop: Optional[float] = None
    
#     # Derived fields (calculated)
#     altitudeM_avg: Optional[float] = None
#     accelX_avg: Optional[float] = None
#     accelY_avg: Optional[float] = None
#     accelZ_avg: Optional[float] = None

# class DatabaseManager:
#     """Professional database management with SQLite"""
    
#     def __init__(self, db_path: str = "cubesat_telemetry.db"):
#         self.db_path = db_path
#         self.lock = threading.Lock()
#         self.init_database()
    
#     def init_database(self):
#         """Initialize database tables"""
#         with sqlite3.connect(self.db_path) as conn:
#             conn.execute('''
#                 CREATE TABLE IF NOT EXISTS telemetry (
#                     sequenceNumber INTEGER PRIMARY KEY,
#                     deviceId TEXT NOT NULL,
#                     sentAt TEXT NOT NULL,
#                     receivedAt TEXT NOT NULL,
#                     schemaVersion TEXT NOT NULL,
                    
#                     -- Environment sensors
#                     temperatureC_dht22 REAL,
#                     humidityPercent_dht22 REAL,
#                     pressurePa_bmp180 REAL,
#                     altitudeM_bmp180 REAL,
                    
#                     -- Motion LSM303
#                     accelX_lsm303 REAL,
#                     accelY_lsm303 REAL,
#                     accelZ_lsm303 REAL,
#                     magX_lsm303 REAL,
#                     magY_lsm303 REAL,
#                     magZ_lsm303 REAL,
                    
#                     -- Motion MPU6050
#                     accelX_mpu6050 REAL,
#                     accelY_mpu6050 REAL,
#                     accelZ_mpu6050 REAL,
#                     gyroX_mpu6050 REAL,
#                     gyroY_mpu6050 REAL,
#                     gyroZ_mpu6050 REAL,
                    
#                     -- GPS
#                     gpsLatitude REAL,
#                     gpsLongitude REAL,
#                     altitudeM_gps REAL,
#                     gpsSpeedKmh REAL,
#                     gpsUtcTime TEXT,
#                     gpsSatellites INTEGER,
#                     gpsHdop REAL,
                    
#                     -- Derived fields
#                     altitudeM_avg REAL,
#                     accelX_avg REAL,
#                     accelY_avg REAL,
#                     accelZ_avg REAL
#                 )
#             ''')
            
#             conn.execute('''
#                 CREATE TABLE IF NOT EXISTS state_latest (
#                     field_name TEXT PRIMARY KEY,
#                     field_value TEXT,
#                     updated_at TEXT NOT NULL
#                 )
#             ''')
            
#             # Create indexes
#             conn.execute('CREATE INDEX IF NOT EXISTS idx_sentAt ON telemetry(sentAt DESC)')
#             conn.commit()
            
#         logger.info("Database initialized successfully")
    
#     def insert_telemetry(self, data: TelemetryData) -> bool:
#         """Insert telemetry data with idempotency"""
#         with self.lock:
#             try:
#                 with sqlite3.connect(self.db_path) as conn:
#                     # Check if sequence number already exists (idempotency)
#                     cursor = conn.execute(
#                         "SELECT sequenceNumber FROM telemetry WHERE sequenceNumber = ?",
#                         (data.sequenceNumber,)
#                     )
#                     if cursor.fetchone():
#                         logger.info(f"Sequence {data.sequenceNumber} already exists, skipping")
#                         return True
                    
#                     # Convert dataclass to dict for insertion
#                     data_dict = asdict(data)
                    
#                     # Prepare columns and values
#                     columns = list(data_dict.keys())
#                     placeholders = ', '.join(['?' for _ in columns])
#                     values = list(data_dict.values())
                    
#                     # Insert into telemetry table
#                     query = f"INSERT INTO telemetry ({', '.join(columns)}) VALUES ({placeholders})"
#                     conn.execute(query, values)
                    
#                     # Update state_latest for non-null fields
#                     for field_name, field_value in data_dict.items():
#                         if field_value is not None and field_name not in ['sequenceNumber', 'receivedAt']:
#                             conn.execute('''
#                                 INSERT OR REPLACE INTO state_latest (field_name, field_value, updated_at)
#                                 VALUES (?, ?, ?)
#                             ''', (field_name, str(field_value), data.sentAt))
                    
#                     conn.commit()
#                     logger.info(f"Successfully inserted sequence {data.sequenceNumber}")
#                     return True
                    
#             except Exception as e:
#                 logger.error(f"Database insertion failed: {e}")
#                 logger.error(traceback.format_exc())
#                 return False
    
#     def get_latest_state(self) -> Dict[str, Any]:
#         """Get latest known values for all fields"""
#         with self.lock:
#             try:
#                 with sqlite3.connect(self.db_path) as conn:
#                     cursor = conn.execute("SELECT field_name, field_value FROM state_latest")
#                     result = {}
#                     for field_name, field_value in cursor.fetchall():
#                         try:
#                             # Try to convert to appropriate type
#                             if field_value.replace('.', '').replace('-', '').isdigit():
#                                 result[field_name] = float(field_value) if '.' in field_value else int(field_value)
#                             else:
#                                 result[field_name] = field_value
#                         except:
#                             result[field_name] = field_value
#                     return result
#             except Exception as e:
#                 logger.error(f"Failed to get latest state: {e}")
#                 return {}

# class SensorSimulator:
#     """Simulates individual sensors with realistic data patterns"""
    
#     def __init__(self, sensor_name: str):
#         self.sensor_name = sensor_name
#         self.is_running = False
#         self.failure_rate = 0.05  # 5% chance of temporary failure
#         self.last_values = {}
    
#     def simulate_dht22(self) -> Dict[str, float]:
#         """Simulate DHT22 temperature and humidity"""
#         if self.should_fail():
#             return {}
        
#         # Realistic temperature variation (-20 to 60°C)
#         temp = 20 + 10 * (time.time() % 100) / 100 + (time.time() % 7) - 3.5
#         # Humidity (20-90%)
#         humidity = 60 + 20 * (time.time() % 50) / 50 + (time.time() % 5) - 2.5
        
#         return {
#             'temperatureC_dht22': round(temp, 2),
#             'humidityPercent_dht22': round(max(0, min(100, humidity)), 2)
#         }
    
#     def simulate_bmp180(self) -> Dict[str, float]:
#         """Simulate BMP180 pressure and altitude"""
#         if self.should_fail():
#             return {}
        
#         # Standard atmospheric pressure with variation
#         pressure = 101325 + 1000 * (time.time() % 30) / 30 - 500
#         # Altitude calculation from pressure
#         altitude = 44330 * (1 - (pressure / 101325) ** 0.1903)
        
#         return {
#             'pressurePa_bmp180': round(pressure, 1),
#             'altitudeM_bmp180': round(altitude, 2)
#         }
    
#     def simulate_lsm303(self) -> Dict[str, float]:
#         """Simulate LSM303 accelerometer and magnetometer"""
#         if self.should_fail():
#             return {}
        
#         # Accelerometer data (including gravity)
#         t = time.time()
#         accel_x = 0.1 * (t % 10) - 0.5
#         accel_y = 0.1 * (t % 8) - 0.4
#         accel_z = 9.8 + 0.2 * (t % 6) - 0.1  # Gravity + small variation
        
#         # Magnetometer data (typical Earth's magnetic field)
#         mag_x = 20 + 5 * (t % 12) / 12
#         mag_y = 30 + 5 * (t % 15) / 15
#         mag_z = 40 + 5 * (t % 18) / 18
        
#         return {
#             'accelX_lsm303': round(accel_x, 3),
#             'accelY_lsm303': round(accel_y, 3),
#             'accelZ_lsm303': round(accel_z, 3),
#             'magX_lsm303': round(mag_x, 2),
#             'magY_lsm303': round(mag_y, 2),
#             'magZ_lsm303': round(mag_z, 2)
#         }
    
#     def simulate_mpu6050(self) -> Dict[str, float]:
#         """Simulate MPU6050 accelerometer and gyroscope"""
#         if self.should_fail():
#             return {}
        
#         t = time.time()
#         # Accelerometer (slightly different from LSM303)
#         accel_x = 0.12 * (t % 9) - 0.54
#         accel_y = 0.11 * (t % 7) - 0.39
#         accel_z = 9.79 + 0.15 * (t % 5) - 0.075
        
#         # Gyroscope (angular velocity)
#         gyro_x = 2 * (t % 20) / 20 - 1
#         gyro_y = 1.5 * (t % 25) / 25 - 0.75
#         gyro_z = 3 * (t % 15) / 15 - 1.5
        
#         return {
#             'accelX_mpu6050': round(accel_x, 3),
#             'accelY_mpu6050': round(accel_y, 3),
#             'accelZ_mpu6050': round(accel_z, 3),
#             'gyroX_mpu6050': round(gyro_x, 3),
#             'gyroY_mpu6050': round(gyro_y, 3),
#             'gyroZ_mpu6050': round(gyro_z, 3)
#         }
    
#     def simulate_gps(self) -> Dict[str, Any]:
#         """Simulate GPS data"""
#         if self.should_fail():
#             return {}
        
#         t = time.time()
#         # Simulate movement around Baku area
#         base_lat = 40.4093  # Baku latitude
#         base_lon = 49.8671  # Baku longitude
        
#         lat = base_lat + 0.001 * (t % 100) / 100 - 0.0005
#         lon = base_lon + 0.001 * (t % 80) / 80 - 0.0005
#         altitude = 50 + 20 * (t % 30) / 30
#         speed = 5 + 10 * (t % 40) / 40
#         satellites = max(4, int(8 + 4 * (t % 20) / 20))
#         hdop = 0.5 + 1.5 * (t % 10) / 10
        
#         return {
#             'gpsLatitude': round(lat, 6),
#             'gpsLongitude': round(lon, 6),
#             'altitudeM_gps': round(altitude, 2),
#             'gpsSpeedKmh': round(speed, 1),
#             'gpsUtcTime': datetime.now(timezone.utc).isoformat(),
#             'gpsSatellites': satellites,
#             'gpsHdop': round(hdop, 2)
#         }
    
#     def should_fail(self) -> bool:
#         """Simulate occasional sensor failures"""
#         import random
#         return random.random() < self.failure_rate

# class TelemetryDataProcessor:
#     """Process and combine sensor data"""
    
#     @staticmethod
#     def calculate_derived_fields(data: Dict[str, Any]) -> Dict[str, float]:
#         """Calculate average values from dual sensors"""
#         derived = {}
        
#         # Average altitude
#         alt_bmp = data.get('altitudeM_bmp180')
#         alt_gps = data.get('altitudeM_gps')
#         if alt_bmp is not None and alt_gps is not None:
#             derived['altitudeM_avg'] = round((alt_bmp + alt_gps) / 2, 2)
#         elif alt_bmp is not None:
#             derived['altitudeM_avg'] = alt_bmp
#         elif alt_gps is not None:
#             derived['altitudeM_avg'] = alt_gps
        
#         # Average acceleration
#         for axis in ['X', 'Y', 'Z']:
#             lsm_val = data.get(f'accel{axis}_lsm303')
#             mpu_val = data.get(f'accel{axis}_mpu6050')
            
#             if lsm_val is not None and mpu_val is not None:
#                 derived[f'accel{axis}_avg'] = round((lsm_val + mpu_val) / 2, 3)
#             elif lsm_val is not None:
#                 derived[f'accel{axis}_avg'] = lsm_val
#             elif mpu_val is not None:
#                 derived[f'accel{axis}_avg'] = mpu_val
        
#         return derived

# class CubeSatTelemetrySystem:
#     """Main telemetry system coordinator"""
    
#     def __init__(self):
#         self.db_manager = DatabaseManager()
#         self.sequence_number = 1
#         self.data_queue = queue.Queue(maxsize=1000)
#         self.running = False
        
#         # Individual sensor simulators
#         self.sensors = {
#             'dht22': SensorSimulator('DHT22'),
#             'bmp180': SensorSimulator('BMP180'),
#             'lsm303': SensorSimulator('LSM303'),
#             'mpu6050': SensorSimulator('MPU6050'),
#             'gps': SensorSimulator('GPS')
#         }
    
#     def start_sensor_threads(self):
#         """Start individual sensor reading threads"""
#         self.running = True
        
#         def sensor_thread(sensor_name: str, read_interval: float):
#             """Individual sensor thread"""
#             sensor = self.sensors[sensor_name]
#             logger.info(f"Starting {sensor_name} thread")
            
#             while self.running:
#                 try:
#                     if sensor_name == 'dht22':
#                         data = sensor.simulate_dht22()
#                     elif sensor_name == 'bmp180':
#                         data = sensor.simulate_bmp180()
#                     elif sensor_name == 'lsm303':
#                         data = sensor.simulate_lsm303()
#                     elif sensor_name == 'mpu6050':
#                         data = sensor.simulate_mpu6050()
#                     elif sensor_name == 'gps':
#                         data = sensor.simulate_gps()
#                     else:
#                         continue
                    
#                     if data:  # Only queue if sensor provided data
#                         self.data_queue.put((sensor_name, data), timeout=1)
#                         logger.debug(f"{sensor_name} data queued: {len(data)} fields")
#                     else:
#                         logger.warning(f"{sensor_name} sensor failed to provide data")
                        
#                 except queue.Full:
#                     logger.error(f"{sensor_name} queue full, dropping data")
#                 except Exception as e:
#                     logger.error(f"{sensor_name} thread error: {e}")
                
#                 time.sleep(read_interval)
        
#         # Start threads with different intervals to simulate real sensors
#         threading.Thread(target=sensor_thread, args=('dht22', 2.0), daemon=True).start()
#         threading.Thread(target=sensor_thread, args=('bmp180', 1.5), daemon=True).start()
#         threading.Thread(target=sensor_thread, args=('lsm303', 0.1), daemon=True).start()
#         threading.Thread(target=sensor_thread, args=('mpu6050', 0.1), daemon=True).start()
#         threading.Thread(target=sensor_thread, args=('gps', 1.0), daemon=True).start()
    
#     def start_data_processor(self):
#         """Process queued sensor data and create telemetry packets"""
#         def processor_thread():
#             logger.info("Starting data processor thread")
#             current_packet = {}
#             last_send_time = time.time()
#             send_interval = 5.0  # Send packet every 5 seconds
            
#             while self.running:
#                 try:
#                     # Get sensor data with timeout
#                     try:
#                         sensor_name, data = self.data_queue.get(timeout=0.5)
#                         current_packet.update(data)
#                         logger.debug(f"Added {sensor_name} data to packet")
#                     except queue.Empty:
#                         pass
                    
#                     # Send packet if enough time has passed
#                     if time.time() - last_send_time >= send_interval:
#                         if current_packet:  # Only send if we have some data
#                             self.send_telemetry_packet(current_packet)
#                         current_packet = {}
#                         last_send_time = time.time()
                        
#                 except Exception as e:
#                     logger.error(f"Data processor error: {e}")
        
#         threading.Thread(target=processor_thread, daemon=True).start()
    
#     def send_telemetry_packet(self, sensor_data: Dict[str, Any]):
#         """Create and store telemetry packet"""
#         try:
#             # Calculate derived fields
#             derived = TelemetryDataProcessor.calculate_derived_fields(sensor_data)
#             sensor_data.update(derived)
            
#             # Create telemetry data object
#             now = datetime.now(timezone.utc)
#             telemetry = TelemetryData(
#                 sequenceNumber=self.sequence_number,
#                 sentAt=now.isoformat(),
#                 receivedAt=now.isoformat(),
#                 **sensor_data
#             )
            
#             # Store in database
#             if self.db_manager.insert_telemetry(telemetry):
#                 logger.info(f"Telemetry packet #{self.sequence_number} sent with {len(sensor_data)} fields")
#                 self.sequence_number += 1
#             else:
#                 logger.error(f"Failed to store telemetry packet #{self.sequence_number}")
                
#         except Exception as e:
#             logger.error(f"Failed to send telemetry packet: {e}")
#             logger.error(traceback.format_exc())
    
#     def get_latest_data(self) -> Dict[str, Any]:
#         """Get latest known values for all fields"""
#         return self.db_manager.get_latest_state()
    
#     def start(self):
#         """Start the complete telemetry system"""
#         logger.info("Starting CubeSat Telemetry System")
#         self.start_sensor_threads()
#         self.start_data_processor()
#         logger.info("All subsystems started successfully")
    
#     def stop(self):
#         """Stop the telemetry system"""
#         logger.info("Stopping CubeSat Telemetry System")
#         self.running = False

# class TelemetryHTTPHandler(BaseHTTPRequestHandler):
#     """HTTP API handler for telemetry system"""
    
#     def do_GET(self):
#         """Handle GET requests"""
#         try:
#             parsed_path = urllib.parse.urlparse(self.path)
#             path = parsed_path.path
            
#             logger.info(f"HTTP GET request: {path}")
            
#             if path == '/latest':
#                 # Get latest telemetry data
#                 latest_data = telemetry_system.get_latest_data()
#                 self.send_json_response(200, {
#                     'status': 'success',
#                     'data': latest_data,
#                     'timestamp': datetime.now(timezone.utc).isoformat(),
#                     'total_fields': len(latest_data)
#                 })
            
#             elif path == '/health':
#                 self.send_json_response(200, {'status': 'healthy', 'message': 'CubeSat telemetry system is running'})
            
#             elif path == '/status':
#                 latest_data = telemetry_system.get_latest_data()
#                 self.send_json_response(200, {
#                     'status': 'running',
#                     'sequence_number': telemetry_system.sequence_number,
#                     'fields_count': len(latest_data),
#                     'uptime_seconds': time.time() - start_time,
#                     'sensors_active': list(telemetry_system.sensors.keys())
#                 })
            
#             elif path == '/' or path == '/index.html':
#                 # Simple web interface
#                 html_content = self.create_web_interface()
#                 self.send_html_response(200, html_content)
            
#             else:
#                 self.send_json_response(404, {'error': 'Endpoint not found', 'available': ['/latest', '/health', '/status', '/']})
                
#         except Exception as e:
#             logger.error(f"GET request error: {e}")
#             logger.error(traceback.format_exc())
#             self.send_json_response(500, {'error': str(e)})
    
#     def create_web_interface(self) -> str:
#         """Create simple web interface"""
#         latest_data = telemetry_system.get_latest_data()
        
#         html = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <title>CubeSat Telemetry System</title>
#             <meta charset="utf-8">
#             <style>
#                 body {{ font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }}
#                 .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
#                 .header {{ text-align: center; color: #333; margin-bottom: 30px; }}
#                 .status {{ background: #4CAF50; color: white; padding: 10px; border-radius: 5px; margin-bottom: 20px; }}
#                 .data-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }}
#                 .sensor-group {{ background: #f9f9f9; padding: 15px; border-radius: 5px; border-left: 4px solid #2196F3; }}
#                 .sensor-title {{ font-weight: bold; color: #2196F3; margin-bottom: 10px; }}
#                 .data-item {{ margin: 5px 0; font-family: monospace; }}
#                 .refresh-btn {{ background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }}
#                 .endpoints {{ background: #e7f3ff; padding: 15px; border-radius: 5px; margin-top: 20px; }}
#             </style>
#         </head>
#         <body>
#             <div class="container">
#                 <div class="header">
#                     <h1> CubeSat Telemetry System</h1>
#                     <div class="status">
#                         System Running - Sequence #{telemetry_system.sequence_number} - {len(latest_data)} Active Fields
#                     </div>
#                 </div>
                
#                 <button class="refresh-btn" onclick="location.reload()"> Refresh Data</button>
                
#                 <div class="data-grid">
#                     <div class="sensor-group">
#                         <div class="sensor-title"> Environment (DHT22)</div>
#                         <div class="data-item">Temperature: {latest_data.get('temperatureC_dht22', 'No data')} °C</div>
#                         <div class="data-item">Humidity: {latest_data.get('humidityPercent_dht22', 'No data')} %</div>
#                     </div>
                    
#                     <div class="sensor-group">
#                         <div class="sensor-title"> Pressure (BMP180)</div>
#                         <div class="data-item">Pressure: {latest_data.get('pressurePa_bmp180', 'No data')} Pa</div>
#                         <div class="data-item">Altitude: {latest_data.get('altitudeM_bmp180', 'No data')} m</div>
#                     </div>
                    
#                     <div class="sensor-group">
#                         <div class="sensor-title"> Motion (LSM303)</div>
#                         <div class="data-item">Accel X: {latest_data.get('accelX_lsm303', 'No data')} m/s²</div>
#                         <div class="data-item">Accel Y: {latest_data.get('accelY_lsm303', 'No data')} m/s²</div>
#                         <div class="data-item">Accel Z: {latest_data.get('accelZ_lsm303', 'No data')} m/s²</div>
#                         <div class="data-item">Mag X: {latest_data.get('magX_lsm303', 'No data')} µT</div>
#                         <div class="data-item">Mag Y: {latest_data.get('magY_lsm303', 'No data')} µT</div>
#                         <div class="data-item">Mag Z: {latest_data.get('magZ_lsm303', 'No data')} µT</div>
#                     </div>
                    
#                     <div class="sensor-group">
#                         <div class="sensor-title"> Motion (MPU6050)</div>
#                         <div class="data-item">Accel X: {latest_data.get('accelX_mpu6050', 'No data')} m/s²</div>
#                         <div class="data-item">Accel Y: {latest_data.get('accelY_mpu6050', 'No data')} m/s²</div>
#                         <div class="data-item">Accel Z: {latest_data.get('accelZ_mpu6050', 'No data')} m/s²</div>
#                         <div class="data-item">Gyro X: {latest_data.get('gyroX_mpu6050', 'No data')} °/s</div>
#                         <div class="data-item">Gyro Y: {latest_data.get('gyroY_mpu6050', 'No data')} °/s</div>
#                         <div class="data-item">Gyro Z: {latest_data.get('gyroZ_mpu6050', 'No data')} °/s</div>
#                     </div>
                    
#                     <div class="sensor-group">
#                         <div class="sensor-title"> GPS Location</div>
#                         <div class="data-item">Latitude: {latest_data.get('gpsLatitude', 'No data')}</div>
#                         <div class="data-item">Longitude: {latest_data.get('gpsLongitude', 'No data')}</div>
#                         <div class="data-item">Altitude: {latest_data.get('altitudeM_gps', 'No data')} m</div>
#                         <div class="data-item">Speed: {latest_data.get('gpsSpeedKmh', 'No data')} km/h</div>
#                         <div class="data-item">Satellites: {latest_data.get('gpsSatellites', 'No data')}</div>
#                         <div class="data-item">HDOP: {latest_data.get('gpsHdop', 'No data')}</div>
#                     </div>
                    
#                     <div class="sensor-group">
#                         <div class="sensor-title"> Averages</div>
#                         <div class="data-item">Avg Altitude: {latest_data.get('altitudeM_avg', 'No data')} m</div>
#                         <div class="data-item">Avg Accel X: {latest_data.get('accelX_avg', 'No data')} m/s²</div>
#                         <div class="data-item">Avg Accel Y: {latest_data.get('accelY_avg', 'No data')} m/s²</div>
#                         <div class="data-item">Avg Accel Z: {latest_data.get('accelZ_avg', 'No data')} m/s²</div>
#                     </div>
#                 </div>
                
#                 <div class="endpoints">
#                     <h3>API Endpoints:</h3>
#                     <p><a href="/latest">/latest</a> - JSON data</p>
#                     <p><a href="/health">/health</a> - Health check</p>
#                     <p><a href="/status">/status</a> - System status</p>
#                 </div>
#             </div>
#         </body>
#         </html>
#         """
#         return html
    
#     def send_json_response(self, status_code: int, data: Dict[str, Any]):
#         """Send JSON response"""
#         response = json.dumps(data, indent=2, ensure_ascii=False)
#         self.send_response(status_code)
#         self.send_header('Content-type', 'application/json; charset=utf-8')
#         self.send_header('Content-length', str(len(response.encode('utf-8'))))
#         self.send_header('Access-Control-Allow-Origin', '*')
#         self.end_headers()
#         self.wfile.write(response.encode('utf-8'))
    
#     def send_html_response(self, status_code: int, html_content: str):
#         """Send HTML response"""
#         self.send_response(status_code)
#         self.send_header('Content-type', 'text/html; charset=utf-8')
#         self.send_header('Content-length', str(len(html_content.encode('utf-8'))))
#         self.end_headers()
#         self.wfile.write(html_content.encode('utf-8'))
    
#     def log_message(self, format, *args):
#         """Override to use our logger"""
#         logger.info(f"HTTP {format % args}")

# def start_http_server(port: int = 8080):
#     """Start HTTP API server with multiple port attempts"""
#     ports_to_try = [8080, 8081, 8082, 8000, 9000]
    
#     for attempt_port in ports_to_try:
#         try:
#             server = HTTPServer(('127.0.0.1', attempt_port), TelemetryHTTPHandler)
#             logger.info(f"HTTP server started on http://127.0.0.1:{attempt_port}")
#             logger.info(f"Also try: http://localhost:{attempt_port}")
#             logger.info("Available endpoints:")
#             logger.info(f"  http://127.0.0.1:{attempt_port}/         - Web interface")
#             logger.info(f"  http://127.0.0.1:{attempt_port}/latest   - Latest telemetry data (JSON)")
#             logger.info(f"  http://127.0.0.1:{attempt_port}/health   - System health check")
#             logger.info(f"  http://127.0.0.1:{attempt_port}/status   - System status")
            
#             def server_thread():
#                 try:
#                     server.serve_forever()
#                 except Exception as e:
#                     logger.error(f"Server thread error: {e}")
            
#             threading.Thread(target=server_thread, daemon=True).start()
#             return server
            
#         except OSError as e:
#             if "Address already in use" in str(e) or "Only one usage" in str(e):
#                 logger.warning(f"Port {attempt_port} already in use, trying next...")
#                 continue
#             else:
#                 logger.error(f"Failed to start server on port {attempt_port}: {e}")
    
#     logger.error("Failed to start HTTP server on any port!")
#     return None

# def main():
#     """Main entry point"""
#     global telemetry_system, start_time
#     start_time = time.time()
    
#     logger.info("="*60)
#     logger.info("CUBESAT TELEMETRY SYSTEM - PROFESSIONAL EDITION")
#     logger.info("="*60)
    
#     try:
#         # Initialize telemetry system
#         telemetry_system = CubeSatTelemetrySystem()
        
#         # Start HTTP server
#         http_server = start_http_server(8080)
        
#         # Start telemetry system
#         telemetry_system.start()
        
#         logger.info("System Status:")
#         logger.info(f"   • Database: SQLite")
#         logger.info(f"   • Sensors: 5 active (DHT22, BMP180, LSM303, MPU6050, GPS)")
#         logger.info(f"   • API Server: http://localhost:8080")
#         logger.info(f"   • Data Collection: Every 5 seconds")
#         logger.info("="*60)
        
#         # Keep main thread alive
#         try:
#             while True:
#                 time.sleep(10)
#                 latest = telemetry_system.get_latest_data()
#                 logger.info(f"Active fields: {len(latest)}, Sequence: #{telemetry_system.sequence_number}")
        
#         except KeyboardInterrupt:
#             logger.info("\nShutdown requested by user")
        
#     except Exception as e:
#         logger.error(f"System failure: {e}")
#         logger.error(traceback.format_exc())
    
#     finally:
#         if 'telemetry_system' in locals():
#             telemetry_system.stop()
#         logger.info("Shutdown complete")

# if __name__ == "__main__":
#     main()




import asyncio
import json
import logging
import threading
import time
import statistics
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import queue
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import traceback
import random

# PostgreSQL imports
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    import sqlite3

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cubesat_telemetry.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('CubeSat')

@dataclass
class TelemetryData:
    """Complete telemetry data structure with ALL sensors"""
    # Meta fields (required)
    sequenceNumber: int
    sentAt: str
    receivedAt: str
    schemaVersion: str = "1.0"
    deviceId: str = "CUBESAT-001"
    
    # Environment Sensors - DHT22
    temperatureC_dht22: Optional[float] = None
    humidityPercent_dht22: Optional[float] = None
    
    # Environment Sensors - BME280
    temperatureC_bme280: Optional[float] = None
    humidityPercent_bme280: Optional[float] = None
    pressurePa_bme280: Optional[float] = None
    altitudeM_bme280: Optional[float] = None
    
    # Pressure Sensor - BMP180
    pressurePa_bmp180: Optional[float] = None
    altitudeM_bmp180: Optional[float] = None
    
    # Motion & Orientation - LSM303
    accelX_lsm303: Optional[float] = None
    accelY_lsm303: Optional[float] = None
    accelZ_lsm303: Optional[float] = None
    magX_lsm303: Optional[float] = None
    magY_lsm303: Optional[float] = None
    magZ_lsm303: Optional[float] = None
    
    # Motion & Orientation - MPU6050
    accelX_mpu6050: Optional[float] = None
    accelY_mpu6050: Optional[float] = None
    accelZ_mpu6050: Optional[float] = None
    gyroX_mpu6050: Optional[float] = None
    gyroY_mpu6050: Optional[float] = None
    gyroZ_mpu6050: Optional[float] = None
    
    # GPS Data
    gpsLatitude: Optional[float] = None
    gpsLongitude: Optional[float] = None
    altitudeM_gps: Optional[float] = None
    gpsSpeedKmh: Optional[float] = None
    gpsUtcTime: Optional[str] = None
    gpsSatellites: Optional[int] = None
    gpsHdop: Optional[float] = None
    
    # Derived fields (calculated server-side)
    altitudeM_avg: Optional[float] = None
    accelX_avg: Optional[float] = None
    accelY_avg: Optional[float] = None
    accelZ_avg: Optional[float] = None
    temperatureC_avg: Optional[float] = None
    humidityPercent_avg: Optional[float] = None
    pressurePa_avg: Optional[float] = None

class DatabaseManager:
    """Professional PostgreSQL database management with SQLite fallback"""
    
    def __init__(self, use_postgres: bool = True):
        self.use_postgres = use_postgres and POSTGRES_AVAILABLE
        self.lock = threading.Lock()
        
        if self.use_postgres:
            self.db_config = {
                'host': 'localhost',
                'database': 'cubesat_telemetry',
                'user': 'postgres',
                'password': 'password',
                'port': 5432
            }
            logger.info("Using PostgreSQL database")
        else:
            self.db_path = "cubesat_telemetry.db"
            logger.info("Using SQLite database (fallback)")
        
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        if self.use_postgres:
            return psycopg2.connect(**self.db_config)
        else:
            return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database tables"""
        try:
            if self.use_postgres:
                self.init_postgresql()
            else:
                self.init_sqlite()
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            if self.use_postgres:
                logger.info("Falling back to SQLite...")
                self.use_postgres = False
                self.init_sqlite()
    
    def init_postgresql(self):
        """Initialize PostgreSQL tables"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                # Main telemetry table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS telemetry (
                        sequenceNumber BIGINT PRIMARY KEY,
                        deviceId VARCHAR(50) NOT NULL,
                        sentAt TIMESTAMP WITH TIME ZONE NOT NULL,
                        receivedAt TIMESTAMP WITH TIME ZONE NOT NULL,
                        schemaVersion VARCHAR(10) NOT NULL,
                        
                        -- Environment sensors DHT22
                        temperatureC_dht22 REAL,
                        humidityPercent_dht22 REAL,
                        
                        -- Environment sensors BME280
                        temperatureC_bme280 REAL,
                        humidityPercent_bme280 REAL,
                        pressurePa_bme280 REAL,
                        altitudeM_bme280 REAL,
                        
                        -- Pressure sensor BMP180
                        pressurePa_bmp180 REAL,
                        altitudeM_bmp180 REAL,
                        
                        -- Motion LSM303
                        accelX_lsm303 REAL,
                        accelY_lsm303 REAL,
                        accelZ_lsm303 REAL,
                        magX_lsm303 REAL,
                        magY_lsm303 REAL,
                        magZ_lsm303 REAL,
                        
                        -- Motion MPU6050
                        accelX_mpu6050 REAL,
                        accelY_mpu6050 REAL,
                        accelZ_mpu6050 REAL,
                        gyroX_mpu6050 REAL,
                        gyroY_mpu6050 REAL,
                        gyroZ_mpu6050 REAL,
                        
                        -- GPS
                        gpsLatitude DOUBLE PRECISION,
                        gpsLongitude DOUBLE PRECISION,
                        altitudeM_gps REAL,
                        gpsSpeedKmh REAL,
                        gpsUtcTime TIMESTAMP WITH TIME ZONE,
                        gpsSatellites INTEGER,
                        gpsHdop REAL,
                        
                        -- Derived fields
                        altitudeM_avg REAL,
                        accelX_avg REAL,
                        accelY_avg REAL,
                        accelZ_avg REAL,
                        temperatureC_avg REAL,
                        humidityPercent_avg REAL,
                        pressurePa_avg REAL
                    )
                ''')
                
                # State latest table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS state_latest (
                        field_name VARCHAR(50) PRIMARY KEY,
                        field_value TEXT,
                        updated_at TIMESTAMP WITH TIME ZONE NOT NULL
                    )
                ''')
                
                # Create indexes
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_sentAt ON telemetry(sentAt DESC)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_deviceId ON telemetry(deviceId)')
                
            conn.commit()
            logger.info("PostgreSQL database initialized successfully")
    
    def init_sqlite(self):
        """Initialize SQLite tables (fallback)"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS telemetry (
                    sequenceNumber INTEGER PRIMARY KEY,
                    deviceId TEXT NOT NULL,
                    sentAt TEXT NOT NULL,
                    receivedAt TEXT NOT NULL,
                    schemaVersion TEXT NOT NULL,
                    
                    -- Environment sensors DHT22
                    temperatureC_dht22 REAL,
                    humidityPercent_dht22 REAL,
                    
                    -- Environment sensors BME280
                    temperatureC_bme280 REAL,
                    humidityPercent_bme280 REAL,
                    pressurePa_bme280 REAL,
                    altitudeM_bme280 REAL,
                    
                    -- Pressure sensor BMP180
                    pressurePa_bmp180 REAL,
                    altitudeM_bmp180 REAL,
                    
                    -- Motion LSM303
                    accelX_lsm303 REAL,
                    accelY_lsm303 REAL,
                    accelZ_lsm303 REAL,
                    magX_lsm303 REAL,
                    magY_lsm303 REAL,
                    magZ_lsm303 REAL,
                    
                    -- Motion MPU6050
                    accelX_mpu6050 REAL,
                    accelY_mpu6050 REAL,
                    accelZ_mpu6050 REAL,
                    gyroX_mpu6050 REAL,
                    gyroY_mpu6050 REAL,
                    gyroZ_mpu6050 REAL,
                    
                    -- GPS
                    gpsLatitude REAL,
                    gpsLongitude REAL,
                    altitudeM_gps REAL,
                    gpsSpeedKmh REAL,
                    gpsUtcTime TEXT,
                    gpsSatellites INTEGER,
                    gpsHdop REAL,
                    
                    -- Derived fields
                    altitudeM_avg REAL,
                    accelX_avg REAL,
                    accelY_avg REAL,
                    accelZ_avg REAL,
                    temperatureC_avg REAL,
                    humidityPercent_avg REAL,
                    pressurePa_avg REAL
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS state_latest (
                    field_name TEXT PRIMARY KEY,
                    field_value TEXT,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            # Create indexes
            conn.execute('CREATE INDEX IF NOT EXISTS idx_sentAt ON telemetry(sentAt DESC)')
            conn.commit()
            
        logger.info("SQLite database initialized successfully")
    
    def insert_telemetry(self, data: TelemetryData) -> bool:
        """Insert telemetry data with idempotency"""
        with self.lock:
            try:
                if self.use_postgres:
                    return self._insert_postgresql(data)
                else:
                    return self._insert_sqlite(data)
            except Exception as e:
                logger.error(f"Database insertion failed: {e}")
                return False
    
    def _insert_postgresql(self, data: TelemetryData) -> bool:
        """PostgreSQL insertion"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                # Check idempotency
                cursor.execute(
                    "SELECT sequenceNumber FROM telemetry WHERE sequenceNumber = %s",
                    (data.sequenceNumber,)
                )
                if cursor.fetchone():
                    logger.info(f"Sequence {data.sequenceNumber} already exists")
                    return True
                
                # Convert dataclass to dict
                data_dict = asdict(data)
                
                # Prepare insertion
                columns = list(data_dict.keys())
                placeholders = ', '.join(['%s' for _ in columns])
                values = list(data_dict.values())
                
                # Insert into telemetry
                query = f"INSERT INTO telemetry ({', '.join(columns)}) VALUES ({placeholders})"
                cursor.execute(query, values)
                
                # Update state_latest
                for field_name, field_value in data_dict.items():
                    if field_value is not None and field_name not in ['sequenceNumber', 'receivedAt']:
                        cursor.execute('''
                            INSERT INTO state_latest (field_name, field_value, updated_at)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (field_name) DO UPDATE SET
                            field_value = EXCLUDED.field_value,
                            updated_at = EXCLUDED.updated_at
                        ''', (field_name, str(field_value), data.sentAt))
                
                conn.commit()
                logger.info(f"PostgreSQL: Successfully inserted sequence {data.sequenceNumber}")
                return True
    
    def _insert_sqlite(self, data: TelemetryData) -> bool:
        """SQLite insertion"""
        with sqlite3.connect(self.db_path) as conn:
            # Check idempotency
            cursor = conn.execute(
                "SELECT sequenceNumber FROM telemetry WHERE sequenceNumber = ?",
                (data.sequenceNumber,)
            )
            if cursor.fetchone():
                logger.info(f"Sequence {data.sequenceNumber} already exists")
                return True
            
            # Convert dataclass to dict
            data_dict = asdict(data)
            
            # Prepare insertion
            columns = list(data_dict.keys())
            placeholders = ', '.join(['?' for _ in columns])
            values = list(data_dict.values())
            
            # Insert into telemetry
            query = f"INSERT INTO telemetry ({', '.join(columns)}) VALUES ({placeholders})"
            conn.execute(query, values)
            
            # Update state_latest
            for field_name, field_value in data_dict.items():
                if field_value is not None and field_name not in ['sequenceNumber', 'receivedAt']:
                    conn.execute('''
                        INSERT OR REPLACE INTO state_latest (field_name, field_value, updated_at)
                        VALUES (?, ?, ?)
                    ''', (field_name, str(field_value), data.sentAt))
            
            conn.commit()
            logger.info(f"SQLite: Successfully inserted sequence {data.sequenceNumber}")
            return True
    
    def get_latest_state(self) -> Dict[str, Any]:
        """Get latest known values for all fields"""
        with self.lock:
            try:
                if self.use_postgres:
                    return self._get_latest_postgresql()
                else:
                    return self._get_latest_sqlite()
            except Exception as e:
                logger.error(f"Failed to get latest state: {e}")
                return {}
    
    def _get_latest_postgresql(self) -> Dict[str, Any]:
        """PostgreSQL latest state"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT field_name, field_value FROM state_latest")
                result = {}
                for row in cursor.fetchall():
                    field_name, field_value = row['field_name'], row['field_value']
                    result[field_name] = self._convert_value(field_value)
                return result
    
    def _get_latest_sqlite(self) -> Dict[str, Any]:
        """SQLite latest state"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT field_name, field_value FROM state_latest")
            result = {}
            for field_name, field_value in cursor.fetchall():
                result[field_name] = self._convert_value(field_value)
            return result
    
    def _convert_value(self, value: str) -> Any:
        """Convert string value to appropriate type"""
        try:
            if '.' in value:
                return float(value)
            elif value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                return int(value)
            else:
                return value
        except:
            return value

class SensorSimulator:
    """Advanced sensor simulator with realistic behavior"""
    
    def __init__(self, sensor_name: str):
        self.sensor_name = sensor_name
        self.failure_rate = 0.03  # 3% chance of failure
        self.noise_level = 0.02
        self.last_values = {}
        self.calibration_offset = random.uniform(-0.1, 0.1)
    
    def add_noise(self, value: float, noise_factor: float = 1.0) -> float:
        """Add realistic sensor noise"""
        noise = random.gauss(0, self.noise_level * noise_factor)
        return value + noise + self.calibration_offset * 0.1
    
    def should_fail(self) -> bool:
        """Simulate occasional sensor failures"""
        return random.random() < self.failure_rate
    
    def simulate_dht22(self) -> Dict[str, float]:
        """Simulate DHT22 temperature and humidity sensor"""
        if self.should_fail():
            logger.warning("DHT22 sensor failure simulated")
            return {}
        
        t = time.time()
        # Temperature varies with time of day simulation
        base_temp = 22 + 8 * math.sin((t % 86400) / 86400 * 2 * math.pi)  # Daily cycle
        temp = self.add_noise(base_temp, 0.5)
        
        # Humidity inversely related to temperature
        humidity = 70 - (temp - 22) * 2 + self.add_noise(0, 5)
        humidity = max(20, min(95, humidity))
        
        return {
            'temperatureC_dht22': round(temp, 2),
            'humidityPercent_dht22': round(humidity, 1)
        }
    
    def simulate_bme280(self) -> Dict[str, float]:
        """Simulate BME280 environmental sensor"""
        if self.should_fail():
            logger.warning("BME280 sensor failure simulated")
            return {}
        
        t = time.time()
        # Slightly different readings than DHT22
        base_temp = 22.5 + 7.5 * math.sin((t % 86400) / 86400 * 2 * math.pi)
        temp = self.add_noise(base_temp, 0.3)
        
        humidity = 68 - (temp - 22) * 1.8 + self.add_noise(0, 3)
        humidity = max(15, min(90, humidity))
        
        # Pressure with altitude variation
        base_pressure = 101325 - 50 * math.sin(t / 3600)  # Slow pressure changes
        pressure = self.add_noise(base_pressure, 100)
        
        # Calculate altitude from pressure
        altitude = 44330 * (1 - (pressure / 101325) ** 0.1903)
        
        return {
            'temperatureC_bme280': round(temp, 2),
            'humidityPercent_bme280': round(humidity, 1),
            'pressurePa_bme280': round(pressure, 1),
            'altitudeM_bme280': round(altitude, 2)
        }
    
    def simulate_bmp180(self) -> Dict[str, float]:
        """Simulate BMP180 pressure sensor"""
        if self.should_fail():
            logger.warning("BMP180 sensor failure simulated")
            return {}
        
        t = time.time()
        # Different pressure reading than BME280
        base_pressure = 101300 - 30 * math.sin(t / 3600 + math.pi/4)
        pressure = self.add_noise(base_pressure, 80)
        
        # Calculate altitude
        altitude = 44330 * (1 - (pressure / 101325) ** 0.1903)
        
        return {
            'pressurePa_bmp180': round(pressure, 1),
            'altitudeM_bmp180': round(altitude, 2)
        }
    
    def simulate_lsm303(self) -> Dict[str, float]:
        """Simulate LSM303 accelerometer and magnetometer"""
        if self.should_fail():
            logger.warning("LSM303 sensor failure simulated")
            return {}
        
        t = time.time()
        # Accelerometer with movement simulation
        accel_x = self.add_noise(0.1 * math.sin(t * 0.5), 0.02)
        accel_y = self.add_noise(0.15 * math.cos(t * 0.3), 0.02)
        accel_z = self.add_noise(9.81 + 0.1 * math.sin(t * 0.2), 0.05)  # Gravity + vibration
        
        # Magnetometer (Earth's magnetic field with variation)
        mag_x = self.add_noise(22.5 + 2 * math.sin(t * 0.1), 0.5)
        mag_y = self.add_noise(31.2 + 2 * math.cos(t * 0.15), 0.5)
        mag_z = self.add_noise(42.8 + 1.5 * math.sin(t * 0.08), 0.4)
        
        return {
            'accelX_lsm303': round(accel_x, 3),
            'accelY_lsm303': round(accel_y, 3),
            'accelZ_lsm303': round(accel_z, 3),
            'magX_lsm303': round(mag_x, 2),
            'magY_lsm303': round(mag_y, 2),
            'magZ_lsm303': round(mag_z, 2)
        }
    
    def simulate_mpu6050(self) -> Dict[str, float]:
        """Simulate MPU6050 accelerometer and gyroscope"""
        if self.should_fail():
            logger.warning("MPU6050 sensor failure simulated")
            return {}
        
        t = time.time()
        # Accelerometer (slightly different calibration than LSM303)
        accel_x = self.add_noise(0.08 * math.sin(t * 0.6), 0.025)
        accel_y = self.add_noise(0.12 * math.cos(t * 0.4), 0.025)
        accel_z = self.add_noise(9.78 + 0.08 * math.sin(t * 0.25), 0.04)
        
        # Gyroscope (angular velocity)
        gyro_x = self.add_noise(1.2 * math.sin(t * 0.2), 0.1)
        gyro_y = self.add_noise(0.8 * math.cos(t * 0.18), 0.1)
        gyro_z = self.add_noise(1.5 * math.sin(t * 0.12), 0.12)
        
        return {
            'accelX_mpu6050': round(accel_x, 3),
            'accelY_mpu6050': round(accel_y, 3),
            'accelZ_mpu6050': round(accel_z, 3),
            'gyroX_mpu6050': round(gyro_x, 3),
            'gyroY_mpu6050': round(gyro_y, 3),
            'gyroZ_mpu6050': round(gyro_z, 3)
        }
    
    def simulate_gps(self) -> Dict[str, Any]:
        """Simulate GPS receiver"""
        if self.should_fail():
            logger.warning("GPS sensor failure simulated")
            return {}
        
        t = time.time()
        # Simulate movement around Baku
        base_lat = 40.4093
        base_lon = 49.8671
        
        # Circular movement pattern
        radius = 0.002  # About 200m radius
        angle = (t / 60) % (2 * math.pi)  # Complete circle every minute
        
        lat = base_lat + radius * math.sin(angle) + self.add_noise(0, 0.0001)
        lon = base_lon + radius * math.cos(angle) + self.add_noise(0, 0.0001)
        
        altitude = 120 + 15 * math.sin(t / 30) + self.add_noise(0, 2)
        speed = 15 + 5 * math.sin(t / 20) + self.add_noise(0, 1)
        speed = max(0, speed)
        
        # Satellite count varies
        satellites = max(4, int(9 + 3 * math.sin(t / 100)))
        hdop = 0.8 + 0.4 * math.sin(t / 200)
        
        return {
            'gpsLatitude': round(lat, 6),
            'gpsLongitude': round(lon, 6),
            'altitudeM_gps': round(altitude, 2),
            'gpsSpeedKmh': round(speed, 1),
            'gpsUtcTime': datetime.now(timezone.utc).isoformat(),
            'gpsSatellites': satellites,
            'gpsHdop': round(hdop, 2)
        }

class TelemetryDataProcessor:
    """Advanced data processing with all sensor fusion"""
    
    @staticmethod
    def calculate_derived_fields(data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate comprehensive average values"""
        derived = {}
        
        # Temperature averages (DHT22 + BME280)
        temp_dht = data.get('temperatureC_dht22')
        temp_bme = data.get('temperatureC_bme280')
        if temp_dht is not None and temp_bme is not None:
            derived['temperatureC_avg'] = round((temp_dht + temp_bme) / 2, 2)
        elif temp_dht is not None:
            derived['temperatureC_avg'] = temp_dht
        elif temp_bme is not None:
            derived['temperatureC_avg'] = temp_bme
        
        # Humidity averages (DHT22 + BME280)
        hum_dht = data.get('humidityPercent_dht22')
        hum_bme = data.get('humidityPercent_bme280')
        if hum_dht is not None and hum_bme is not None:
            derived['humidityPercent_avg'] = round((hum_dht + hum_bme) / 2, 1)
        elif hum_dht is not None:
            derived['humidityPercent_avg'] = hum_dht
        elif hum_bme is not None:
            derived['humidityPercent_avg'] = hum_bme
        
        # Pressure averages (BMP180 + BME280)
        press_bmp = data.get('pressurePa_bmp180')
        press_bme = data.get('pressurePa_bme280')
        if press_bmp is not None and press_bme is not None:
            derived['pressurePa_avg'] = round((press_bmp + press_bme) / 2, 1)
        elif press_bmp is not None:
            derived['pressurePa_avg'] = press_bmp
        elif press_bme is not None:
            derived['pressurePa_avg'] = press_bme
        
        # Altitude averages (BMP180 + BME280 + GPS)
        alt_values = []
        for alt_field in ['altitudeM_bmp180', 'altitudeM_bme280', 'altitudeM_gps']:
            if data.get(alt_field) is not None:
                alt_values.append(data[alt_field])
        
        if alt_values:
            derived['altitudeM_avg'] = round(statistics.mean(alt_values), 2)
        
        # Acceleration averages (LSM303 + MPU6050)
        for axis in ['X', 'Y', 'Z']:
            lsm_val = data.get(f'accel{axis}_lsm303')
            mpu_val = data.get(f'accel{axis}_mpu6050')
            
            if lsm_val is not None and mpu_val is not None:
                derived[f'accel{axis}_avg'] = round((lsm_val + mpu_val) / 2, 3)
            elif lsm_val is not None:
                derived[f'accel{axis}_avg'] = lsm_val
            elif mpu_val is not None:
                derived[f'accel{axis}_avg'] = mpu_val
        
        return derived

class CubeSatTelemetrySystem:
    """Complete professional CubeSat telemetry system"""
    
    def __init__(self, use_postgres: bool = True):
        self.db_manager = DatabaseManager(use_postgres)
        self.sequence_number = 1
        self.data_queue = queue.Queue(maxsize=2000)
        self.running = False
        
        # ALL sensor simulators
        self.sensors = {
            'dht22': SensorSimulator('DHT22'),
            'bme280': SensorSimulator('BME280'),  # ƏLAVƏ EDILDI!
            'bmp180': SensorSimulator('BMP180'),
            'lsm303': SensorSimulator('LSM303'),
            'mpu6050': SensorSimulator('MPU6050'),
            'gps': SensorSimulator('GPS')
        }
        
        logger.info(f"Initialized with {len(self.sensors)} sensors: {list(self.sensors.keys())}")
    
    def start_sensor_threads(self):
        """Start ALL sensor reading threads"""
        self.running = True
        
        def sensor_thread(sensor_name: str, read_interval: float):
            """Individual sensor thread with enhanced error handling"""
            sensor = self.sensors[sensor_name]
            logger.info(f"Starting {sensor_name} sensor thread (interval: {read_interval}s)")
            
            while self.running:
                try:
                    # Get sensor data based on type
                    if sensor_name == 'dht22':
                        data = sensor.simulate_dht22()
                    elif sensor_name == 'bme280':
                        data = sensor.simulate_bme280()
                    elif sensor_name == 'bmp180':
                        data = sensor.simulate_bmp180()
                    elif sensor_name == 'lsm303':
                        data = sensor.simulate_lsm303()
                    elif sensor_name == 'mpu6050':
                        data = sensor.simulate_mpu6050()
                    elif sensor_name == 'gps':
                        data = sensor.simulate_gps()
                    else:
                        logger.error(f"Unknown sensor: {sensor_name}")
                        continue
                    
                    if data:  # Only queue if sensor provided data
                        self.data_queue.put((sensor_name, data), timeout=1)
                        logger.debug(f"{sensor_name} → {len(data)} fields queued")
                    else:
                        logger.debug(f"{sensor_name} sensor failed (simulated)")
                        
                except queue.Full:
                    logger.error(f"{sensor_name} queue full, dropping data")
                except Exception as e:
                    logger.error(f"{sensor_name} thread error: {e}")
                
                time.sleep(read_interval)
        
        # Start ALL sensor threads with realistic intervals
        sensor_configs = [
            ('dht22', 3.0),      # DHT22: slower, every 3 seconds
            ('bme280', 2.0),     # BME280: every 2 seconds
            ('bmp180', 2.5),     # BMP180: every 2.5 seconds
            ('lsm303', 0.1),     # LSM303: high frequency for motion
            ('mpu6050', 0.1),    # MPU6050: high frequency for motion
            ('gps', 1.0)         # GPS: every second
        ]
        
        for sensor_name, interval in sensor_configs:
            threading.Thread(
                target=sensor_thread, 
                args=(sensor_name, interval), 
                daemon=True,
                name=f"Sensor-{sensor_name}"
            ).start()
            logger.info(f"✓ {sensor_name} thread started")
    
    def start_data_processor(self):
        """Process queued sensor data and create telemetry packets"""
        def processor_thread():
            logger.info("Starting main data processor thread")
            current_packet = {}
            last_send_time = time.time()
            send_interval = 5.0  # Send comprehensive packet every 5 seconds
            
            while self.running:
                try:
                    # Collect sensor data
                    try:
                        sensor_name, data = self.data_queue.get(timeout=0.5)
                        current_packet.update(data)
                        logger.debug(f"Added {sensor_name} data: {list(data.keys())}")
                    except queue.Empty:
                        pass
                    
                    # Send packet when interval elapsed
                    if time.time() - last_send_time >= send_interval:
                        if current_packet:
                            self.send_telemetry_packet(current_packet)
                            logger.info(f"📦 Packet sent with {len(current_packet)} fields")
                        else:
                            logger.warning("No sensor data collected in this interval")
                        current_packet = {}
                        last_send_time = time.time()
                        
                except Exception as e:
                    logger.error(f"Data processor error: {e}")
                    logger.error(traceback.format_exc())
        
        threading.Thread(target=processor_thread, daemon=True, name="DataProcessor").start()
    
    def send_telemetry_packet(self, sensor_data: Dict[str, Any]):
        """Create and store comprehensive telemetry packet"""
        try:
            # Calculate ALL derived fields
            derived = TelemetryDataProcessor.calculate_derived_fields(sensor_data)
            sensor_data.update(derived)
            
            # Create telemetry data object
            now = datetime.now(timezone.utc)
            telemetry = TelemetryData(
                sequenceNumber=self.sequence_number,
                sentAt=now.isoformat(),
                receivedAt=now.isoformat(),
                **sensor_data
            )
            
            # Store in database
            if self.db_manager.insert_telemetry(telemetry):
                active_sensors = [k for k, v in sensor_data.items() if v is not None and 'avg' not in k]
                logger.info(f"📡 Telemetry #{self.sequence_number}: {len(active_sensors)} sensors, {len(derived)} averages")
                self.sequence_number += 1
            else:
                logger.error(f"❌ Failed to store telemetry packet #{self.sequence_number}")
                
        except Exception as e:
            logger.error(f"Failed to send telemetry packet: {e}")
            logger.error(traceback.format_exc())
    
    def get_latest_data(self) -> Dict[str, Any]:
        """Get latest known values for all fields"""
        return self.db_manager.get_latest_state()
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        latest_data = self.get_latest_data()
        
        # Count active sensors
        sensor_status = {}
        for sensor_name in self.sensors.keys():
            active_fields = [k for k in latest_data.keys() if sensor_name.replace('_', '').lower() in k.lower()]
            sensor_status[sensor_name] = {
                'active': len(active_fields) > 0,
                'fields_count': len(active_fields),
                'fields': active_fields
            }
        
        return {
            'total_fields': len(latest_data),
            'sequence_number': self.sequence_number,
            'sensors': sensor_status,
            'derived_fields': [k for k in latest_data.keys() if 'avg' in k]
        }
    
    def start(self):
        """Start the complete telemetry system"""
        logger.info("🚀 Starting CubeSat Telemetry System - FULL EDITION")
        logger.info("="*60)
        self.start_sensor_threads()
        self.start_data_processor()
        logger.info("✅ All subsystems operational")
    
    def stop(self):
        """Stop the telemetry system"""
        logger.info("🛑 Stopping CubeSat Telemetry System")
        self.running = False

class TelemetryHTTPHandler(BaseHTTPRequestHandler):
    """Professional HTTP API handler"""
    
    def do_POST(self):
        """Handle POST /ingest requests"""
        try:
            if self.path == '/ingest':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                payload = json.loads(post_data.decode('utf-8'))
                
                logger.info(f"📥 POST /ingest received: {len(payload)} fields")
                
                # Process external telemetry data
                now = datetime.now(timezone.utc)
                
                # Calculate derived fields
                derived = TelemetryDataProcessor.calculate_derived_fields(payload)
                payload.update(derived)
                
                # Create telemetry object
                telemetry = TelemetryData(
                    sequenceNumber=payload.get('sequenceNumber', telemetry_system.sequence_number),
                    sentAt=payload.get('sentAt', now.isoformat()),
                    receivedAt=now.isoformat(),
                    schemaVersion=payload.get('schemaVersion', '1.0'),
                    **{k: v for k, v in payload.items() if k not in ['sequenceNumber', 'sentAt', 'receivedAt', 'schemaVersion']}
                )
                
                # Store in database
                if telemetry_system.db_manager.insert_telemetry(telemetry):
                    self.send_json_response(200, {
                        'status': 'success',
                        'message': 'Telemetry data ingested successfully',
                        'sequenceNumber': telemetry.sequenceNumber,
                        'fieldsProcessed': len([k for k, v in payload.items() if v is not None])
                    })
                else:
                    self.send_json_response(500, {'status': 'error', 'message': 'Database insertion failed'})
            else:
                self.send_json_response(404, {'error': 'POST endpoint not found'})
                
        except Exception as e:
            logger.error(f"POST request error: {e}")
            self.send_json_response(400, {'error': str(e)})
    
    def do_GET(self):
        """Handle GET requests with comprehensive endpoints"""
        try:
            parsed_path = urllib.parse.urlparse(self.path)
            path = parsed_path.path
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            logger.info(f"HTTP GET: {path}")
            
            if path == '/latest':
                # Get latest telemetry data
                latest_data = telemetry_system.get_latest_data()
                self.send_json_response(200, {
                    'status': 'success',
                    'data': latest_data,
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'total_fields': len(latest_data),
                    'active_sensors': len([k for k in latest_data.keys() if not k.endswith('_avg')])
                })
            
            elif path == '/health':
                self.send_json_response(200, {
                    'status': 'healthy', 
                    'message': 'CubeSat telemetry system operational',
                    'database': 'PostgreSQL' if telemetry_system.db_manager.use_postgres else 'SQLite'
                })
            
            elif path == '/status':
                stats = telemetry_system.get_system_stats()
                self.send_json_response(200, {
                    'status': 'running',
                    'uptime_seconds': round(time.time() - start_time, 1),
                    'database_type': 'PostgreSQL' if telemetry_system.db_manager.use_postgres else 'SQLite',
                    **stats
                })
            
            elif path == '/sensors':
                # Detailed sensor information
                latest_data = telemetry_system.get_latest_data()
                sensor_details = {}
                
                for sensor_name in telemetry_system.sensors.keys():
                    fields = [k for k in latest_data.keys() if sensor_name.lower() in k.lower()]
                    sensor_details[sensor_name] = {
                        'active': len(fields) > 0,
                        'field_count': len(fields),
                        'fields': {field: latest_data.get(field) for field in fields}
                    }
                
                self.send_json_response(200, {
                    'sensors': sensor_details,
                    'total_sensors': len(telemetry_system.sensors),
                    'active_sensors': sum(1 for s in sensor_details.values() if s['active'])
                })
            
            elif path == '/' or path == '/index.html':
                # Enhanced web interface
                html_content = self.create_enhanced_web_interface()
                self.send_html_response(200, html_content)
            
            else:
                self.send_json_response(404, {
                    'error': 'Endpoint not found', 
                    'available_endpoints': ['/latest', '/health', '/status', '/sensors', '/ingest', '/']
                })
                
        except Exception as e:
            logger.error(f"GET request error: {e}")
            logger.error(traceback.format_exc())
            self.send_json_response(500, {'error': str(e)})
    
    def create_enhanced_web_interface(self) -> str:
        """Create professional web interface with all sensors"""
        latest_data = telemetry_system.get_latest_data()
        stats = telemetry_system.get_system_stats()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>🛰️ CubeSat Telemetry System</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    color: #333;
                }}
                .container {{ 
                    max-width: 1400px; 
                    margin: 0 auto; 
                    padding: 20px;
                }}
                .header {{ 
                    text-align: center; 
                    color: white; 
                    margin-bottom: 30px;
                    background: rgba(0,0,0,0.2);
                    padding: 20px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                }}
                .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
                .system-status {{ 
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin-bottom: 30px;
                }}
                .status-card {{ 
                    background: rgba(255,255,255,0.95);
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                }}
                .status-value {{ font-size: 1.8em; font-weight: bold; color: #4CAF50; }}
                .status-label {{ color: #666; margin-top: 5px; }}
                
                .sensors-grid {{ 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); 
                    gap: 20px; 
                    margin-bottom: 30px;
                }}
                .sensor-card {{ 
                    background: rgba(255,255,255,0.95); 
                    padding: 20px; 
                    border-radius: 15px; 
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                    border-left: 5px solid;
                }}
                .sensor-card.dht22 {{ border-left-color: #FF6B6B; }}
                .sensor-card.bme280 {{ border-left-color: #4ECDC4; }}
                .sensor-card.bmp180 {{ border-left-color: #45B7D1; }}
                .sensor-card.lsm303 {{ border-left-color: #96CEB4; }}
                .sensor-card.mpu6050 {{ border-left-color: #FFEAA7; }}
                .sensor-card.gps {{ border-left-color: #DDA0DD; }}
                .sensor-card.averages {{ border-left-color: #FF7675; }}
                
                .sensor-title {{ 
                    font-size: 1.3em; 
                    font-weight: bold; 
                    margin-bottom: 15px; 
                    display: flex;
                    align-items: center;
                }}
                .sensor-icon {{ 
                    width: 30px; 
                    height: 30px; 
                    border-radius: 50%; 
                    margin-right: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                }}
                .dht22 .sensor-icon {{ background: #FF6B6B; }}
                .bme280 .sensor-icon {{ background: #4ECDC4; }}
                .bmp180 .sensor-icon {{ background: #45B7D1; }}
                .lsm303 .sensor-icon {{ background: #96CEB4; }}
                .mpu6050 .sensor-icon {{ background: #FFEAA7; color: #333; }}
                .gps .sensor-icon {{ background: #DDA0DD; }}
                .averages .sensor-icon {{ background: #FF7675; }}
                
                .data-grid {{ 
                    display: grid; 
                    grid-template-columns: 1fr 1fr; 
                    gap: 10px; 
                }}
                .data-item {{ 
                    padding: 8px 12px; 
                    background: #f8f9fa; 
                    border-radius: 5px; 
                    font-family: 'Courier New', monospace;
                    display: flex;
                    justify-content: space-between;
                }}
                .data-label {{ font-weight: bold; }}
                .data-value {{ color: #2c3e50; }}
                .no-data {{ color: #e74c3c; font-style: italic; }}
                
                .controls {{ 
                    text-align: center; 
                    margin: 20px 0;
                }}
                .btn {{ 
                    background: linear-gradient(45deg, #667eea, #764ba2); 
                    color: white; 
                    padding: 12px 25px; 
                    border: none; 
                    border-radius: 25px; 
                    cursor: pointer; 
                    font-size: 1em;
                    margin: 0 10px;
                    transition: transform 0.2s;
                }}
                .btn:hover {{ transform: translateY(-2px); }}
                
                .api-info {{ 
                    background: rgba(255,255,255,0.95); 
                    padding: 20px; 
                    border-radius: 15px; 
                    margin-top: 20px;
                }}
                .api-endpoint {{ 
                    display: inline-block; 
                    background: #e9ecef; 
                    padding: 5px 10px; 
                    border-radius: 5px; 
                    margin: 5px; 
                    text-decoration: none; 
                    color: #495057;
                }}
                .api-endpoint:hover {{ background: #dee2e6; }}
                
                @media (max-width: 768px) {{
                    .sensors-grid {{ grid-template-columns: 1fr; }}
                    .data-grid {{ grid-template-columns: 1fr; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🛰️ CubeSat Telemetry System</h1>
                    <p>Professional Multi-Sensor Data Collection & Analysis</p>
                </div>
                
                <div class="system-status">
                    <div class="status-card">
                        <div class="status-value">{stats['sequence_number']}</div>
                        <div class="status-label">Telemetry Packets</div>
                    </div>
                    <div class="status-card">
                        <div class="status-value">{stats['total_fields']}</div>
                        <div class="status-label">Active Data Fields</div>
                    </div>
                    <div class="status-card">
                        <div class="status-value">{len(telemetry_system.sensors)}</div>
                        <div class="status-label">Total Sensors</div>
                    </div>
                    <div class="status-card">
                        <div class="status-value">{len(stats['derived_fields'])}</div>
                        <div class="status-label">Calculated Averages</div>
                    </div>
                </div>
                
                <div class="controls">
                    <button class="btn" onclick="location.reload()">🔄 Refresh Data</button>
                    <button class="btn" onclick="window.open('/latest', '_blank')">📊 View JSON</button>
                    <button class="btn" onclick="window.open('/status', '_blank')">⚙️ System Status</button>
                </div>
                
                <div class="sensors-grid">
                    <!-- DHT22 Environment Sensor -->
                    <div class="sensor-card dht22">
                        <div class="sensor-title">
                            <div class="sensor-icon">T</div>
                            DHT22 Environment Sensor
                        </div>
                        <div class="data-grid">
                            <div class="data-item">
                                <span class="data-label">Temperature:</span>
                                <span class="data-value">{latest_data.get('temperatureC_dht22', 'No data')} °C</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Humidity:</span>
                                <span class="data-value">{latest_data.get('humidityPercent_dht22', 'No data')} %</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- BME280 Environment Sensor -->
                    <div class="sensor-card bme280">
                        <div class="sensor-title">
                            <div class="sensor-icon">B</div>
                            BME280 Environment Sensor
                        </div>
                        <div class="data-grid">
                            <div class="data-item">
                                <span class="data-label">Temperature:</span>
                                <span class="data-value">{latest_data.get('temperatureC_bme280', 'No data')} °C</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Humidity:</span>
                                <span class="data-value">{latest_data.get('humidityPercent_bme280', 'No data')} %</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Pressure:</span>
                                <span class="data-value">{latest_data.get('pressurePa_bme280', 'No data')} Pa</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Altitude:</span>
                                <span class="data-value">{latest_data.get('altitudeM_bme280', 'No data')} m</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- BMP180 Pressure Sensor -->
                    <div class="sensor-card bmp180">
                        <div class="sensor-title">
                            <div class="sensor-icon">P</div>
                            BMP180 Pressure Sensor
                        </div>
                        <div class="data-grid">
                            <div class="data-item">
                                <span class="data-label">Pressure:</span>
                                <span class="data-value">{latest_data.get('pressurePa_bmp180', 'No data')} Pa</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Altitude:</span>
                                <span class="data-value">{latest_data.get('altitudeM_bmp180', 'No data')} m</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- LSM303 Motion Sensor -->
                    <div class="sensor-card lsm303">
                        <div class="sensor-title">
                            <div class="sensor-icon">L</div>
                            LSM303 Motion & Magnetic Sensor
                        </div>
                        <div class="data-grid">
                            <div class="data-item">
                                <span class="data-label">Accel X:</span>
                                <span class="data-value">{latest_data.get('accelX_lsm303', 'No data')} m/s²</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Accel Y:</span>
                                <span class="data-value">{latest_data.get('accelY_lsm303', 'No data')} m/s²</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Accel Z:</span>
                                <span class="data-value">{latest_data.get('accelZ_lsm303', 'No data')} m/s²</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Mag X:</span>
                                <span class="data-value">{latest_data.get('magX_lsm303', 'No data')} µT</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Mag Y:</span>
                                <span class="data-value">{latest_data.get('magY_lsm303', 'No data')} µT</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Mag Z:</span>
                                <span class="data-value">{latest_data.get('magZ_lsm303', 'No data')} µT</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- MPU6050 Motion Sensor -->
                    <div class="sensor-card mpu6050">
                        <div class="sensor-title">
                            <div class="sensor-icon">M</div>
                            MPU6050 Motion Sensor
                        </div>
                        <div class="data-grid">
                            <div class="data-item">
                                <span class="data-label">Accel X:</span>
                                <span class="data-value">{latest_data.get('accelX_mpu6050', 'No data')} m/s²</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Accel Y:</span>
                                <span class="data-value">{latest_data.get('accelY_mpu6050', 'No data')} m/s²</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Accel Z:</span>
                                <span class="data-value">{latest_data.get('accelZ_mpu6050', 'No data')} m/s²</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Gyro X:</span>
                                <span class="data-value">{latest_data.get('gyroX_mpu6050', 'No data')} °/s</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Gyro Y:</span>
                                <span class="data-value">{latest_data.get('gyroY_mpu6050', 'No data')} °/s</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Gyro Z:</span>
                                <span class="data-value">{latest_data.get('gyroZ_mpu6050', 'No data')} °/s</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- GPS Navigation -->
                    <div class="sensor-card gps">
                        <div class="sensor-title">
                            <div class="sensor-icon">📍</div>
                            GPS Navigation System
                        </div>
                        <div class="data-grid">
                            <div class="data-item">
                                <span class="data-label">Latitude:</span>
                                <span class="data-value">{latest_data.get('gpsLatitude', 'No data')}°</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Longitude:</span>
                                <span class="data-value">{latest_data.get('gpsLongitude', 'No data')}°</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Altitude:</span>
                                <span class="data-value">{latest_data.get('altitudeM_gps', 'No data')} m</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Speed:</span>
                                <span class="data-value">{latest_data.get('gpsSpeedKmh', 'No data')} km/h</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Satellites:</span>
                                <span class="data-value">{latest_data.get('gpsSatellites', 'No data')}</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">HDOP:</span>
                                <span class="data-value">{latest_data.get('gpsHdop', 'No data')}</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Calculated Averages -->
                    <div class="sensor-card averages">
                        <div class="sensor-title">
                            <div class="sensor-icon">📈</div>
                            Calculated Averages & Fusion
                        </div>
                        <div class="data-grid">
                            <div class="data-item">
                                <span class="data-label">Avg Temperature:</span>
                                <span class="data-value">{latest_data.get('temperatureC_avg', 'No data')} °C</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Avg Humidity:</span>
                                <span class="data-value">{latest_data.get('humidityPercent_avg', 'No data')} %</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Avg Pressure:</span>
                                <span class="data-value">{latest_data.get('pressurePa_avg', 'No data')} Pa</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Avg Altitude:</span>
                                <span class="data-value">{latest_data.get('altitudeM_avg', 'No data')} m</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Avg Accel X:</span>
                                <span class="data-value">{latest_data.get('accelX_avg', 'No data')} m/s²</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Avg Accel Y:</span>
                                <span class="data-value">{latest_data.get('accelY_avg', 'No data')} m/s²</span>
                            </div>
                            <div class="data-item">
                                <span class="data-label">Avg Accel Z:</span>
                                <span class="data-value">{latest_data.get('accelZ_avg', 'No data')} m/s²</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="api-info">
                    <h3>🔌 API Endpoints</h3>
                    <p>
                        <a href="/latest" class="api-endpoint">GET /latest</a>
                        <a href="/health" class="api-endpoint">GET /health</a>
                        <a href="/status" class="api-endpoint">GET /status</a>
                        <a href="/sensors" class="api-endpoint">GET /sensors</a>
                        <span class="api-endpoint">POST /ingest</span>
                    </p>
                    <p style="margin-top: 15px;">
                        <strong>Database:</strong> {'PostgreSQL' if telemetry_system.db_manager.use_postgres else 'SQLite (Fallback)'} | 
                        <strong>Uptime:</strong> {round(time.time() - start_time, 1)}s |
                        <strong>Auto-refresh:</strong> <span id="countdown">30</span>s
                    </p>
                </div>
            </div>
            
            <script>
                // Auto-refresh countdown
                let countdown = 30;
                const countdownElement = document.getElementById('countdown');
                
                setInterval(() => {{
                    countdown--;
                    countdownElement.textContent = countdown;
                    if (countdown <= 0) {{
                        location.reload();
                    }}
                }}, 1000);
                
                // Add some visual feedback
                document.querySelectorAll('.data-value').forEach(el => {{
                    if (el.textContent === 'No data') {{
                        el.classList.add('no-data');
                    }}
                }});
            </script>
        </body>
        </html>
        """
        return html
    
    def send_json_response(self, status_code: int, data: Dict[str, Any]):
        """Send JSON response with proper headers"""
        response = json.dumps(data, indent=2, ensure_ascii=False)
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Content-length', str(len(response.encode('utf-8'))))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
    
    def send_html_response(self, status_code: int, html_content: str):
        """Send HTML response"""
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-length', str(len(html_content.encode('utf-8'))))
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Override to use our logger"""
        logger.info(f"HTTP {format % args}")

# Add missing import for math
import math

def start_http_server(port: int = 8080):
    """Start HTTP API server with comprehensive error handling"""
    ports_to_try = [8080, 8081, 8082, 8000, 9000, 3000, 5000]
    
    for attempt_port in ports_to_try:
        try:
            server = HTTPServer(('0.0.0.0', attempt_port), TelemetryHTTPHandler)
            logger.info("="*60)
            logger.info(f"🌐 HTTP Server started successfully!")
            logger.info(f"📡 Access via: http://localhost:{attempt_port}")
            logger.info(f"🔗 Or try: http://127.0.0.1:{attempt_port}")
            logger.info("="*60)
            logger.info("📋 Available endpoints:")
            logger.info(f"   🏠 http://localhost:{attempt_port}/         → Web Dashboard")
            logger.info(f"   📊 http://localhost:{attempt_port}/latest   → Latest telemetry (JSON)")
            logger.info(f"   ❤️  http://localhost:{attempt_port}/health   → Health check")
            logger.info(f"   ⚙️  http://localhost:{attempt_port}/status   → System status")
            logger.info(f"   🔧 http://localhost:{attempt_port}/sensors  → Sensor details")
            logger.info(f"   📤 POST http://localhost:{attempt_port}/ingest → Data ingestion")
            logger.info("="*60)
            
            def server_thread():
                try:
                    server.serve_forever()
                except Exception as e:
                    logger.error(f"Server thread error: {e}")
            
            threading.Thread(target=server_thread, daemon=True, name="HTTPServer").start()
            return server
            
        except OSError as e:
            if "Address already in use" in str(e) or "Only one usage" in str(e):
                logger.warning(f"Port {attempt_port} busy, trying next...")
                continue
            else:
                logger.error(f"Failed to start server on port {attempt_port}: {e}")
    
    logger.error("❌ Failed to start HTTP server on any available port!")
    return None

def print_startup_banner():
    """Print professional startup banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        🛰️  CUBESAT TELEMETRY SYSTEM - FULL EDITION  🛰️      ║
    ║                                                              ║
    ║  🎯 ALL SENSORS OPERATIONAL                                 ║
    ║  📊 REAL-TIME DATA COLLECTION                               ║
    ║  🔄 SENSOR FUSION & AVERAGES                                ║
    ║  🗄️  POSTGRESQL + SQLITE SUPPORT                            ║
    ║  🌐 PROFESSIONAL WEB API                                    ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Main entry point - Professional CubeSat Telemetry System"""
    global telemetry_system, start_time
    start_time = time.time()
    
    print_startup_banner()
    
    try:
        # Initialize telemetry system with PostgreSQL preference
        telemetry_system = CubeSatTelemetrySystem(use_postgres=True)
        
        # Start HTTP server
        http_server = start_http_server(8080)
        if not http_server:
            logger.error("Cannot start without HTTP server")
            return
        
        # Start telemetry system
        telemetry_system.start()
        
        # Print system status
        logger.info("🚀 SYSTEM INITIALIZATION COMPLETE")
        logger.info("="*60)
        logger.info("📋 SYSTEM CONFIGURATION:")
        logger.info(f"   🗄️  Database: {'PostgreSQL' if telemetry_system.db_manager.use_postgres else 'SQLite'}")
        logger.info(f"   🔧 Sensors: {len(telemetry_system.sensors)} active")
        for sensor_name in telemetry_system.sensors.keys():
            logger.info(f"      ✓ {sensor_name.upper()}")
        logger.info(f"   📡 Data Collection: Every 5 seconds")
        logger.info(f"   🌐 Web Interface: http://localhost:8080")
        logger.info("="*60)
        logger.info("🟢 SYSTEM OPERATIONAL - Press Ctrl+C to stop")
        logger.info("="*60)
        
        # Main monitoring loop
        monitoring_interval = 30
        try:
            while True:
                time.sleep(monitoring_interval)
                latest = telemetry_system.get_latest_data()
                stats = telemetry_system.get_system_stats()
                
                # Status update
                active_sensors = sum(1 for s in stats['sensors'].values() if s['active'])
                logger.info(f"📊 Status: {active_sensors}/{len(telemetry_system.sensors)} sensors, "
                           f"{len(latest)} fields, Seq #{telemetry_system.sequence_number}")
                
                # Sensor health check
                for sensor_name, sensor_info in stats['sensors'].items():
                    status = "🟢" if sensor_info['active'] else "🔴"
                    logger.debug(f"   {status} {sensor_name}: {sensor_info['fields_count']} fields")
        
        except KeyboardInterrupt:
            logger.info("\n🛑 Shutdown requested by user")
        
    except Exception as e:
        logger.error(f"💥 System failure: {e}")
        logger.error(traceback.format_exc())
    
    finally:
        if 'telemetry_system' in locals():
            telemetry_system.stop()
        logger.info("🏁 Shutdown complete - All systems stopped")
        logger.info("="*60)

if __name__ == "__main__":
    main()