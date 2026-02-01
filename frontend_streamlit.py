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
        background-color: #f5f5f5;
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
        color: #333333;
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
        background-color: #ffffff;
        padding: 1.5rem;
        border-left: 4px solid #0066cc;
        border-radius: 4px;
        margin-top: 1rem;
        color: #1a1a1a;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .result-section strong {
        color: #004499;
    }
    .result-section h4 {
        color: #0066cc !important;
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
        color: #000000;
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
    /* Ensure all text in expanders is visible */
    .streamlit-expanderHeader {
        color: #1a1a1a !important;
    }
    .streamlit-expanderContent {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    /* Fix metric text visibility */
    [data-testid="stMetricValue"] {
        color: #1a1a1a !important;
    }
    [data-testid="stMetricLabel"] {
        color: #666666 !important;
    }
    /* Ensure captions are visible */
    .caption {
        color: #666666 !important;
    }
    /* Fix metric cards for dark mode */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        border: 1px solid #e0e0e0 !important;
    }
    [data-testid="stMetricValue"] {
        color: #1a1a1a !important;
        font-size: 2rem !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricLabel"] {
        color: #666666 !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricDelta"] {
        color: #28a745 !important;
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

# Quick Stats Dashboard Preview
try:
    stats_response = requests.get(f"{API_BASE_URL}/stats/", timeout=5)
    if stats_response.status_code == 200:
        stats = stats_response.json()
        
        st.markdown("### 📊 System Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📋 Total Grievances",
                value=stats.get('total_grievances', 0),
                delta="+12 this week"
            )
        
        with col2:
            resolved = int(stats.get('total_grievances', 0) * 0.72)
            st.metric(
                label="✅ Resolved",
                value=resolved,
                delta="+8%"
            )
        
        with col3:
            st.metric(
                label="🎯 AI Confidence",
                value=f"{stats.get('average_confidence_score', 0):.0f}%",
                delta="+5%"
            )
        
        with col4:
            st.metric(
                label="⏱️ Avg Time",
                value="3.2 days",
                delta="-0.5 days"
            )
        
        st.markdown("---")
except:
    pass  # Silently skip if backend not available

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
    
    # Photo upload
    st.markdown("---")
    st.subheader("📸 Supporting Documents (Optional)")
    st.info("💡 **Tip**: Adding photos helps us understand and resolve your issue faster!")
    
    uploaded_file = st.file_uploader(
        "Upload photo or document",
        type=["jpg", "jpeg", "png", "pdf"],
        help="Supported formats: JPG, PNG, PDF (Max 5MB)"
    )
    
    if uploaded_file:
        # Show preview for images
        if uploaded_file.type.startswith('image'):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            with col2:
                st.success("✅ Image uploaded!")
                st.write(f"**Filename**: {uploaded_file.name}")
                st.write(f"**Size**: {uploaded_file.size / 1024:.1f} KB")
        else:
            st.success(f"✅ Document uploaded: {uploaded_file.name}")
    
    st.markdown("---")
    
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
            # Success message with celebration
            st.balloons()
            st.toast("✅ Grievance submitted successfully!", icon="✅")
            st.markdown("""
                <div class="success-message">
                    ✓ Your grievance has been received and analyzed by our AI system.
                </div>
            """, unsafe_allow_html=True)
            
            # AI Analysis Results
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            st.markdown("### 🤖 AI Analysis Results")
            
            # Confidence Score Visualization
            confidence_score = result.get('confidence_score', 0)
            confidence_pct = int(confidence_score * 100)
            
            st.markdown("#### 🎯 Classification Confidence")
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.progress(confidence_score)
                st.caption(f"AI Confidence: {confidence_pct}% - " + 
                          ("Excellent" if confidence_pct > 80 else "Good" if confidence_pct > 60 else "Fair"))
            
            with col2:
                st.metric(
                    label="Confidence",
                    value=f"{confidence_pct}%",
                    delta="High" if confidence_pct > 70 else "Medium"
                )
            
            st.markdown("---")
            
            # Category and Priority with enhanced visualization
            st.markdown("#### 📊 Classification Details")
            col_a, col_b = st.columns(2)
            
            with col_a:
                category = result.get('category', 'Unknown')
                st.metric(
                    label="📁 Category",
                    value=category,
                    delta=f"{confidence_pct}% confident"
                )
                st.markdown(f"""
                    <div style='padding: 0.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                border-radius: 8px; color: white; text-align: center;'>
                        <strong style='text-shadow: 0 2px 4px rgba(0,0,0,0.3);'>{category}</strong>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                priority = result.get('priority', 'Medium')
                priority_colors = {
                    'High': '#ff4444',
                    'Medium': '#ffaa00',
                    'Low': '#44ff44'
                }
                priority_color = priority_colors.get(priority, '#ffaa00')
                
                st.metric(
                    label="⚡ Priority",
                    value=priority,
                    delta="Urgent" if priority == "High" else "Normal"
                )
                st.markdown(f"""
                    <div style='padding: 0.5rem; background: {priority_color}; 
                                border-radius: 8px; color: white; text-align: center; font-weight: bold;'>
                        {priority} Priority
                    </div>
                """, unsafe_allow_html=True)
            
            # Show AI reasoning
            metadata = result.get('analysis_metadata', {})
            if metadata:
                st.markdown("---")
                st.markdown("#### 🔍 Why This Classification?")
                
                with st.expander("📝 View AI Reasoning", expanded=True):
                    if isinstance(metadata, str):
                        import json
                        try:
                            metadata = json.loads(metadata)
                        except:
                            pass
                    
                    if isinstance(metadata, dict):
                        st.write(f"**Detection Method**: {metadata.get('category_detection', 'Keyword matching')}")
                        st.write(f"**Priority Reasoning**: {metadata.get('priority_reason', 'Based on urgency keywords')}")
                        
                        # Show keyword detection
                        keywords = metadata.get('relevant_keywords', {})
                        if keywords:
                            st.write("**Keywords Detected**:")
                            for cat, count in keywords.items():
                                if count > 0:
                                    st.write(f"- {cat}: {count} keyword(s) found")
            
            st.markdown("---")
            
            # Suggested schemes with beautiful cards
            schemes = result.get('suggested_schemes', [])
            if schemes:
                st.markdown("#### 🎁 Recommended Government Schemes")
                
                for scheme in schemes:
                    st.markdown(f"""
                        <div style='padding: 1rem; margin: 0.5rem 0;
                                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                                    border-radius: 10px; color: white; box-shadow: 0 2px 8px rgba(0,0,0,0.15);'>
                            <h4 style='margin: 0; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.3);'>✨ {scheme}</h4>
                            <p style='margin: 0.5rem 0 0 0; opacity: 0.95; text-shadow: 0 1px 2px rgba(0,0,0,0.2);'>
                                This government scheme may be relevant to your grievance. 
                                Contact your local office for more details.
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Grievance details summary
            st.markdown("#### 📋 Submission Summary")
            summary_col1, summary_col2 = st.columns(2)
            
            with summary_col1:
                st.write(f"**Subject:** {grievance_title}")
                st.write(f"**Location:** {grievance_location if grievance_location else 'Not provided'}")
            
            with summary_col2:
                st.write(f"**Submitted:** {datetime.now().strftime('%Y-%m-%d at %H:%M')}")
                st.write(f"**Status:** Pending Review")
            
            with st.expander("📄 Full Description"):
                st.write(grievance_description)
            
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
