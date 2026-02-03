"""
Comprehensive Diagnostic Script
Tests both login and map API issues
"""
import requests
import hashlib

print("="*60)
print("DIAGNOSTIC REPORT")
print("="*60)

# Test 1: Admin Login Credentials
print("\n1. ADMIN LOGIN TEST")
print("-"*60)
username = "admin"
password = "admin123"
password_hash = hashlib.sha256(password.encode()).hexdigest()
expected_hash = "240be518fabd2724720a9c08c8fa822809f74c7"

print(f"Username: {username}")
print(f"Password: {password}")
print(f"Hash Match: {password_hash == expected_hash}")

if password_hash == expected_hash:
    print("✅ Credentials are CORRECT")
else:
    print("❌ Hash mismatch!")
    print(f"Got: {password_hash}")
    print(f"Expected: {expected_hash}")

# Test 2: Backend API Connectivity
print("\n2. BACKEND API TEST")
print("-"*60)
try:
    resp = requests.get('http://localhost:8000/grievances/', timeout=5)
    print(f"Status Code: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        grievances = data.get('grievances', [])
        print(f"✅ API is working!")
        print(f"Total Grievances: {len(grievances)}")
        
        if grievances:
            first = grievances[0]
            print(f"\nFirst Grievance:")
            print(f"  ID: {first.get('id')}")
            print(f"  Title: {first.get('title', 'N/A')[:30]}...")
            print(f"  Latitude: {first.get('latitude', 'MISSING')}")
            print(f"  Longitude: {first.get('longitude', 'MISSING')}")
            
            if first.get('latitude') and first.get('longitude'):
                print("  ✅ Coordinates present")
            else:
                print("  ❌ Coordinates MISSING in API response")
        else:
            print("⚠️  No grievances in database")
    else:
        print(f"❌ API returned error: {resp.status_code}")
except Exception as e:
    print(f"❌ Cannot connect to backend: {e}")

# Test 3: Database Check
print("\n3. DATABASE TEST")
print("-"*60)
try:
    import sqlite3
    conn = sqlite3.connect('backend/grievance.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM grievances')
    total = cursor.fetchone()[0]
    print(f"Total grievances in DB: {total}")
    
    cursor.execute('SELECT COUNT(*) FROM grievances WHERE latitude IS NOT NULL AND longitude IS NOT NULL')
    with_coords = cursor.fetchone()[0]
    print(f"Grievances with coordinates: {with_coords}")
    
    if with_coords > 0:
        cursor.execute('SELECT id, latitude, longitude FROM grievances WHERE latitude IS NOT NULL LIMIT 1')
        row = cursor.fetchone()
        print(f"\nSample: ID {row[0]}: {row[1]:.4f}, {row[2]:.4f}")
        print("✅ Database has coordinates")
    else:
        print("❌ No coordinates in database")
    
    conn.close()
except Exception as e:
    print(f"❌ Database error: {e}")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print("\nIf login fails:")
print("  - Make sure you're on http://localhost:8502")
print("  - Click 'Admin Login' in sidebar")
print("  - Type exactly: admin / admin123")
print("\nIf map is empty:")
print("  - Check if API returns coordinates above")
print("  - Check if database has coordinates above")
print("  - Refresh browser and clear cache")
print("="*60)
