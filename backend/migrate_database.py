"""
Database migration script to add status_history column to existing database
Run this once to update your existing database
"""

import sqlite3
import json
from datetime import datetime

def migrate_database():
    """Add status_history column to existing grievances table"""
    
    db_path = "grievance.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(grievances)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'status_history' in columns:
            print("✅ status_history column already exists!")
            return
        
        print("Adding status_history column...")
        
        # Add the new column
        cursor.execute("""
            ALTER TABLE grievances 
            ADD COLUMN status_history TEXT DEFAULT '[]'
        """)
        
        # Update existing grievances with initial history based on created_at
        cursor.execute("SELECT id, status, created_at FROM grievances")
        grievances = cursor.fetchall()
        
        for gid, status, created_at in grievances:
            initial_history = [{
                "status": status or "Pending",
                "timestamp": created_at or datetime.utcnow().isoformat(),
                "changed_by": "system",
                "action": "Grievance submitted (migrated)"
            }]
            
            cursor.execute(
                "UPDATE grievances SET status_history = ? WHERE id = ?",
                (json.dumps(initial_history), gid)
            )
        
        conn.commit()
        print(f"✅ Migration complete! Updated {len(grievances)} grievances.")
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("✅ Column already exists!")
        else:
            print(f"❌ Error: {e}")
            raise
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
