"""
Citizen Grievance & Welfare Intelligence System - Frontend
A government-grade, accessible web interface for submitting and tracking citizen grievances.

Design Philosophy:
- Simple, clean, and serious interface
- Focus on clarity and transparency
- No unnecessary animations or marketing language
- Suitable for public sector e-governance platforms
"""

import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Citizen Grievance & Welfare System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
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
        padding: 2rem 1rem;
    }
    .header-section {
        background-color: #ffffff;
        padding: 2rem;
        border-bottom: 3px solid #0066cc;
        margin-bottom: 2rem;
        border-radius: 4px;
        color: #1a1a1a;
    }
    .header-section h1 {
        color: #0066cc !important;
        margin: 0;
        padding: 0;
    }
    .header-section p {
        color: #555555;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    .form-section {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        color: #1a1a1a;
    }
    .form-section h2, .form-section h3 {
        color: #0066cc;
    }
    .result-section {
        background-color: #f0f7ff;
        padding: 1.5rem;
        border-left: 4px solid #0066cc;
        border-radius: 4px;
        margin-top: 1rem;
        color: #1a1a1a;
    }
    .result-section strong {
        color: #004499;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 4px;
        border-left: 4px solid #28a745;
        margin-bottom: 1rem;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 4px;
        border-left: 4px solid #dc3545;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #e7f3ff;
        padding: 1rem;
        border-radius: 4px;
        border-left: 4px solid #0066cc;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
        line-height: 1.5;
        color: #1a1a1a;
    }
    .info-box strong {
        color: #004499;
        font-weight: 600;
    }
    .category-badge {
        display: inline-block;
        background-color: #0066cc;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .priority-high {
        background-color: #dc3545;
        color: white;
    }
    .priority-medium {
        background-color: #ffc107;
        color: #1a1a1a;
    }
    .priority-low {
        background-color: #28a745;
        color: white;
    }
    .scheme-list {
        list-style-type: none;
        padding: 0;
    }
    .scheme-list li {
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        background-color: #ffffff;
        border-left: 3px solid #0066cc;
        border-radius: 2px;
        color: #1a1a1a;
    }
    input, textarea, select {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }
    label {
        color: #1a1a1a !important;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'submission_history' not in st.session_state:
    st.session_state.submission_history = []
if 'api_error' not in st.session_state:
    st.session_state.api_error = None

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 10

def fetch_grievances():
    """Fetch grievances from backend API."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/grievances/",
            timeout=TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        # Extract grievances from the response structure
        if isinstance(data, dict) and "grievances" in data:
            return data["grievances"]
        elif isinstance(data, list):
            return data
        else:
            return []
    except requests.exceptions.ConnectionError:
        st.session_state.api_error = "Cannot connect to the backend service. Please ensure the backend is running."
        return []
    except requests.exceptions.Timeout:
        st.session_state.api_error = "Backend service is not responding. Please try again."
        return []
    except Exception as e:
        st.session_state.api_error = f"Error fetching grievances: {str(e)}"
        return []

def submit_grievance(title, description, location):
    """Submit grievance to backend API."""
    try:
        payload = {
            "title": title,
            "description": description,
            "location": location
        }
        response = requests.post(
            f"{API_BASE_URL}/grievances/",
            json=payload,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to the backend service. Please ensure the backend is running."
    except requests.exceptions.Timeout:
        return None, "Backend service is not responding. Please try again."
    except requests.exceptions.HTTPError as e:
        error_msg = f"Submission failed: {e.response.status_code}"
        try:
            error_detail = e.response.json()
            if 'detail' in error_detail:
                error_msg += f" - {error_detail['detail']}"
        except:
            pass
        return None, error_msg
    except Exception as e:
        return None, f"Error submitting grievance: {str(e)}"

# Header Section
st.markdown("""
    <div class="header-section">
        <h1 style="color: #0066cc; margin: 0; padding: 0;">🏛️ Citizen Grievance Portal</h1>
        <p style="color: #555; margin: 0.5rem 0 0 0; font-size: 1.1rem;">
            Submit your concerns to help us serve you better. Your feedback is important to improving public services.
        </p>
    </div>
""", unsafe_allow_html=True)

# Information Box
st.markdown("""
    <div class="info-box">
        <strong>How to Submit Your Grievance:</strong><br>
        1. Describe the issue you are facing<br>
        2. Provide your location (optional but helpful)<br>
        3. Submit your grievance<br>
        4. We will automatically categorize your issue and identify relevant government support programs<br>
        <br>
        <strong>Your Privacy:</strong> Your personal information is protected and will only be used to address your grievance and improve services. 
        All submissions are treated fairly and processed systematically.
    </div>
""", unsafe_allow_html=True)

# Display any API errors
if st.session_state.api_error:
    st.markdown(f"""
        <div class="error-message">
            ⚠️ {st.session_state.api_error}
        </div>
    """, unsafe_allow_html=True)
    st.session_state.api_error = None

# Main Form Section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.subheader("📝 Tell Us About Your Concern")
    
    # Reference guidance for users
    st.info("""
    **What should you include in your grievance?**
    
    - **What is the problem?** (e.g., "Potholes on Main Street", "No water supply for 3 days")
    - **Where did it happen?** (Location details help us respond faster)
    - **When did it start?** (Dates or timeframe)
    - **How does it affect you?** (Impact on your daily life or community)
    - **Any photos or details?** (More information helps us resolve faster)
    
    We will automatically identify which government programs or departments can help you.
    """)
    
    # Title input
    grievance_title = st.text_input(
        "Subject of Your Concern",
        placeholder="e.g., Water shortage in Sector 4",
        help="A brief description of what you want to report"
    )
    
    # Description input
    grievance_description = st.text_area(
        "Please Describe the Issue in Detail",
        placeholder="Tell us:\n- What is the problem?\n- When did it start?\n- How does it affect you?\n- Any other details that would help us understand",
        height=150,
        help="The more details you provide, the better we can assist you"
    )
    
    # Location input
    grievance_location = st.text_input(
        "Your Location (Optional)",
        placeholder="e.g., Ward No. 5, Sector 4",
        help="Helps us better understand issues in different areas"
    )
    
    # Submit button
    submit_button = st.button(
        "� Submit Grievance",
        type="primary",
        use_container_width=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar with instructions
with st.sidebar:
    st.markdown("### ✍️ Tips for Your Submission")
    st.markdown("""
    **Be specific:**
    - Include dates and times when possible
    - Describe exactly how the issue affects you
    - Share any relevant details
    
    **What happens next:**
    - Your concern is categorized automatically
    - We identify relevant government programs that can help
    - Your information is kept confidential
    
    All grievances are handled fairly and systematically.
    """)
    
    st.divider()
    st.caption("📱 This is an official government service for your convenience.")

# Handle form submission
if submit_button:
    # Validation
    errors = []
    if not grievance_title.strip():
        errors.append("Please enter a grievance title")
    if not grievance_description.strip():
        errors.append("Please describe your grievance in detail")
    if len(grievance_title.strip()) < 5:
        errors.append("Title should be at least 5 characters")
    if len(grievance_description.strip()) < 20:
        errors.append("Description should be at least 20 characters")
    
    if errors:
        for error in errors:
            st.error(f"❌ {error}")
    else:
        # Submit to backend
        with st.spinner("Processing your grievance..."):
            result, error = submit_grievance(
                grievance_title,
                grievance_description,
                grievance_location
            )
        
        if error:
            st.markdown(f"""
                <div class="error-message">
                    ⚠️ {error}
                </div>
            """, unsafe_allow_html=True)
        else:
            # Success message
            st.markdown("""
                <div class="success-message">
                    ✓ Your grievance has been received. We will review it carefully.
                </div>
            """, unsafe_allow_html=True)
            
            # Display results
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            st.markdown("### What We've Identified")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown(f"""
                    <strong>Category of Your Concern:</strong><br>
                    <span class="category-badge">{result.get('category', 'Unknown')}</span>
                """, unsafe_allow_html=True)
            
            with col_b:
                priority = result.get('priority', 'Medium')
                priority_class = f"priority-{priority.lower()}"
                st.markdown(f"""
                    <strong>Urgency Level:</strong><br>
                    <span class="category-badge {priority_class}">{priority}</span>
                """, unsafe_allow_html=True)
            
            # Suggested schemes
            schemes = result.get('suggested_schemes', [])
            if schemes:
                st.markdown("**Government Support Programs Available:**")
                scheme_html = "<ul class='scheme-list'>"
                for scheme in schemes:
                    scheme_html += f"<li>{scheme}</li>"
                scheme_html += "</ul>"
                st.markdown(scheme_html, unsafe_allow_html=True)
            
            # Grievance details
            st.markdown("**Your Submission Summary:**")
            st.markdown(f"""
            - **Subject:** {grievance_title}
            - **Details:** {grievance_description[:100]}...
            - **Location:** {grievance_location if grievance_location else "Not provided"}
            - **Submitted:** {datetime.now().strftime('%Y-%m-%d at %H:%M')}
            """)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add to history
            st.session_state.submission_history.append({
                'title': grievance_title,
                'category': result.get('category'),
                'priority': result.get('priority'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            })
            
            # Clear form
            st.rerun()

# View Submissions Section
st.divider()
st.markdown('<div class="form-section">', unsafe_allow_html=True)
st.subheader("📋 All Grievances Received")

if st.button("� Refresh List", use_container_width=True):
    st.session_state.refresh = True

grievances = fetch_grievances()

if not grievances:
    if st.session_state.api_error:
        st.info("Please try again later. We are working to resolve this.")
    else:
        st.info("No grievances submitted yet.")
else:
    # Display grievance count
    st.markdown(f"**Total Grievances Received:** {len(grievances)}")
    
    # Priority distribution
    high_priority = len([g for g in grievances if g.get('priority') == 'High'])
    medium_priority = len([g for g in grievances if g.get('priority') == 'Medium'])
    low_priority = len([g for g in grievances if g.get('priority') == 'Low'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔴 Urgent", high_priority)
    with col2:
        st.metric("🟡 Standard", medium_priority)
    with col3:
        st.metric("🟢 General", low_priority)
    
    st.divider()
    
    # Display grievances in a table
    grievance_data = []
    for g in grievances[:10]:  # Show latest 10
        priority_display = "Urgent" if g.get('priority') == 'High' else ("Standard" if g.get('priority') == 'Medium' else "General")
        grievance_data.append({
            '📝 Subject': g.get('title', 'N/A')[:50],
            '📂 Category': g.get('category', 'Unknown'),
            '⏱️ Urgency': priority_display,
            '📅 Date Submitted': g.get('created_at', 'N/A')[:10]
        })
    
    if grievance_data:
        st.dataframe(grievance_data, use_container_width=True, hide_index=True)
    
    st.caption(f"Showing the latest grievances. Total received: {len(grievances)}")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; padding: 2rem 0;">
        <p><strong>Citizen Grievance Portal</strong> | Official Government Service</p>
        <p>We listen, we care, we act | Your concerns matter to us</p>
        <p style="font-size: 0.85rem; color: #999;">All grievances are handled with confidentiality and fairness</p>
    </div>
""", unsafe_allow_html=True)
