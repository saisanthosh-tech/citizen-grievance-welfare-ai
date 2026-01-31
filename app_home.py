"""
Citizen Grievance & Welfare Intelligence System - Home Page
A government-grade, multi-page web application for grievance management

Design Philosophy:
- Simple, clean, and serious interface
- Focus on clarity and transparency
- Government-grade language and design
- Privacy-first and accessible
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Citizen Grievance & Welfare System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="auto"
)

# Custom CSS for government-grade styling
st.markdown("""
    <style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        color: #1a1a1a;
        background-color: #f5f5f5;
    }
    .main {
        max-width: 1200px;
    }
    .header-section {
        background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
        padding: 3rem 2rem;
        border-radius: 8px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .header-section h1 {
        color: white !important;
        margin: 0;
        font-size: 2.5rem;
    }
    .header-section p {
        color: rgba(255,255,255,0.95);
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
    }
    .feature-card {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #0066cc;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .feature-card h3 {
        color: #0066cc;
        margin-top: 0;
    }
    .feature-card p {
        color: #555;
        line-height: 1.6;
    }
    .info-box {
        background-color: #e8f4f8;
        border-left: 4px solid #0066cc;
        padding: 1.5rem;
        border-radius: 4px;
        margin: 1rem 0;
        color: #1a1a1a;
    }
    .info-box strong {
        color: #004499;
    }
    .btn-large {
        background-color: #0066cc;
        color: white;
        padding: 12px 24px;
        border-radius: 4px;
        text-decoration: none;
        display: inline-block;
        margin: 10px 10px 10px 0;
        font-weight: 600;
        border: none;
    }
    .btn-large:hover {
        background-color: #004499;
    }
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    .stat-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border-top: 3px solid #0066cc;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #0066cc;
    }
    .stat-label {
        color: #666;
        margin-top: 0.5rem;
        font-size: 0.95rem;
    }
    </style>
""", unsafe_allow_html=True)

# Navigation
st.sidebar.title("🏛️ Government Portal")
page = st.sidebar.radio("Navigate to:", [
    "🏠 Home",
    "📝 Submit Grievance",
    "🔍 Track Grievance",
    "❓ About & Help",
    "🔐 Admin Login"
])

# Main content
st.markdown("""
    <div class="header-section">
        <h1>🏛️ Citizen Grievance & Welfare Portal</h1>
        <p>Your voice matters. Report concerns, track progress, access government support programs.</p>
    </div>
""", unsafe_allow_html=True)

if page == "🏠 Home":
    
    # Hero section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Welcome to the Citizen Grievance & Welfare Portal
        
        This is an official government service designed to:
        - **Listen** to your concerns about public services
        - **Categorize** your grievances automatically
        - **Identify** relevant government support programs
        - **Track** the progress of your submission
        
        Your feedback helps us improve public services and better serve you.
        """)
    
    with col2:
        st.metric("Portal Status", "🟢 Operational", "All systems running smoothly")
    
    # Quick action buttons
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Submit a Grievance", use_container_width=True, key="btn_submit"):
            st.switch_page("pages/01_Submit_Grievance.py")
    
    with col2:
        if st.button("🔍 Track Your Grievance", use_container_width=True, key="btn_track"):
            st.switch_page("pages/02_Track_Grievance.py")
    
    with col3:
        if st.button("❓ Get Help", use_container_width=True, key="btn_help"):
            st.switch_page("pages/03_About_Help.py")
    
    # Features
    st.divider()
    st.markdown("### How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3>1️⃣ Submit</h3>
        <p>Tell us about your concern in simple words. No technical knowledge needed.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
        <h3>2️⃣ Analyze</h3>
        <p>Our system automatically identifies the category and recommends relevant programs.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
        <h3>3️⃣ Track</h3>
        <p>Monitor your grievance status and see what's being done to address it.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Information
    st.divider()
    st.markdown("### Important Information")
    
    st.markdown("""
    <div class="info-box">
    <strong>🔒 Your Privacy:</strong> Your personal information is protected and used only to address your grievance and improve services.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <strong>⚖️ Fair Treatment:</strong> All submissions are treated fairly and processed systematically without discrimination.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <strong>📱 Accessibility:</strong> This portal is accessible on all devices - desktop, tablet, and mobile.
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics
    st.divider()
    st.markdown("### Portal Statistics")
    
    try:
        response = requests.get("http://localhost:8000/stats/")
        if response.status_code == 200:
            stats = response.json()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Grievances", stats.get("total_grievances", 0))
            
            with col2:
                high = stats.get("by_priority", {}).get("High", 0)
                st.metric("🔴 Urgent", high)
            
            with col3:
                medium = stats.get("by_priority", {}).get("Medium", 0)
                st.metric("🟡 Standard", medium)
            
            with col4:
                low = stats.get("by_priority", {}).get("Low", 0)
                st.metric("🟢 General", low)
        else:
            st.info("Statistics temporarily unavailable")
    except:
        st.info("Unable to load statistics. Backend may be offline.")
    
    # FAQ
    st.divider()
    st.markdown("### Frequently Asked Questions")
    
    with st.expander("❓ How do I submit a grievance?"):
        st.markdown("""
        1. Click on **Submit a Grievance** button
        2. Fill in the form with details about your concern
        3. Provide a clear description and location (optional)
        4. Click **Submit Grievance**
        5. You'll receive confirmation and tracking details
        """)
    
    with st.expander("❓ How do I track my grievance?"):
        st.markdown("""
        1. Click on **Track Your Grievance** button
        2. Enter your Grievance ID (provided at submission)
        3. View current status and any updates
        4. See recommended government programs
        """)
    
    with st.expander("❓ What happens after I submit?"):
        st.markdown("""
        - Your grievance is automatically categorized
        - Relevant government programs are identified
        - Staff will review and take appropriate action
        - You can track progress anytime
        - Updates will be provided as work progresses
        """)
    
    with st.expander("❓ Is my information safe?"):
        st.markdown("""
        Yes. We take your privacy seriously:
        - Information is encrypted and stored securely
        - Data is used only for grievance resolution
        - We follow government data protection standards
        - You have the right to request your data
        """)
    
    # Footer
    st.divider()
    st.markdown("""
    ---
    <div style="text-align: center; color: #666; font-size: 0.9rem; padding: 2rem 0;">
        <p><strong>Citizen Grievance & Welfare Portal</strong> | Official Government Service</p>
        <p>We listen, we care, we act | Your concerns matter to us</p>
        <p style="font-size: 0.85rem; color: #999;">All grievances are handled with confidentiality and fairness</p>
    </div>
    """, unsafe_allow_html=True)

elif page == "📝 Submit Grievance":
    st.switch_page("pages/01_Submit_Grievance.py")

elif page == "🔍 Track Grievance":
    st.switch_page("pages/02_Track_Grievance.py")

elif page == "❓ About & Help":
    st.switch_page("pages/03_About_Help.py")

elif page == "🔐 Admin Login":
    st.switch_page("pages/04_Admin_Login.py")

import requests
