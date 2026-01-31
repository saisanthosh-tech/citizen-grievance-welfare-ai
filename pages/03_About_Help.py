"""
About & Help Page
Information about the system and comprehensive support
"""

import streamlit as st

st.set_page_config(page_title="About & Help", page_icon="❓", layout="wide")

st.title("❓ About & Help")

st.markdown("""
This page provides information about the Citizen Grievance & Welfare Intelligence System 
and answers common questions.
""")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["About System", "FAQ", "How to Use", "Contact"])

with tab1:
    st.markdown("### About the Citizen Grievance & Welfare Intelligence System")
    
    st.markdown("""
    The **Citizen Grievance & Welfare Intelligence System** is a government initiative 
    designed to make it easier for citizens to report issues and receive help.
    
    #### Our Mission
    - 🎯 **Simplify:** Make grievance reporting easy and straightforward
    - 🤝 **Connect:** Link citizens with relevant government programs
    - 📊 **Improve:** Use data to improve government services
    - 🛡️ **Protect:** Keep your personal information safe and secure
    
    #### Key Features
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ✓ **Easy to Use**
        Submit grievances in 2 minutes without creating an account
        
        ✓ **Smart Categorization**
        AI identifies which department can help you
        
        ✓ **Track Progress**
        Know the status of your grievance anytime
        """)
    
    with col2:
        st.markdown("""
        ✓ **Program Identification**
        We suggest government schemes that can help
        
        ✓ **Privacy Protected**
        Your data is encrypted and secure
        
        ✓ **Always Free**
        No registration, no fees, no hidden charges
        """)
    
    st.divider()
    
    st.markdown("#### Our Service Categories")
    
    categories = {
        "🏥 Healthcare": "Hospitals, clinics, medical services, health insurance, vaccination programs",
        "📚 Education": "Schools, colleges, scholarships, tuition assistance, literacy programs",
        "💧 Water Supply": "Drinking water, water leaks, water quality, billing issues",
        "🛣️ Roads & Transport": "Potholes, street lights, traffic, public transportation",
        "⚡ Electricity": "Power outages, billing, connections, meter issues",
        "🚽 Sanitation": "Garbage collection, drainage, cleanliness, sewage systems"
    }
    
    for category, description in categories.items():
        st.markdown(f"**{category}**\n{description}")

with tab2:
    st.markdown("### Frequently Asked Questions")
    
    faq_items = [
        {
            "question": "Do I need to create an account or login?",
            "answer": "No! You can submit grievances directly without any account. We believe everyone should have easy access to government services."
        },
        {
            "question": "How do I know my grievance was received?",
            "answer": "Immediately after submission, you'll receive a unique Grievance ID. Save this ID to track your grievance status anytime."
        },
        {
            "question": "How long does it take to resolve a grievance?",
            "answer": "Resolution time depends on the type of issue. Most grievances are acknowledged within 24-48 hours. You can check status anytime using your Grievance ID."
        },
        {
            "question": "Can I submit multiple grievances?",
            "answer": "Yes, you can submit as many grievances as needed. Each will get its own ID for tracking."
        },
        {
            "question": "Is my information kept private?",
            "answer": "Yes, absolutely. Your personal information is encrypted and only shared with relevant government departments to help resolve your issue. We never sell or misuse your data."
        },
        {
            "question": "What if I don't understand the categories?",
            "answer": "Our AI system automatically categorizes your grievance. If you're unsure which category applies, just describe your problem clearly and we'll sort it out."
        },
        {
            "question": "Can I edit my grievance after submitting?",
            "answer": "Contact our support team with your Grievance ID to request changes. For urgent corrections, resubmit with updated information."
        },
        {
            "question": "What are the suggested schemes?",
            "answer": "These are government programs and benefits that might help you. Our AI identifies them based on your grievance category. You can learn more about each scheme or apply through official channels."
        },
        {
            "question": "How can I follow up if nothing changes?",
            "answer": "If your grievance isn't progressing, contact support with your Grievance ID. We'll escalate it to the appropriate department."
        },
        {
            "question": "Is this service available in other languages?",
            "answer": "Currently available in English. We're working on adding more languages. Check back soon!"
        }
    ]
    
    for idx, item in enumerate(faq_items, 1):
        with st.expander(f"{idx}. {item['question']}"):
            st.markdown(item['answer'])

