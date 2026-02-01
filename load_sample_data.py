"""
Sample Data Generator for Demo
Creates diverse sample grievances to showcase the system
"""

import requests
import time

API_BASE_URL = "http://127.0.0.1:8000"

sample_grievances = [
    {
        "title": "Water shortage in Ward 5",
        "description": "There has been no water supply for the past 3 days in our area. Many families are struggling. This is an urgent issue that needs immediate attention.",
        "location": "Ward 5, Sector 12"
    },
    {
        "title": "Pothole on Main Road near School",
        "description": "Large pothole on Main Road causing accidents. Located right near the school entrance. Very dangerous for children and vehicles.",
        "location": "Main Road, Near Government School"
    },
    {
        "title": "Frequent power cuts in residential area",
        "description": "Power cuts happening 4-5 times daily for past week. Each outage lasts 2-3 hours. Affecting work from home and children's studies.",
        "location": "Residential Area, Block C"
    },
    {
        "title": "Garbage not collected for 5 days",
        "description": "Municipal garbage collection has not happened for 5 days. Waste is piling up and creating health hazards. Bad smell and flies everywhere.",
        "location": "Street 7, Sector 15"
    },
    {
        "title": "Need medicines at government hospital",
        "description": "Essential medicines not available at government hospital. Diabetic medicines and blood pressure tablets out of stock for 2 weeks.",
        "location": "District Hospital"
    },
    {
        "title": "School building needs urgent repair",
        "description": "School building roof is leaking badly. During rain, water enters classrooms. Walls also have cracks. Safety concern for students.",
        "location": "Government Primary School, Village"
    },
    {
        "title": "Street lights not working",
        "description": "All street lights in our colony have been non-functional for 2 months. Very unsafe at night, especially for women and elderly.",
        "location": "Colony Road, Sector 8"
    },
    {
        "title": "Drainage system blocked",
        "description": "Drainage is completely blocked causing water logging. Mosquito breeding happening. Health risk for entire neighborhood.",
        "location": "Market Area, Main Street"
    },
    {
        "title": "Bus service frequency very low",
        "description": "Only 2 buses per day to city. People missing work and appointments. Need more frequent bus service on this route.",
        "location": "Village to City Route"
    },
    {
        "title": "Ration shop closed frequently",
        "description": "Government ration shop remains closed most days. When open, long queues and insufficient stock. Poor people suffering.",
        "location": "Fair Price Shop, Ward 3"
    }
]

def submit_sample_data():
    """Submit all sample grievances to the backend"""
    print("🚀 Starting sample data generation...")
    print(f"📊 Will create {len(sample_grievances)} sample grievances\n")
    
    success_count = 0
    failed_count = 0
    
    for i, grievance in enumerate(sample_grievances, 1):
        try:
            print(f"[{i}/{len(sample_grievances)}] Submitting: {grievance['title'][:50]}...")
            
            response = requests.post(
                f"{API_BASE_URL}/grievances/",
                json=grievance,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"    ✅ Success! Category: {result.get('category', 'N/A')}, Priority: {result.get('priority', 'N/A')}")
                success_count += 1
            else:
                print(f"    ❌ Failed with status {response.status_code}")
                failed_count += 1
            
            # Small delay to avoid overwhelming the server
            time.sleep(0.5)
            
        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
            failed_count += 1
    
    print(f"\n{'='*60}")
    print(f"📊 Summary:")
    print(f"   ✅ Successfully created: {success_count} grievances")
    print(f"   ❌ Failed: {failed_count} grievances")
    print(f"   📈 Total: {len(sample_grievances)} grievances")
    print(f"{'='*60}\n")
    
    if success_count > 0:
        print("🎉 Sample data loaded successfully!")
        print("📊 Visit http://localhost:8501 to see the dashboard")
        print("📈 Check Analytics Dashboard for visualizations")
    else:
        print("⚠️  No data was loaded. Please check if the backend is running.")
        print("💡 Start backend with: uvicorn app.main_demo:app --reload")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎯 SAMPLE DATA GENERATOR FOR DEMO")
    print("="*60 + "\n")
    
    # Check if backend is running
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        print("✅ Backend is running!\n")
        submit_sample_data()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend!")
        print("💡 Please start the backend first:")
        print("   cd backend")
        print("   uvicorn app.main_demo:app --reload")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
