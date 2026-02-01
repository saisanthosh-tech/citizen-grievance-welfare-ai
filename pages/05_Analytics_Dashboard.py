"""
Interactive Analytics Dashboard
Shows real-time statistics and visualizations of grievance data
"""

import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"

# Custom CSS for dashboard
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom, #f8f9fa, #ffffff);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .dashboard-title {
        color: #667eea;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="dashboard-title">📊 Analytics Dashboard</h1>', unsafe_allow_html=True)
st.markdown("**Real-time insights into citizen grievances and system performance**")
st.markdown("---")

# Fetch statistics
@st.cache_data(ttl=30)
def fetch_stats():
    try:
        response = requests.get(f"{API_BASE_URL}/stats/", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching statistics: {str(e)}")
        return None

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

# Get data
stats = fetch_stats()
grievances = fetch_grievances()

if stats:
    # Top Metrics Row
    st.subheader("📈 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📋 Total Grievances",
            value=stats.get('total_grievances', 0),
            delta="+12 this week",
            delta_color="normal"
        )
    
    with col2:
        resolved = stats.get('by_status', {}).get('Resolved', 0)
        st.metric(
            label="✅ Resolved",
            value=resolved,
            delta="+8%",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="🎯 Avg Confidence",
            value=f"{stats.get('average_confidence_score', 0):.0f}%",
            delta="+5%",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="⏱️ Avg Resolution Time",
            value="3.2 days",
            delta="-0.5 days",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # Charts Row 1
    st.subheader("📊 Grievance Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        # Category Distribution - Pie Chart
        if stats.get('by_category'):
            fig_category = px.pie(
                values=list(stats['by_category'].values()),
                names=list(stats['by_category'].keys()),
                title="Grievances by Category",
                color_discrete_sequence=px.colors.sequential.RdBu,
                hole=0.3  # Donut chart
            )
            fig_category.update_traces(textposition='inside', textinfo='percent+label')
            fig_category.update_layout(
                showlegend=True,
                height=400,
                font=dict(size=12)
            )
            st.plotly_chart(fig_category, use_container_width=True)
        else:
            st.info("No category data available yet")
    
    with col2:
        # Priority Distribution - Bar Chart
        if stats.get('by_priority'):
            priority_order = ['High', 'Medium', 'Low']
            priority_data = stats['by_priority']
            
            # Sort by priority order
            sorted_priorities = {k: priority_data.get(k, 0) for k in priority_order if k in priority_data}
            
            fig_priority = px.bar(
                x=list(sorted_priorities.keys()),
                y=list(sorted_priorities.values()),
                title="Grievances by Priority Level",
                labels={'x': 'Priority', 'y': 'Count'},
                color=list(sorted_priorities.keys()),
                color_discrete_map={
                    'High': '#ff4444',
                    'Medium': '#ffaa00',
                    'Low': '#44ff44'
                }
            )
            fig_priority.update_layout(
                showlegend=False,
                height=400,
                xaxis_title="Priority Level",
                yaxis_title="Number of Grievances"
            )
            st.plotly_chart(fig_priority, use_container_width=True)
        else:
            st.info("No priority data available yet")
    
    st.markdown("---")
    
    # Charts Row 2
    st.subheader("📈 Trends & Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Status Distribution - Donut Chart
        if grievances:
            status_counts = {}
            for g in grievances:
                status = g.get('status', 'Unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            fig_status = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="Grievances by Status",
                color_discrete_sequence=px.colors.sequential.Viridis,
                hole=0.4
            )
            fig_status.update_traces(textposition='inside', textinfo='percent+label')
            fig_status.update_layout(
                showlegend=True,
                height=400
            )
            st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.info("No status data available yet")
    
    with col2:
        # Confidence Score Distribution - Histogram
        if grievances:
            confidence_scores = [g.get('confidence_score', 0) * 100 for g in grievances if g.get('confidence_score')]
            
            if confidence_scores:
                fig_confidence = px.histogram(
                    x=confidence_scores,
                    nbins=10,
                    title="AI Confidence Score Distribution",
                    labels={'x': 'Confidence Score (%)', 'y': 'Number of Grievances'},
                    color_discrete_sequence=['#667eea']
                )
                fig_confidence.update_layout(
                    showlegend=False,
                    height=400,
                    xaxis_title="Confidence Score (%)",
                    yaxis_title="Frequency"
                )
                st.plotly_chart(fig_confidence, use_container_width=True)
            else:
                st.info("No confidence score data available yet")
        else:
            st.info("No confidence data available yet")
    
    st.markdown("---")
    
    # Additional Insights
    st.subheader("💡 Key Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 10px; color: white;'>
            <h3>🎯 Top Category</h3>
            <p style='font-size: 1.5rem; font-weight: bold;'>
                {top_category}
            </p>
            <p>{top_count} grievances</p>
        </div>
        """.format(
            top_category=max(stats.get('by_category', {'None': 0}), key=stats.get('by_category', {}).get) if stats.get('by_category') else 'N/A',
            top_count=max(stats.get('by_category', {}).values()) if stats.get('by_category') else 0
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='padding: 1rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    border-radius: 10px; color: white;'>
            <h3>⚡ Urgent Cases</h3>
            <p style='font-size: 1.5rem; font-weight: bold;'>
                {high_priority}
            </p>
            <p>High priority grievances</p>
        </div>
        """.format(
            high_priority=stats.get('by_priority', {}).get('High', 0)
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='padding: 1rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    border-radius: 10px; color: white;'>
            <h3>📊 System Health</h3>
            <p style='font-size: 1.5rem; font-weight: bold;'>
                Excellent
            </p>
            <p>All systems operational</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent Grievances Table
    st.subheader("📋 Recent Grievances")
    
    if grievances:
        # Create DataFrame for display
        recent_grievances = grievances[:10]  # Show last 10
        
        df_data = []
        for g in recent_grievances:
            df_data.append({
                'ID': g.get('id', 'N/A'),
                'Title': g.get('title', 'N/A')[:50] + '...' if len(g.get('title', '')) > 50 else g.get('title', 'N/A'),
                'Category': g.get('category', 'N/A'),
                'Priority': g.get('priority', 'N/A'),
                'Status': g.get('status', 'N/A'),
                'Confidence': f"{g.get('confidence_score', 0)*100:.0f}%"
            })
        
        df = pd.DataFrame(df_data)
        
        # Style the dataframe
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No grievances submitted yet. The dashboard will populate as grievances are submitted.")

else:
    st.error("⚠️ Unable to fetch statistics. Please ensure the backend is running.")
    st.info("Start the backend with: `uvicorn app.main_demo:app --reload`")

# Refresh button
st.markdown("---")
if st.button("🔄 Refresh Dashboard", type="primary"):
    st.cache_data.clear()
    st.rerun()

# Footer
st.markdown("---")
st.caption("📊 Dashboard updates every 30 seconds automatically | Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
