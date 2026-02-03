"""Test if API returns coordinates correctly"""
import requests

try:
    response = requests.get('http://localhost:8000/grievances/')
    if response.status_code == 200:
        data = response.json()
        grievances = data.get('grievances', [])
        
        print("="*60)
        print("API COORDINATE TEST")
        print("="*60)
        print(f"\nTotal grievances: {len(grievances)}")
        
        if grievances:
            print("\nFirst 3 grievances from API:")
            for g in grievances[:3]:
                print(f"\nID: {g.get('id')}")
                print(f"  Title: {g.get('title', 'N/A')[:40]}")
                print(f"  Latitude: {g.get('latitude')}")
                print(f"  Longitude: {g.get('longitude')}")
                
                if g.get('latitude') and g.get('longitude'):
                    print(f"  ✅ HAS COORDINATES")
                else:
                    print(f"  ❌ MISSING COORDINATES")
        
        # Check how many have coordinates
        with_coords = [g for g in grievances if g.get('latitude') and g.get('longitude')]
        print(f"\n{'='*60}")
        print(f"Grievances with coordinates: {len(with_coords)}/{len(grievances)}")
        print(f"{'='*60}")
        
    else:
        print(f"API Error: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
