"""
Submit Grievance Page
Citizens submit their grievances with optional location and automatic AI categorization
"""

import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Submit Grievance", page_icon="📝", layout="wide")

# ============ AUTHENTICATION CHECK ============
if not st.session_state.get("auth_token"):
    st.error("🔐 Please login first to submit grievances")
    st.info("👉 Go to the **Login** page to create an account or sign in")
    st.stop()

# Custom CSS
st.markdown("""
    <style>
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
    .result-section {
        background-color: #f0f7ff;
        padding: 1.5rem;
        border-left: 4px solid #0066cc;
        border-radius: 4px;
        margin-top: 1rem;
        color: #1a1a1a;
    }
    .category-badge {
        background-color: #0066cc;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: 600;
    }
    .form-section {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    /* Fix metric cards for visibility */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        border: 1px solid #e0e0e0 !important;
    }
    [data-testid="stMetricValue"] {
        color: #1a1a1a !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricLabel"] {
        color: #666666 !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "submission_history" not in st.session_state:
    st.session_state.submission_history = []
if "api_error" not in st.session_state:
    st.session_state.api_error = None

st.title("📝 Submit Your Grievance")

st.markdown("""
Tell us about your concern. Our system will automatically categorize your issue 
and identify relevant government support programs.
""")

# Reference guidance
st.info("""
**What should you include in your grievance?**

- **What is the problem?** (e.g., "Potholes on Main Street", "No water supply for 3 days")
- **Where did it happen?** (Location details help us respond faster)
- **When did it start?** (Dates or timeframe)
- **How does it affect you?** (Impact on your daily life or community)
- **Any photos or details?** (More information helps us resolve faster)

We will automatically identify which government programs or departments can help you.
""")

# Form
st.markdown('<div class="form-section">', unsafe_allow_html=True)

grievance_title = st.text_input(
    "Subject of Your Concern",
    placeholder="e.g., Water shortage in Sector 4",
    help="A brief description of what you want to report"
)

grievance_description = st.text_area(
    "Please Describe the Issue in Detail",
    placeholder="Tell us:\n- What is the problem?\n- When did it start?\n- How does it affect you?\n- Any other details that would help us understand",
    height=150,
    help="The more details you provide, the better we can assist you"
)

# Photo upload section
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

grievance_location = st.text_input(
    "Your Location (Optional)",
    placeholder="e.g., Ward No. 5, Sector 4",
    help="Helps us better understand issues in different areas"
)

submit_button = st.button(
    "📮 Submit Grievance",
    type="primary",
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)

# Handle submission
if submit_button:
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
        with st.spinner("Processing your grievance..."):
            try:
                # Add authentication header with JWT token
                headers = {
                    "Authorization": f"Bearer {st.session_state.auth_token}"
                }
                
                response = requests.post(
                    "http://localhost:8000/grievances/",
                    json={
                        "title": grievance_title,
                        "description": grievance_description,
                        "location": grievance_location if grievance_location else None
                    },
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Success with celebration
                    st.balloons()
                    st.toast("✅ Grievance submitted successfully!", icon="✅")
                    
                    st.markdown("""
                        <div class="success-message">
                        ✓ Your grievance has been received and analyzed by our AI system.
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display results with AI confidence
                    st.markdown('<div class="result-section">', unsafe_allow_html=True)
                    st.markdown("### 🤖 AI Analysis Results")
                    
                    # Backend returns data at top level, not under 'grievance' key
                    grievance_data = result
                    analysis = result.get("analysis_metadata", {})
                    
                    # Confidence Score
                    confidence = grievance_data.get('confidence_score', 0)
                    confidence_pct = int(confidence * 100)
                    
                    st.markdown("#### 🎯 Classification Confidence")
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.progress(confidence)
                        st.caption(f"AI Confidence: {confidence_pct}% - " + 
                                  ("Excellent" if confidence_pct > 80 else "Good" if confidence_pct > 60 else "Fair"))
                    
                    with col2:
                        st.metric(
                            label="Confidence",
                            value=f"{confidence_pct}%",
                            delta="High" if confidence_pct > 70 else "Medium"
                        )
                    
                    st.markdown("---")
                    
                    # Category and Priority
                    st.markdown("#### 📊 Classification Details")
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        category = grievance_data.get('category', 'Unknown')
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
                        priority = grievance_data.get('priority', 'Medium')
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
                    
                    st.markdown("---")
                    
                    # Schemes
                    schemes = analysis.get('suggested_schemes', []) or grievance_data.get('suggested_schemes', [])
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
                                    </p>
                                </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    # AI Reasoning
                    with st.expander("🔍 Why This Classification?", expanded=True):
                        explanation = analysis.get('explanation', {})
                        st.write(f"**Detection Method**: {explanation.get('category_detection', 'Keyword matching')}")
                        st.write(f"**Priority Reasoning**: {explanation.get('priority_reason', 'Based on urgency keywords')}")
                        
                        if explanation.get('relevant_keywords'):
                            st.write("**Keywords Detected:**")
                            for cat, count in explanation.get('relevant_keywords', {}).items():
                                if count > 0:
                                    st.write(f"- {cat}: {count} keyword(s)")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Grievance ID
                    grievance_id = grievance_data.get('id', 'N/A')
                    st.markdown(f"**Your Grievance ID:** `{grievance_id}` (Save this to track your grievance)")
                    
                    # Add to history
                    st.session_state.submission_history.append({
                        'id': grievance_id,
                        'title': grievance_title,
                        'category': analysis.get('category'),
                        'priority': analysis.get('priority'),
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'status': 'Pending'
                    })
                    
                    st.success("✅ Submission successful! You can now track your grievance.")
                    
                else:
                    error_msg = "Submission failed"
                    try:
                        error_data = response.json()
                        if 'detail' in error_data:
                            error_msg += f": {error_data['detail']}"
                    except:
                        error_msg += f": Status {response.status_code}"
                    
                    st.markdown(f"""
                        <div class="error-message">
                        ⚠️ {error_msg}
                        </div>
                    """, unsafe_allow_html=True)
                    
            except requests.exceptions.ConnectionError:
                st.markdown("""
                    <div class="error-message">
                    ⚠️ Cannot connect to the backend service. Please try again later or contact support.
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                    <div class="error-message">
                    ⚠️ An error occurred: {str(e)}
                    </div>
                """, unsafe_allow_html=True)

# Display submission history
if st.session_state.submission_history:
    st.divider()
    st.markdown("### Your Recent Submissions")
    
    for submission in st.session_state.submission_history[-5:]:
        with st.expander(f"📋 {submission.get('title', 'N/A')} - {submission.get('category', 'N/A')}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Status", submission.get('status', 'Pending'))
            with col2:
                st.metric("Urgency", submission.get('priority', 'Medium'))
            with col3:
                st.metric("ID", submission.get('id', 'N/A'))
            st.caption(f"Submitted: {submission.get('timestamp', 'N/A')}")
