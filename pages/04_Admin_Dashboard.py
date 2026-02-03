"""
Admin Dashboard Page
Government staff dashboard for managing grievances
"""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from language_selector import language_selector, t, init_language

# Initialize language
init_language()

st.set_page_config(page_title="Admin Dashboard", page_icon="📋", layout="wide")

# Language Selector
language_selector()

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f7ff;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #0066cc;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0066cc;
        margin: 0.5rem 0;
    }
    .metric-label {
        color: #666;
        font-size: 0.9rem;
    }
    .status-pending {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.5rem 1rem;
        border-radius: 20px;
    }
    .status-in-progress {
        background-color: #cce5ff;
        color: #004085;
        padding: 0.5rem 1rem;
        border-radius: 20px;
    }
    .status-resolved {
        background-color: #d4edda;
        color: #155724;
        padding: 0.5rem 1rem;
        border-radius: 20px;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 4px;
        border-left: 4px solid #dc3545;
        margin-bottom: 1rem;
    }
    .grievance-row {
        background-color: #f9f9f9;
        padding: 1rem;
        border-left: 3px solid #0066cc;
        margin-bottom: 1rem;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Check authentication
if not st.session_state.get("authenticated", False):
    st.warning("⚠️ You need to login to access the admin dashboard.")
    if st.button("Go to Login"):
        st.switch_page("pages/04_Admin_Login.py")
    st.stop()

st.title(f"📊 Admin Dashboard")
st.markdown(f"Welcome, **{st.session_state.admin_user.title()}**!")

# Add logout button
col1, col2, col3 = st.columns([3, 1, 1])
with col3:
    if st.button("🔓 Logout"):
        st.session_state.authenticated = False
        st.session_state.admin_user = None
        st.rerun()

st.divider()

# Statistics Section
st.markdown("### 📈 Dashboard Statistics")

try:
    stats_response = requests.get("http://localhost:8000/stats/", timeout=10)
    
    if stats_response.status_code == 200:
        stats = stats_response.json()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Total Grievances</div>
                <div class="metric-value">""" + str(stats.get('total_grievances', 0)) + """</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            pending_count = stats.get('by_status', {}).get('Pending', 0)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Pending</div>
                <div class="metric-value" style="color: #ffc107;">{pending_count}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            in_progress_count = stats.get('by_status', {}).get('In Progress', 0)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">In Progress</div>
                <div class="metric-value" style="color: #0066cc;">{in_progress_count}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            resolved_count = stats.get('by_status', {}).get('Resolved', 0)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Resolved</div>
                <div class="metric-value" style="color: #28a745;">{resolved_count}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Category breakdown
        st.markdown("### 📂 Grievances by Category")
        
        categories = stats.get('category_breakdown', {})
        if categories:
            # Create bar chart data
            chart_data = pd.DataFrame({
                'Category': list(categories.keys()),
                'Count': list(categories.values())
            })
            
            st.bar_chart(chart_data.set_index('Category'))
            
            # Category table
            with st.expander("View Category Details"):
                st.table(chart_data)
        
        # Priority breakdown
        st.markdown("### 🎯 Grievances by Priority")
        
        priorities = stats.get('priority_breakdown', {})
        if priorities:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                high_count = priorities.get('High', 0)
                st.markdown(f"""
                <div style="background-color: #f8d7da; padding: 1rem; border-radius: 4px; text-align: center;">
                    <strong style="color: #721c24;">🔴 High Priority</strong><br>
                    <span style="font-size: 1.5rem; color: #dc3545; font-weight: bold;">{high_count}</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                medium_count = priorities.get('Medium', 0)
                st.markdown(f"""
                <div style="background-color: #fff3cd; padding: 1rem; border-radius: 4px; text-align: center;">
                    <strong style="color: #856404;">🟡 Medium Priority</strong><br>
                    <span style="font-size: 1.5rem; color: #ffc107; font-weight: bold;">{medium_count}</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                low_count = priorities.get('Low', 0)
                st.markdown(f"""
                <div style="background-color: #d4edda; padding: 1rem; border-radius: 4px; text-align: center;">
                    <strong style="color: #155724;">🟢 Low Priority</strong><br>
                    <span style="font-size: 1.5rem; color: #28a745; font-weight: bold;">{low_count}</span>
                </div>
                """, unsafe_allow_html=True)

except Exception as e:
    st.markdown(f"""
        <div class="error-message">
        ⚠️ Could not load statistics: {str(e)}
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Grievances Management Section
st.markdown("### 📋 Manage Grievances")

# Filter options
col1, col2, col3 = st.columns(3)

with col1:
    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Pending", "In Progress", "Resolved"]
    )

with col2:
    category_filter = st.selectbox(
        "Filter by Category",
        ["All", "Healthcare", "Education", "Water Supply", "Roads & Transport", "Electricity", "Sanitation"]
    )

with col3:
    priority_filter = st.selectbox(
        "Filter by Priority",
        ["All", "High", "Medium", "Low"]
    )

# Fetch grievances
try:
    grievances_response = requests.get("http://localhost:8000/grievances/", timeout=10)
    
    if grievances_response.status_code == 200:
        result = grievances_response.json()
        grievances = result.get('grievances', []) if isinstance(result, dict) else result
        
        # Apply filters
        filtered_grievances = grievances
        
        if status_filter != "All":
            filtered_grievances = [g for g in filtered_grievances if g.get('status') == status_filter]
        
        if category_filter != "All":
            filtered_grievances = [g for g in filtered_grievances if g.get('category') == category_filter]
        
        if priority_filter != "All":
            filtered_grievances = [g for g in filtered_grievances if g.get('priority') == priority_filter]
        
        st.markdown(f"**Showing {len(filtered_grievances)} of {len(grievances)} grievances**")
        
        if filtered_grievances:
            for grievance in filtered_grievances[:20]:  # Show latest 20
                with st.expander(f"📌 {grievance.get('id')} - {grievance.get('title')}"):
                    
                    # Grievance details
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        status = grievance.get('status', 'Unknown')
                        status_emoji = "⏲️" if status == "Pending" else ("⏳" if status == "In Progress" else "✓")
                        st.markdown(f"**Status:** {status_emoji} {status}")
                    
                    with col2:
                        priority = grievance.get('priority', 'Unknown')
                        priority_emoji = "🔴" if priority == "High" else ("🟡" if priority == "Medium" else "🟢")
                        st.markdown(f"**Priority:** {priority_emoji} {priority}")
                    
                    with col3:
                        st.markdown(f"**Category:** {grievance.get('category', 'Unknown')}")
                    
                    st.markdown("---")
                    
                    st.markdown(f"**Title:** {grievance.get('title')}")
                    st.markdown(f"**Description:** {grievance.get('description')}")
                    
                    if grievance.get('location'):
                        st.markdown(f"**Location:** {grievance.get('location')}")
                    
                    st.markdown(f"**Submitted:** {grievance.get('created_at', 'Unknown')}")
                    
                    # Analysis
                    analysis = grievance.get('analysis_metadata', {})
                    if analysis:
                        with st.expander("View Analysis"):
                            st.markdown(f"**Confidence:** {int(analysis.get('confidence', 0) * 100)}%")
                            explanation = analysis.get('explanation', {})
                            st.markdown(f"**Category Detection:** {explanation.get('category_detection', 'N/A')}")
                            st.markdown(f"**Priority Reason:** {explanation.get('priority_reason', 'N/A')}")
                    
                    # Suggested schemes
                    schemes = grievance.get('suggested_schemes', [])
                    if schemes:
                        st.markdown("**Suggested Programs:**")
                        for scheme in schemes:
                            st.markdown(f"- {scheme}")
                    
                    # Status History Timeline
                    status_history = grievance.get('status_history', [])
                    if status_history:
                        with st.expander("📅 View Status History"):
                            import sys
                            sys.path.append('.')
                            from components.timeline import render_timeline
                            render_timeline(status_history)
                    
                    # Management actions
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        new_status = st.selectbox(
                            "Update Status",
                            ["Pending", "In Progress", "Resolved"],
                            key=f"status_{grievance.get('id')}"
                        )
                    
                    with col2:
                        st.empty()
                    
                    with col3:
                        if st.button("💾 Save Changes", key=f"save_{grievance.get('id')}"):
                            try:
                                # Call API to update status
                                response = requests.patch(
                                    f"http://localhost:8000/grievances/{grievance.get('id')}/status",
                                    json={"status": new_status},
                                    timeout=10
                                )
                                
                                if response.status_code == 200:
                                    st.toast(f"🔄 Status updated to {new_status}!", icon="✅")
                                    st.success(f"✅ Status updated to {new_status}!")
                                    if new_status == "Resolved":
                                        st.balloons()
                                    # Refresh the page to show updated data
                                    st.rerun()
                                else:
                                    st.error(f"❌ Failed to update status: {response.status_code}")
                            except Exception as e:
                                st.error(f"❌ Error updating status: {str(e)}")
                    
                    # Delete grievance option (for Resolved/Rejected only)
                    st.markdown("---")
                    status = grievance.get('status', '')
                    if status in ['Resolved', 'Rejected']:
                        st.markdown("**🗑️ Delete Grievance**")
                        st.caption("⚠️ This action cannot be undone. Only delete grievances that are no longer needed.")
                        
                        col_del1, col_del2 = st.columns([1, 2])
                        with col_del1:
                            if st.button("🗑️ Delete", type="secondary", key=f"delete_{grievance.get('id')}"):
                                st.session_state[f"confirm_delete_{grievance.get('id')}"] = True
                        
                        # Confirmation dialog
                        if st.session_state.get(f"confirm_delete_{grievance.get('id')}", False):
                            st.warning(f"⚠️ Are you sure you want to permanently delete grievance #{grievance.get('id')}?")
                            col_conf1, col_conf2 = st.columns(2)
                            
                            with col_conf1:
                                if st.button("✅ Yes, Delete", type="primary", key=f"confirm_yes_{grievance.get('id')}"):
                                    try:
                                        response = requests.delete(
                                            f"http://localhost:8000/grievances/{grievance.get('id')}",
                                            timeout=10
                                        )
                                        
                                        if response.status_code == 200:
                                            st.success(f"✅ Grievance #{grievance.get('id')} deleted successfully!")
                                            st.session_state[f"confirm_delete_{grievance.get('id')}"] = False
                                            st.rerun()
                                        else:
                                            st.error(f"❌ Failed to delete: {response.status_code}")
                                    except Exception as e:
                                        st.error(f"❌ Error deleting grievance: {str(e)}")
                            
                            with col_conf2:
                                if st.button("❌ Cancel", key=f"confirm_no_{grievance.get('id')}"):
                                    st.session_state[f"confirm_delete_{grievance.get('id')}"] = False
                                    st.rerun()
                    else:
                        st.info("💡 Tip: Only Resolved or Rejected grievances can be deleted.")
                    
                    # Add notes
                    notes = st.text_area(
                        "Add Official Notes",
                        placeholder="Add notes about this grievance...",
                        height=80,
                        key=f"notes_{grievance.get('id')}"
                    )
                    
                    if st.button("📝 Update Notes", key=f"notes_btn_{grievance.get('id')}"):
                        st.toast("📝 Notes updated successfully!", icon="✅")
                        st.success("✅ Notes updated successfully!")
        
        else:
            st.info("No grievances match the selected filters.")
    
    else:
        st.markdown("""
            <div class="error-message">
            ⚠️ Could not load grievances. Please try again later.
            </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.markdown(f"""
        <div class="error-message">
        ⚠️ Error loading grievances: {str(e)}
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Export section
st.markdown("### 📥 Export Data")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Export as CSV", use_container_width=True):
        st.info("CSV export functionality would be implemented here")

with col2:
    if st.button("📈 Export as Excel", use_container_width=True):
        st.info("Excel export functionality would be implemented here")

with col3:
    if st.button("📄 Generate Report", use_container_width=True):
        st.info("Report generation would be implemented here")

st.divider()

st.markdown("""
---
**Admin Dashboard Guide:**
- Use filters to find specific grievances
- Click on a grievance to see full details
- Update status and add notes for grievances
- Track progress and resolve issues efficiently
- Export data for reporting and analysis
""")
