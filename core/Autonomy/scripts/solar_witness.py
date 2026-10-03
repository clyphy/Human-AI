#!/usr/bin/env python3
import os
import sys
import math
import sqlite3
from datetime import datetime

BASE_DIR = os.path.expanduser("~/projects/Human-AI/core/Autonomy")
DB_PATH = os.path.join(BASE_DIR, "databases/memory_drum.db")

def init_tables():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS witness_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            rhythm_type TEXT NOT NULL,
            solar_elevation REAL,
            solar_azimuth REAL,
            observation TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def calculate_solar_position(lat=48.8, lon=-100.0):
    now = datetime.now()
    day_of_year = now.timetuple().tm_yday
    hour = now.hour + now.minute / 60.0 + now.second / 3600.0
    
    declination = 23.45 * math.sin(math.radians((360 / 365) * (day_of_year - 81)))
    lstm = 15 * -6  
    bg_time = 4 * (lon - lstm)
    eq_time = 9.87 * math.sin(math.radians(2 * (360 / 364) * (day_of_year - 81))) - 7.53 * math.cos(math.radians((360 / 364) * (day_of_year - 81)))
    time_correction = bg_time + eq_time
    local_solar_time = hour + (time_correction / 60.0)
    hour_angle = 15 * (local_solar_time - 12)
    
    lat_rad = math.radians(lat)
    dec_rad = math.radians(declination)
    ha_rad = math.radians(hour_angle)
    
    sin_el = (math.sin(lat_rad) * math.sin(dec_rad)) + (math.cos(lat_rad) * math.cos(dec_rad) * math.cos(ha_rad))
    elevation = math.degrees(math.asin(sin_el))
    
    cos_az = (math.sin(dec_rad) - math.sin(lat_rad) * sin_el) / (math.cos(lat_rad) * math.cos(math.asin(sin_el)))
    cos_az = max(-1.0, min(1.0, cos_az))
    azimuth = math.degrees(math.acos(cos_az))
    if hour_angle > 0:
        azimuth = 360 - azimuth
        
    return round(elevation, 2), round(azimuth, 2)

def record_witness_mark(rhythm_type, observation):
    init_tables()
    elevation, azimuth = calculate_solar_position()
    timestamp = datetime.now().isoformat()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO witness_events (timestamp, rhythm_type, solar_elevation, solar_azimuth, observation)
        VALUES (?, ?, ?, ?, ?);
    """, (timestamp, rhythm_type, elevation, azimuth, observation))
    
    conn.commit()
    conn.close()
    print(f"Witness status logged at {timestamp}.")
    print(f"Solar tracking alignment: Elevation {elevation}°, Azimuth {azimuth}°.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        record_witness_mark(sys.argv[1], sys.argv[2])
    else:
        record_witness_mark("solar_alignment", "Baseline check of cyclical tracking coordinates.")
