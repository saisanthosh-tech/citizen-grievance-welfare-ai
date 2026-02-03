"""
Interactive Map Component
Displays grievances on an interactive map with color-coded markers
"""

import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import folium_static
from location_utils import get_india_center

# Status color mapping
STATUS_COLORS = {
    'Pending': 'red',
    'In Progress': 'orange',
    'Resolved': 'green',
    'Rejected': 'gray'
}

# Status icons
STATUS_ICONS = {
    'Pending': 'exclamation-circle',
    'In Progress': 'clock',
    'Resolved': 'check-circle',
    'Rejected': 'times-circle'
}

def get_marker_color(status):
    """Get marker color based on grievance status"""
    return STATUS_COLORS.get(status, 'blue')

def get_marker_icon(status):
    """Get marker icon based on grievance status"""
    return STATUS_ICONS.get(status, 'info-circle')

def create_popup_html(grievance):
    """Create HTML for marker popup"""
    status_color = get_marker_color(grievance.get('status', 'Unknown'))
    
    html = f"""
    <div style="width: 250px; font-family: Arial, sans-serif;">
        <h4 style="margin: 0 0 10px 0; color: #0066cc;">
            🆔 #{grievance.get('id', 'N/A')}
        </h4>
        <p style="margin: 5px 0;">
            <b>Title:</b><br/>
            {grievance.get('title', 'N/A')[:60]}...
        </p>
        <p style="margin: 5px 0;">
            <b>Status:</b> 
            <span style="color: {status_color}; font-weight: bold;">
                {grievance.get('status', 'Unknown')}
            </span>
        </p>
        <p style="margin: 5px 0;">
            <b>Category:</b> {grievance.get('category', 'N/A')}
        </p>
        <p style="margin: 5px 0;">
            <b>Priority:</b> {grievance.get('priority', 'N/A')}
        </p>
        <p style="margin: 5px 0;">
            <b>Location:</b> {grievance.get('location', 'N/A')}
        </p>
    </div>
    """
    return html

def create_grievance_map(grievances, center=None, zoom_start=5, use_clustering=True):
    """
    Create an interactive map with grievance markers
    
    Args:
        grievances: List of grievance dictionaries with lat, lon fields
        center: Tuple of (lat, lon) for map center. Defaults to India center
        zoom_start: Initial zoom level
        use_clustering: Whether to use marker clustering
    
    Returns:
        folium.Map object
    """
    # Set default center to India
    if center is None:
        center = get_india_center()
    
    # Create base map
    m = folium.Map(
        location=center,
        zoom_start=zoom_start,
        tiles='OpenStreetMap',
        control_scale=True
    )
    
    # Add marker cluster if enabled
    if use_clustering and len(grievances) > 10:
        marker_cluster = MarkerCluster(
            name='Grievances',
            overlay=True,
            control=True
        ).add_to(m)
        marker_group = marker_cluster
    else:
        marker_group = m
    
    # Add markers for each grievance
    for grievance in grievances:
        lat = grievance.get('latitude')
        lon = grievance.get('longitude')
        
        if lat is None or lon is None:
            continue  # Skip grievances without coordinates
        
        status = grievance.get('status', 'Unknown')
        color = get_marker_color(status)
        icon_name = get_marker_icon(status)
        
        # Create popup
        popup_html = create_popup_html(grievance)
        popup = folium.Popup(popup_html, max_width=300)
        
        # Create marker
        folium.Marker(
            location=[lat, lon],
            popup=popup,
            tooltip=f"#{grievance.get('id')} - {grievance.get('title', 'N/A')[:30]}...",
            icon=folium.Icon(
                color=color,
                icon=icon_name,
                prefix='fa'
            )
        ).add_to(marker_group)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 180px; height: auto; 
                background-color: white; z-index:9999; font-size:14px;
                border:2px solid grey; border-radius: 5px; padding: 10px">
        <p style="margin: 0 0 10px 0; font-weight: bold;">Grievance Status</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:red"></i> Pending</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:orange"></i> In Progress</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:green"></i> Resolved</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:gray"></i> Rejected</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m

def render_grievance_map(grievances, height=600, use_clustering=True):
    """
    Render grievance map in Streamlit
    
    Args:
        grievances: List of grievances with latitude/longitude
        height: Map height in pixels
        use_clustering: Whether to use marker clustering
    """
    if not grievances:
        st.info("📍 No grievances with location data to display on map")
        return
    
    # Filter grievances with valid coordinates
    valid_grievances = [
        g for g in grievances 
        if g.get('latitude') is not None and g.get('longitude') is not None
    ]
    
    if not valid_grievances:
        st.warning("⚠️ No grievances have location coordinates yet")
        return
    
    # Create map
    m = create_grievance_map(valid_grievances, use_clustering=use_clustering)
    
    # Display map
    folium_static(m, width=None, height=height)
    
    # Show statistics
    st.caption(f"📊 Showing {len(valid_grievances)} grievances on map")
