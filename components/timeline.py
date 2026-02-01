"""
Timeline Component for Grievance Status History
Displays a beautiful vertical timeline showing status changes
"""

import streamlit as st
from datetime import datetime

def render_timeline(status_history):
    """
    Render a timeline from status history data
    
    Args:
        status_history: List of dict with keys: status, timestamp, changed_by, action
    """
    if not status_history or len(status_history) == 0:
        st.info("📅 No status history available yet")
        return
    
    # CSS for timeline
    st.markdown("""
        <style>
        .timeline {
            position: relative;
            padding: 0;
            list-style: none;
        }
        .timeline-item {
            position: relative;
            padding-left: 3rem;
            padding-bottom: 2rem;
            border-left: 2px solid #e0e0e0;
        }
        .timeline-item:last-child {
            border-left: 2px solid transparent;
            padding-bottom: 0;
        }
        .timeline-marker {
            position: absolute;
            left: -8px;
            top: 0;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background-color: #0066cc;
            border: 2px solid #ffffff;
            box-shadow: 0 0 0 2px #0066cc;
        }
        .timeline-marker.resolved {
            background-color: #28a745;
            box-shadow: 0 0 0 2px #28a745;
        }
        .timeline-marker.in-progress {
            background-color: #ffc107;
            box-shadow: 0 0 0 2px #ffc107;
        }
        .timeline-content {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .timeline-status {
            font-weight: 600;
            color: #0066cc;
            font-size: 1.1rem;
            margin-bottom: 0.25rem;
        }
        .timeline-action {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }
        .timeline-meta {
            color: #999;
            font-size: 0.85rem;
        }
        .timeline-icon {
            margin-right: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Render timeline
    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    
    for entry in reversed(status_history):  # Show newest first
        status = entry.get('status', 'Unknown')
        timestamp = entry.get('timestamp', '')
        changed_by = entry.get('changed_by', 'system')
        action = entry.get('action', f'Status: {status}')
        
        # Determine marker class based on status
        marker_class = ''
        if status == 'Resolved':
            marker_class = 'resolved'
            icon = '✅'
        elif status == 'In Progress':
            marker_class = 'in-progress'
            icon = '🔄'
        else:
            icon = '📝'
        
        # Format timestamp
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            formatted_time = dt.strftime('%b %d, %Y at %I:%M %p')
        except:
            formatted_time = timestamp
        
        # Render timeline item
        st.markdown(f"""
            <div class="timeline-item">
                <div class="timeline-marker {marker_class}"></div>
                <div class="timeline-content">
                    <div class="timeline-status">
                        <span class="timeline-icon">{icon}</span>{action}
                    </div>
                    <div class="timeline-action">Status: <strong>{status}</strong></div>
                    <div class="timeline-meta">
                        {formatted_time} • by {changed_by}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
