"""
Location Utilities
Generate mock coordinates for grievances in Indian cities
"""

import random

# Major Indian cities with coordinates
INDIAN_CITIES = {
    'Delhi': (28.7041, 77.1025),
    'Mumbai': (19.0760, 72.8777),
    'Bangalore': (12.9716, 77.5946),
    'Chennai': (13.0827, 80.2707),
    'Kolkata': (22.5726, 88.3639),
    'Hyderabad': (17.3850, 78.4867),
    'Pune': (18.5204, 73.8567),
    'Ahmedabad': (23.0225, 72.5714),
    'Jaipur': (26.9124, 75.7873),
    'Lucknow': (26.8467, 80.9462),
    'Kanpur': (26.4499, 80.3319),
    'Nagpur': (21.1458, 79.0882),
    'Indore': (22.7196, 75.8577),
    'Thane': (19.2183, 72.9781),
    'Bhopal': (23.2599, 77.4126),
    'Visakhapatnam': (17.6868, 83.2185),
    'Pimpri-Chinchwad': (18.6298, 73.7997),
    'Patna': (25.5941, 85.1376),
    'Vadodara': (22.3072, 73.1812),
    'Ghaziabad': (28.6692, 77.4538),
    'Ludhiana': (30.9010, 75.8573),
    'Agra': (27.1767, 78.0081),
    'Nashik': (19.9975, 73.7898),
    'Faridabad': (28.4089, 77.3178),
    'Meerut': (28.9845, 77.7064),
    'Rajkot': (22.3039, 70.8022),
    'Varanasi': (25.3176, 82.9739),
    'Srinagar': (34.0837, 74.7973),
    'Amritsar': (31.6340, 74.8723),
    'Allahabad': (25.4358, 81.8463),
}

def get_random_city():
    """Get a random Indian city"""
    return random.choice(list(INDIAN_CITIES.keys()))

def get_city_coordinates(city_name):
    """Get coordinates for a city"""
    return INDIAN_CITIES.get(city_name, INDIAN_CITIES['Delhi'])

def generate_random_coordinates(city_name=None):
    """
    Generate random coordinates in India
    If city_name provided, generate near that city
    Otherwise, pick a random city
    """
    if city_name is None or city_name not in INDIAN_CITIES:
        city_name = get_random_city()
    
    base_lat, base_lon = INDIAN_CITIES[city_name]
    
    # REDUCED offset to keep markers on land (±0.02 degrees ≈ ±2km)
    # This prevents markers from going into the ocean
    lat = base_lat + random.uniform(-0.02, 0.02)
    lon = base_lon + random.uniform(-0.02, 0.02)
    
    return (lat, lon, city_name)

def parse_location_to_coordinates(location_text, grievance_id=None):
    """
    Parse location text to coordinates
    For demo, uses mock coordinates based on city keywords
    Uses grievance_id for consistent city selection if no location provided
    """
    if not location_text:
        # Use grievance_id to consistently pick a city
        if grievance_id is not None:
            cities = list(INDIAN_CITIES.keys())
            city_index = grievance_id % len(cities)
            city_name = cities[city_index]
        else:
            city_name = get_random_city()
        return generate_random_coordinates(city_name)
    
    location_lower = location_text.lower()
    
    # Check if any city name is in the location text
    for city in INDIAN_CITIES.keys():
        if city.lower() in location_lower:
            return generate_random_coordinates(city)
    
    # Default to Delhi if no match (capital city)
    return generate_random_coordinates('Delhi')

def get_india_center():
    """Get center coordinates for India"""
    return (20.5937, 78.9629)  # Geographic center of India
