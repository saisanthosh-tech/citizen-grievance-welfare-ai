import sqlite3

conn = sqlite3.connect('grievances.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", tables)

if tables:
    cursor.execute("PRAGMA table_info(grievances)")
    columns = cursor.fetchall()
    print("\nColumns in grievances table:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")

conn.close()
