"""
Test script for Admin Status Update API

This script tests the new admin endpoint for updating grievance status.
Run this after starting the backend server.

Usage:
    python test_admin_api.py
"""

import requests
import json

API_BASE_URL = "http://127.0.0.1:8000"

def test_update_status():
    """Test updating grievance status"""
    print("=" * 60)
    print("Testing Admin Status Update API")
    print("=" * 60)
    
    # First, get all grievances to find an ID to test with
    print("\n1. Fetching existing grievances...")
    try:
        response = requests.get(f"{API_BASE_URL}/grievances/")
        response.raise_for_status()
        data = response.json()
        
        grievances = data.get("grievances", [])
        if not grievances:
            print("❌ No grievances found. Please submit a grievance first.")
            return
        
        # Use the first grievance for testing
        test_grievance = grievances[0]
        grievance_id = test_grievance["id"]
        current_status = test_grievance["status"]
        
        print(f"✓ Found grievance ID: {grievance_id}")
        print(f"  Current status: {current_status}")
        print(f"  Title: {test_grievance['title']}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Please ensure it's running on http://127.0.0.1:8000")
        return
    except Exception as e:
        print(f"❌ Error fetching grievances: {e}")
        return
    
    # Test 1: Update to "In Progress"
    print("\n2. Testing status update to 'In Progress'...")
    try:
        payload = {"status": "In Progress"}
        response = requests.patch(
            f"{API_BASE_URL}/grievances/{grievance_id}/status",
            json=payload
        )
        response.raise_for_status()
        updated = response.json()
        
        print(f"✓ Status updated successfully!")
        print(f"  New status: {updated['status']}")
        
    except Exception as e:
        print(f"❌ Error updating status: {e}")
        return
    
    # Test 2: Update to "Resolved"
    print("\n3. Testing status update to 'Resolved'...")
    try:
        payload = {"status": "Resolved"}
        response = requests.patch(
            f"{API_BASE_URL}/grievances/{grievance_id}/status",
            json=payload
        )
        response.raise_for_status()
        updated = response.json()
        
        print(f"✓ Status updated successfully!")
        print(f"  New status: {updated['status']}")
        
    except Exception as e:
        print(f"❌ Error updating status: {e}")
        return
    
    # Test 3: Try invalid status (should fail)
    print("\n4. Testing invalid status (should fail)...")
    try:
        payload = {"status": "Invalid Status"}
        response = requests.patch(
            f"{API_BASE_URL}/grievances/{grievance_id}/status",
            json=payload
        )
        
        if response.status_code == 400:
            print(f"✓ Validation working! Rejected invalid status.")
            print(f"  Error message: {response.json()['detail']}")
        else:
            print(f"⚠️ Expected 400 error, got {response.status_code}")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    # Test 4: Try non-existent grievance ID (should fail)
    print("\n5. Testing non-existent grievance ID (should fail)...")
    try:
        payload = {"status": "Pending"}
        response = requests.patch(
            f"{API_BASE_URL}/grievances/99999/status",
            json=payload
        )
        
        if response.status_code == 404:
            print(f"✓ Error handling working! Rejected non-existent ID.")
            print(f"  Error message: {response.json()['detail']}")
        else:
            print(f"⚠️ Expected 404 error, got {response.status_code}")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    # Reset to original status
    print(f"\n6. Resetting to original status '{current_status}'...")
    try:
        payload = {"status": current_status}
        response = requests.patch(
            f"{API_BASE_URL}/grievances/{grievance_id}/status",
            json=payload
        )
        response.raise_for_status()
        print(f"✓ Reset complete!")
        
    except Exception as e:
        print(f"❌ Error resetting status: {e}")
    
    print("\n" + "=" * 60)
    print("✓ All tests completed!")
    print("=" * 60)
    print("\nAllowed status values:")
    print("  - Pending")
    print("  - In Progress")
    print("  - Resolved")
    print("\nAPI Endpoint:")
    print(f"  PATCH {API_BASE_URL}/grievances/{{grievance_id}}/status")
    print("\nRequest body:")
    print('  {"status": "In Progress"}')
    print("=" * 60)

if __name__ == "__main__":
    test_update_status()
