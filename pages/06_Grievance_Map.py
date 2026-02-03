"""
Grievance Map Page
Interactive map showing all grievances with geographic visualization
"""

import streamlit as st
import requests
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.map_view import render_grievance_map
from language_selector import language_selector, t, init_language
from location_utils import parse_location_to_coordinates

# Initialize language
init_language()

st.set_page_config(page_title="Grievance Map", page_icon="🗺️", layout="wide")

# Language Selector
language_selector()

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"

# Custom CSS
st.markdown("""
    <style>
    .map-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .stat-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
    <div class="map-header">
        <h1 style="margin: 0;">🗺️ {t('analytics') if t('analytics') != 'analytics' else 'Grievance Map'}</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
            Geographic visualization of citizen grievances across India
        </p>
    </div>
""", unsafe_allow_html=True)

# Fetch grievances
@st.cache_data(ttl=30)
def fetch_grievances():
    try:
        response = requests.get(f"{API_BASE_URL}/grievances/", timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and "grievances" in data:
            return data["grievances"]
        elif isinstance(data, list):
            return data
        return []
    except Exception as e:
        st.error(f"Error fetching grievances: {str(e)}")
        return []

# Get grievances
grievances = fetch_grievances()

# DEBUG: Show what we got from API
st.sidebar.markdown("### 🐛 Debug Info")
if grievances:
    for g in grievances[:3]:
        st.sidebar.text(f"ID {g.get('id')}: {g.get('latitude', 'NULL')}, {g.get('longitude', 'NULL')}")

# Note: Coordinates should come from database
# Only generate for old grievances that don't have coordinates
import random
for grievance in grievances:
    # ONLY generate if coordinates are truly missing (None or 0)
    if (grievance.get('latitude') is None or grievance.get('latitude') == 0 or
        grievance.get('longitude') is None or grievance.get('longitude') == 0):
        # Use grievance ID as seed for consistent coordinates
        random.seed(grievance.get('id', 0))
        lat, lon, city = parse_location_to_coordinates(
            grievance.get('location', ''),
            grievance_id=grievance.get('id', 0)
        )
        grievance['latitude'] = lat
        grievance['longitude'] = lon
        grievance['city'] = city
        # Reset random seed
        random.seed()
    else:
        # Use database coordinates (manually marked or previously saved)
        # Extract city name from location if available
        grievance['city'] = grievance.get('location', 'Unknown').split(',')[0] if grievance.get('location') else 'Unknown'


# Sidebar filters
st.sidebar.markdown("### 🔍 Filters")

# Status filter
status_options = ['All'] + list(set([g.get('status', 'Unknown') for g in grievances]))
selected_status = st.sidebar.selectbox(
    f"{t('status') if t('status') != 'status' else 'Status'}",
    status_options
)

# Category filter
category_options = ['All'] + list(set([g.get('category', 'Unknown') for g in grievances]))
selected_category = st.sidebar.selectbox(
    f"{t('category') if t('category') != 'category' else 'Category'}",
    category_options
)

# Priority filter
priority_options = ['All'] + list(set([g.get('priority', 'Unknown') for g in grievances]))
selected_priority = st.sidebar.selectbox(
    f"{t('priority') if t('priority') != 'priority' else 'Priority'}",
    priority_options
)

# Apply filters
filtered_grievances = grievances
if selected_status != 'All':
    filtered_grievances = [g for g in filtered_grievances if g.get('status') == selected_status]
if selected_category != 'All':
    filtered_grievances = [g for g in filtered_grievances if g.get('category') == selected_category]
if selected_priority != 'All':
    filtered_grievances = [g for g in filtered_grievances if g.get('priority') == selected_priority]

# Statistics
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Statistics")

total_grievances = len(filtered_grievances)
pending = len([g for g in filtered_grievances if g.get('status') == 'Pending'])
in_progress = len([g for g in filtered_grievances if g.get('status') == 'In Progress'])
resolved = len([g for g in filtered_grievances if g.get('status') == 'Resolved'])

st.sidebar.metric("Total Grievances", total_grievances)
st.sidebar.metric("🔴 Pending", pending)
st.sidebar.metric("🟡 In Progress", in_progress)
st.sidebar.metric("🟢 Resolved", resolved)

# Map options
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Map Options")
use_clustering = st.sidebar.checkbox("Enable Marker Clustering", value=True)
map_height = st.sidebar.slider("Map Height (px)", 400, 800, 600, 50)

# Main content
if filtered_grievances:
    # Show map
    render_grievance_map(filtered_grievances, height=map_height, use_clustering=use_clustering)
    
    # Show breakdown by city
    st.markdown("---")
    st.subheader("📍 Grievances by City")
    
    city_counts = {}
    for g in filtered_grievances:
        city = g.get('city', 'Unknown')
        city_counts[city] = city_counts.get(city, 0) + 1
    
    # Sort by count
    sorted_cities = sorted(city_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Display top cities
    cols = st.columns(4)
    for idx, (city, count) in enumerate(sorted_cities[:8]):
        with cols[idx % 4]:
            st.metric(city, count)
    
else:
    st.info("📍 No grievances match the selected filters")

# Refresh button
st.markdown("---")
if st.button("🔄 Refresh Map", type="primary"):
    st.cache_data.clear()
    st.rerun()

# Footer
st.markdown("---")
st.caption("🗺️ Map updates every 30 seconds automatically | Click markers for details")