with tab3:
    st.markdown("### Step-by-Step Guide")
    
    st.markdown("#### How to Submit a Grievance")
    
    st.markdown("""
    **Step 1: Open Submit Grievance**
    - Click on "Submit Grievance" in the sidebar or home page
    """)
    
    st.markdown("""
    **Step 2: Write Your Concern**
    - Describe your issue clearly
    - Include specific details (when, where, who, how it affects you)
    - Location information helps us respond faster
    """)
    
    st.markdown("""
    **Step 3: Submit**
    - Click the "Submit Grievance" button
    - The system will analyze your grievance
    """)
    
    st.markdown("""
    **Step 4: Get Your ID**
    - A unique Grievance ID will appear
    - SAVE THIS ID - you'll need it to track your grievance
    - The system will identify the best programs to help you
    """)
    
    st.divider()
    
    st.markdown("#### How to Track Your Grievance")
    
    st.markdown("""
    **Step 1: Open Track Grievance**
    - Click on "Track Grievance" in the sidebar or home page
    """)
    
    st.markdown("""
    **Step 2: Enter Your ID**
    - Input the Grievance ID you received
    - Click Search
    """)
    
    st.markdown("""
    **Step 3: View Status**
    - See current status of your grievance
    - Check which programs can help
    - View official notes and updates
    """)
    
    st.divider()
    
    st.markdown("#### Tips for Better Results")
    
    tips = [
        "📝 Be specific: 'Water leak on Main Street near hospital' is better than 'water problem'",
        "📍 Include location: It helps us send help to the right place",
        "📅 Mention timeline: 'For the past 3 days' is clearer than 'recently'",
        "🔢 Use numbers: '10 potholes' is clearer than 'many potholes'",
        "📸 Describe impact: 'My child can't go to school' shows importance",
        "✅ Proofread: Check your description before submitting"
    ]
    
    for tip in tips:
        st.markdown(f"- {tip}")

with tab4:
    st.markdown("### Contact & Support")
    
    st.info("""
    **Need Help with the System?**
    
    If you're having trouble using this portal, contact our technical support team.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Contact Information
        
        📧 **Email Support**
        support@grievance-welfare.gov.in
        
        📞 **Phone Support**
        1800-GRIEVANCE (toll-free)
        Monday-Friday, 9 AM - 5 PM IST
        
        🕐 **Online Chat**
        Available on home page
        """)
    
    with col2:
        st.markdown("""
        #### Grievance Help
        
        If you have a problem with a grievance:
        
        1. Use your **Grievance ID**
        2. Describe the issue
        3. Contact support
        
        Example:
        "My Grievance ID: GR-123456. 
        I submitted on May 15 but status hasn't changed. 
        Can you help?"
        """)
    
    st.divider()
    
    st.markdown("### Report a Problem with This System")
    
    problem_type = st.selectbox(
        "What's the problem?",
        [
            "Submission not working",
            "Can't track grievance",
            "Feature not working",
            "Confusing instructions",
            "Other issue"
        ]
    )
    
    description = st.text_area(
        "Describe the problem (optional)",
        placeholder="Tell us what's happening...",
        height=100
    )
    
    if st.button("Report Problem", type="primary"):
        if description.strip():
            st.success("✓ Thank you! We've received your report. We'll look into it right away.")
        else:
            st.warning("Please describe the problem so we can help.")
    
    st.divider()
    
    st.markdown("""
    ### About Government Services
    
    This system helps connect you with government programs. Here are some resources:
    
    - 🌐 [Government Portal](https://india.gov.in)
    - 📱 [Citizen Services](https://services.gov.in)
    - 💼 [Welfare Programs](https://welfareprogram.gov.in)
    - 📋 [Official Documents](https://documents.gov.in)
    """)
