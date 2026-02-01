"""
Track Grievance Page
Citizens can check the status of their submitted grievances
"""

import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Track Grievance", page_icon="🔍", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .status-pending {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-left: 4px solid #ffc107;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .status-in-progress {
        background-color: #cce5ff;
        color: #004085;
        padding: 1rem;
        border-left: 4px solid #0066cc;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .status-resolved {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-left: 4px solid #28a745;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .status-rejected {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-left: 4px solid #dc3545;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .grievance-card {
        background-color: #f9f9f9;
        padding: 1.5rem;
        border-radius: 4px;
        border: 1px solid #ddd;
        margin-bottom: 1rem;
    }
    .timeline-item {
        padding: 1rem;
        border-left: 3px solid #0066cc;
        padding-left: 1.5rem;
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
    </style>
""", unsafe_allow_html=True)

st.title("🔍 Track Your Grievance")

st.markdown("""
Enter your grievance ID to check the current status of your submission.
Your ID was provided when you submitted your grievance.
""")

# Search form
col1, col2 = st.columns([3, 1])

with col1:
    grievance_id = st.text_input(
        "Grievance ID",
        placeholder="Enter your 7-digit grievance ID",
        help="The ID you received after submitting your grievance"
    )

with col2:
    st.empty()
    search_button = st.button("🔍 Search", type="primary", use_container_width=True)

# Process search
if search_button or grievance_id:
    if not grievance_id.strip():
        st.warning("⚠️ Please enter a grievance ID")
    else:
        with st.spinner("Searching..."):
            try:
                response = requests.get(
                    f"http://localhost:8000/grievances/?id={grievance_id}",
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    grievances = result.get('grievances', []) if isinstance(result, dict) else result
                    
                    if grievances:
                        grievance = grievances[0]
                        
                        # Determine status CSS class
                        status = grievance.get('status', 'Pending').lower()
                        if status == 'resolved':
                            status_class = "status-resolved"
                            status_emoji = "✓"
                        elif status == 'in progress' or status == 'in_progress':
                            status_class = "status-in-progress"
                            status_emoji = "⏳"
                        elif status == 'rejected':
                            status_class = "status-rejected"
                            status_emoji = "✗"
                        else:
                            status_class = "status-pending"
                            status_emoji = "⏲️"
                        
                        # Display grievance details
                        st.markdown(f'<div class="{status_class}">', unsafe_allow_html=True)
                        st.markdown(f"### {status_emoji} Status: {grievance.get('status', 'Pending')}")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Main details
                        st.markdown('<div class="grievance-card">', unsafe_allow_html=True)
                        st.markdown("#### Grievance Details")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("ID", grievance.get('id', 'N/A'))
                        with col2:
                            st.metric("Category", grievance.get('category', 'Unknown'))
                        with col3:
                            priority = grievance.get('priority', 'Medium')
                            priority_emoji = "🔴" if priority == "High" else ("🟡" if priority == "Medium" else "🟢")
                            st.markdown(f"**Urgency Level**\n{priority_emoji} {priority}")
                        
                        st.divider()
                        
                        st.markdown(f"**Title:** {grievance.get('title', 'N/A')}")
                        st.markdown(f"**Description:** {grievance.get('description', 'N/A')}")
                        
                        if grievance.get('location'):
                            st.markdown(f"**Location:** {grievance.get('location')}")
                        
                        st.markdown(f"**Submitted:** {grievance.get('created_at', 'N/A')}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Analysis details
                        analysis = grievance.get('analysis_metadata', {})
                        if analysis:
                            with st.expander("📊 Analysis Details"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown(f"**Confidence:** {int(analysis.get('confidence', 0) * 100)}%")
                                    if analysis.get('explanation'):
                                        explanation = analysis.get('explanation', {})
                                        st.markdown("**Category Detection:**")
                                        st.caption(explanation.get('category_detection', 'N/A'))
                                
                                with col2:
                                    st.markdown("**Priority Reasoning:**")
                                    st.caption(explanation.get('priority_reason', 'N/A'))
                        
                        # Suggested schemes
                        schemes = grievance.get('suggested_schemes', [])
                        if schemes:
                            st.divider()
                            st.markdown("#### Government Support Programs")
                            for scheme in schemes:
                                st.markdown(f"✓ {scheme}")
                        
                        # Notes section
                        if grievance.get('notes'):
                            st.divider()
                            st.markdown("#### Official Notes")
                            st.info(grievance.get('notes'))
                        
                        # Timeline - Show status history
                        st.divider()
                        st.markdown("#### 📅 Status History")
                        
                        # Import timeline component
                        import sys
                        sys.path.append('.')
                        from components.timeline import render_timeline
                        
                        # Get status history from grievance
                        status_history = grievance.get('status_history', [])
                        render_timeline(status_history)
                        
                        st.divider()
                        st.info("""
                        **What happens next?**
                        
                        1. **Acknowledgement** - We confirm receipt of your grievance
                        2. **Analysis** - Our team reviews your concern
                        3. **Action** - We connect you with the right government program
                        4. **Resolution** - We work to resolve your issue
                        
                        You can check back here anytime to see updates on your grievance.
                        """)
                        
                    else:
                        st.markdown(f"""
                            <div class="error-message">
                            ⚠️ Grievance ID "{grievance_id}" not found
                            </div>
                        """, unsafe_allow_html=True)
                        st.markdown("Please check that you entered the correct ID and try again.")
                
                else:
                    st.markdown("""
                        <div class="error-message">
                        ⚠️ Cannot search for grievances. Please try again later.
                        </div>
                    """, unsafe_allow_html=True)
                    
            except requests.exceptions.ConnectionError:
                st.markdown("""
                    <div class="error-message">
                    ⚠️ Cannot connect to the backend service. Please try again later.
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                    <div class="error-message">
                    ⚠️ An error occurred: {str(e)}
                    </div>
                """, unsafe_allow_html=True)

# Information section
st.divider()
st.markdown("### Need Help?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **I can't find my grievance ID**
    
    - Check your email for a confirmation message
    - The ID is shown immediately after submission
    - Contact our support team for assistance
    """)

with col2:
    st.markdown("""
    **What if my grievance status doesn't change?**
    
    - Give us time to review (usually 24-48 hours)
    - Complex cases may take longer
    - Check back frequently for updates
    - Contact support if no progress after 5 days
    """)
