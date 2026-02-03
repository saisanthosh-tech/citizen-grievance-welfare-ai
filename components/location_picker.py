"""
Interactive Location Picker Component
Allows users to click on a map to set their exact location
"""

import folium
from streamlit_folium import st_folium
import streamlit as st

def render_location_picker(default_location=(20.5937, 78.9629), zoom=5):
    """
    Render an interactive map for location picking
    
    Args:
        default_location: Tuple of (lat, lon) for initial map center
        zoom: Initial zoom level
    
    Returns:
        Tuple of (latitude, longitude) if location clicked, else None
    """
    
    # Create map centered on India or user's last location
    if 'picked_lat' in st.session_state and st.session_state.picked_lat:
        center = (st.session_state.picked_lat, st.session_state.picked_lon)
        zoom = 13
    else:
        center = default_location
    
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles='OpenStreetMap'
    )
    
    # Add marker if location already picked
    if 'picked_lat' in st.session_state and st.session_state.picked_lat:
        folium.Marker(
            location=[st.session_state.picked_lat, st.session_state.picked_lon],
            popup="Your Location",
            tooltip="Click map to change location",
            icon=folium.Icon(color='red', icon='map-pin', prefix='fa')
        ).add_to(m)
    
    # Add click instruction
    folium.map.Marker(
        [center[0], center[1]],
        icon=folium.DivIcon(html=f"""
            <div style="background-color: white; padding: 10px; border-radius: 5px; 
                        border: 2px solid #0066cc; font-family: Arial; font-size: 12px;">
                📍 Click anywhere on the map to mark your location
            </div>
        """)
    ).add_to(m)
    
    # Render map and capture clicks
    map_data = st_folium(
        m,
        width=700,
        height=400,
        returned_objects=["last_clicked"]
    )
    
    # Check if user clicked on map
    if map_data and map_data.get("last_clicked"):
        clicked_lat = map_data["last_clicked"]["lat"]
        clicked_lon = map_data["last_clicked"]["lng"]
        
        # Store in session state
        st.session_state.picked_lat = clicked_lat
        st.session_state.picked_lon = clicked_lon
        
        return (clicked_lat, clicked_lon)
    
    # Return existing picked location if available
    if 'picked_lat' in st.session_state and st.session_state.picked_lat:
        return (st.session_state.picked_lat, st.session_state.picked_lon)
    
    return None
