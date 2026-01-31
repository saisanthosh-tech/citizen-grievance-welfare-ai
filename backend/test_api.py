#!/usr/bin/env python3
"""
Test script for Citizen Grievance & Welfare Intelligence System API

This script demonstrates all API endpoints and validates responses.
Run after starting the backend: python backend/test_api.py
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def print_response(response, label=""):
    """Pretty print response"""
    if label:
        print(f"[{label}]")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print(f"Status: {response.status_code}\n")

def test_root():
    """Test root endpoint"""
    print_header("1. TESTING ROOT ENDPOINT")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "GET /")
    return response.status_code == 200

def test_create_grievance():
    """Test grievance submission"""
    print_header("2. TESTING GRIEVANCE SUBMISSION")
    
    grievances = [
        {
            "title": "Water shortage in Sector 5",
            "description": "There has been no water supply for 3 days in our area. This is urgent and affecting the entire neighborhood.",
            "location": "Ward No. 5, Sector 5"
        },
        {
            "title": "Pothole causing accidents",
            "description": "A large pothole on Main Street near the market is causing accidents and damage to vehicles.",
            "location": "Main Street, Market Area"
        },
        {
            "title": "School needs repair",
            "description": "The roof of the school building has damaged areas. Books and teaching materials are at risk.",
            "location": "Government School, Near Hospital"
        }
    ]
    
    results = []
    for i, grievance in enumerate(grievances, 1):
        print(f"\n--- Grievance #{i} ---")
        response = requests.post(f"{BASE_URL}/grievances/", json=grievance)
        print_response(response, f"POST /grievances/")
        results.append(response.status_code == 200)
    
    return all(results)

def test_get_grievances():
    """Test retrieving grievances"""
    print_header("3. TESTING GET GRIEVANCES")
    
    tests = [
        ("Get all grievances", f"{BASE_URL}/grievances/"),
        ("Get first 2 grievances", f"{BASE_URL}/grievances/?limit=2"),
        ("Get high priority only", f"{BASE_URL}/grievances/?priority=High"),
        ("Get water supply grievances", f"{BASE_URL}/grievances/?category=Water%20Supply"),
    ]
    
    results = []
    for label, url in tests:
        print(f"\n--- {label} ---")
        response = requests.get(url)
        print_response(response, f"GET {url.replace(BASE_URL, '')}")
        results.append(response.status_code == 200)
    
    return all(results)

def test_statistics():
    """Test statistics endpoint"""
    print_header("4. TESTING STATISTICS")
    response = requests.get(f"{BASE_URL}/stats/")
    print_response(response, "GET /stats/")
    return response.status_code == 200

def test_validation():
    """Test input validation"""
    print_header("5. TESTING INPUT VALIDATION")
    
    invalid_grievances = [
        {
            "title": "Short",
            "description": "Too short",
            "error": "Title too short (< 5 chars)"
        },
        {
            "title": "Valid Title",
            "description": "Too short",
            "error": "Description too short (< 20 chars)"
        },
    ]
    
    results = []
    for i, test_case in enumerate(invalid_grievances, 1):
        print(f"\n--- Invalid Case #{i}: {test_case['error']} ---")
        grievance = {
            "title": test_case.get("title", "Test Title"),
            "description": test_case.get("description", "Test description goes here"),
        }
        response = requests.post(f"{BASE_URL}/grievances/", json=grievance)
        print_response(response, "POST /grievances/ (expecting error)")
        results.append(response.status_code == 400)
    
    return all(results)

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print(" CITIZEN GRIEVANCE & WELFARE INTELLIGENCE SYSTEM - API TEST SUITE")
    print("="*70)
    print(f"\nBase URL: {BASE_URL}")
    print(f"Test Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        # Test connectivity
        requests.get(BASE_URL)
    except:
        print("❌ ERROR: Cannot connect to backend at", BASE_URL)
        print("   Make sure the backend is running:")
        print("   cd backend && python -m uvicorn app.main:app --reload --port 8000")
        return
    
    # Run tests
    test_results = {
        "Root Endpoint": test_root(),
        "Create Grievance": test_create_grievance(),
        "Get Grievances": test_get_grievances(),
        "Statistics": test_statistics(),
        "Validation": test_validation(),
    }
    
    # Summary
    print_header("TEST SUMMARY")
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<50} {status}")
    
    total_passed = sum(1 for r in test_results.values() if r)
    print(f"\nTotal: {total_passed}/{len(test_results)} tests passed")
    
    if total_passed == len(test_results):
        print("\n✅ All tests passed! Backend is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
