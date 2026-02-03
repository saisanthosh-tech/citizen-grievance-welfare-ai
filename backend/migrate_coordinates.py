"""
Database Migration: Add Latitude and Longitude columns
Safely adds GPS coordinates to existing grievances table
"""

import sqlite3
import json
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from location_utils import parse_location_to_coordinates

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), "grievance.db")

def migrate_add_coordinates():
    """Add latitude and longitude columns to grievances table"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(grievances)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'latitude' in columns and 'longitude' in columns:
            print("✅ Columns already exist. Skipping migration.")
            conn.close()
            return
        
        print("📍 Adding latitude and longitude columns...")
        
        # Add latitude column
        if 'latitude' not in columns:
            cursor.execute("ALTER TABLE grievances ADD COLUMN latitude REAL")
            print("  ✓ Added latitude column")
        
        # Add longitude column
        if 'longitude' not in columns:
            cursor.execute("ALTER TABLE grievances ADD COLUMN longitude REAL")
            print("  ✓ Added longitude column")
        
        conn.commit()
        
        # Update existing grievances with coordinates
        print("\n📌 Generating coordinates for existing grievances...")
        cursor.execute("SELECT id, location FROM grievances WHERE latitude IS NULL OR longitude IS NULL")
        grievances = cursor.fetchall()
        
        updated_count = 0
        for gid, location in grievances:
            lat, lon, city = parse_location_to_coordinates(location)
            cursor.execute(
                "UPDATE grievances SET latitude = ?, longitude = ? WHERE id = ?",
                (lat, lon, gid)
            )
            updated_count += 1
            print(f"  ✓ Updated grievance #{gid} with coordinates ({lat:.4f}, {lon:.4f}) - {city}")
        
        conn.commit()
        conn.close()
        
        print(f"\n✅ Migration complete! Updated {updated_count} grievances with coordinates.")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        if conn:
            conn.rollback()
            conn.close()
        raise

if __name__ == "__main__":
    print("🗺️ Starting database migration for GPS coordinates...\n")
    migrate_add_coordinates()
    print("\n🎉 Migration successful!")
