"""
Authentication Page - Login & Signup
Users can register and login to access the grievance system
"""

import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(page_title="Login / Register", page_icon="🔐", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .auth-container {
        max-width: 500px;
        margin: 3rem auto;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 8px;
        color: white;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 4px;
        border-left: 4px solid #28a745;
        margin-bottom: 1rem;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 4px;
        border-left: 4px solid #dc3545;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #e7f3ff;
        color: #004085;
        padding: 1rem;
        border-radius: 4px;
        border-left: 4px solid #0066cc;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "auth_token" not in st.session_state:
    st.session_state.auth_token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "submission_history" not in st.session_state:
    st.session_state.submission_history = []

# Check if already logged in
if st.session_state.auth_token:
    st.success(f"✅ Logged in as {st.session_state.user_info.get('email', 'User')}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Go to Submit Grievance", use_container_width=True):
            st.switch_page("pages/01_Submit_Grievance.py")
    with col2:
        if st.button("🔍 Track Grievance", use_container_width=True):
            st.switch_page("pages/02_Track_Grievance.py")
    
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.auth_token = None
        st.session_state.user_info = None
        st.rerun()
else:
    st.title("🔐 Citizen Account")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["📝 Register", "🔓 Login"])
    
    # ============ REGISTRATION TAB ============
    with tab1:
        st.markdown("### Create Your Account")
        st.markdown("""
        Register to submit and track your grievances. Your account is secure and 
        helps us maintain a record of your interactions with government services.
        """)
        
        st.divider()
        
        with st.form("registration_form"):
            name = st.text_input(
                "Full Name",
                placeholder="e.g., Rajesh Kumar",
                help="Your full name as it appears in official documents"
            )
            
            email = st.text_input(
                "Email Address",
                placeholder="e.g., rajesh.kumar@email.com",
                help="We'll use this to verify your account and send updates"
            )
            
            phone = st.text_input(
                "Phone Number (Optional)",
                placeholder="e.g., 9876543210",
                help="Optional - helps us contact you faster"
            )
            
            password = st.text_input(
                "Create Password",
                type="password",
                placeholder="Min 6 characters",
                help="Strong password with mix of letters, numbers, symbols"
            )
            
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password"
            )
            
            st.info("""
            **Password Requirements:**
            - At least 6 characters
            - Mix of uppercase and lowercase letters
            - Include numbers and symbols for better security
            """)
            
            submit_register = st.form_submit_button(
                "✅ Create Account",
                use_container_width=True,
                type="primary"
            )
        
        if submit_register:
            errors = []
            
            if not name.strip():
                errors.append("Please enter your full name")
            if not email.strip():
                errors.append("Please enter your email address")
            if not password.strip():
                errors.append("Please create a password")
            if len(password) < 6:
                errors.append("Password must be at least 6 characters")
            if password != confirm_password:
                errors.append("Passwords do not match")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                with st.spinner("Creating your account..."):
                    try:
                        response = requests.post(
                            "http://localhost:8000/auth/register",
                            json={
                                "email": email.strip().lower(),
                                "name": name.strip(),
                                "phone": phone.strip() if phone.strip() else None,
                                "password": password
                            },
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.auth_token = result.get("access_token")
                            st.session_state.user_info = result.get("user", {})
                            
                            st.markdown("""
                                <div class="success-box">
                                ✓ Account created successfully! Welcome to the system.
                                </div>
                            """, unsafe_allow_html=True)
                            
                            st.info(f"👋 Welcome, {name}! Your account is ready.")
                            st.success("Redirecting to submit your grievance...")
                            st.switch_page("pages/01_Submit_Grievance.py")
                        else:
                            error_msg = "Registration failed"
                            try:
                                error_data = response.json()
                                if 'detail' in error_data:
                                    error_msg = error_data['detail']
                            except:
                                pass
                            
                            st.error(f"❌ {error_msg}")
                    
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to server. Please try again later.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # ============ LOGIN TAB ============
    with tab2:
        st.markdown("### Login to Your Account")
        st.markdown("""
        Enter your credentials to access your account and manage your grievances.
        """)
        
        st.divider()
        
        with st.form("login_form"):
            email = st.text_input(
                "Email Address",
                placeholder="e.g., rajesh.kumar@email.com"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )
            
            submit_login = st.form_submit_button(
                "🔓 Login",
                use_container_width=True,
                type="primary"
            )
        
        if submit_login:
            if not email.strip():
                st.error("❌ Please enter your email")
            elif not password.strip():
                st.error("❌ Please enter your password")
            else:
                with st.spinner("Logging in..."):
                    try:
                        response = requests.post(
                            "http://localhost:8000/auth/login",
                            json={
                                "email": email.strip().lower(),
                                "password": password
                            },
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.auth_token = result.get("access_token")
                            st.session_state.user_info = result.get("user", {})
                            
                            st.markdown("""
                                <div class="success-box">
                                ✓ Login successful!
                                </div>
                            """, unsafe_allow_html=True)
                            
                            user_name = st.session_state.user_info.get('name', 'User')
                            st.success(f"👋 Welcome back, {user_name}!")
                            st.switch_page("pages/01_Submit_Grievance.py")
                        else:
                            error_msg = "Invalid email or password"
                            try:
                                error_data = response.json()
                                if 'detail' in error_data:
                                    error_msg = error_data['detail']
                            except:
                                pass
                            
                            st.error(f"❌ {error_msg}")
                    
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to server. Please try again later.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # ============ ADDITIONAL INFO ============
    st.divider()
    st.markdown("### 🛡️ About Your Account Security")
    st.markdown("""
    **Your data is protected by:**
    - ✅ Encrypted password storage
    - ✅ JWT token-based authentication
    - ✅ Secure HTTPS communication
    - ✅ Government-grade security standards
    
    **What you get:**
    - 📝 Submit unlimited grievances
    - 🔍 Track all your grievances
    - 📊 View resolution status
    - 🔔 Get updates on your submissions
    - 📋 Access your grievance history
    """)
