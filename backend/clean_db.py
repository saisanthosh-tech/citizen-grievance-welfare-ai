import sqlite3

conn = sqlite3.connect('grievance.db')
c = conn.cursor()

# Delete grievances with NULL coordinates
c.execute('DELETE FROM grievances WHERE latitude IS NULL OR latitude = 0')
conn.commit()
deleted = c.rowcount
print(f'✅ Deleted {deleted} grievances with NULL/zero coordinates')

# Show remaining
c.execute('SELECT id, latitude, longitude FROM grievances')
rows = c.fetchall()
print(f'\n📍 Remaining {len(rows)} grievances:')
for row in rows:
    print(f'  ID {row[0]}: Lat {row[1]:.4f}, Lon {row[2]:.4f}')

conn.close()
print('\n✅ Database cleaned!')
