"""
Admin Login Page
Government staff login to access admin dashboard
"""

import streamlit as st
import hashlib

st.set_page_config(page_title="Admin Login", page_icon="🔐", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background-color: #f9f9f9;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 4px;
        border-left: 4px solid #dc3545;
        margin-bottom: 1rem;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 4px;
        border-left: 4px solid #28a745;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "admin_user" not in st.session_state:
    st.session_state.admin_user = None

st.title("🔐 Admin Access")

st.markdown("""
Government staff login area. If you need admin access, contact your department head.
""")

# Simple password hash (not for production - just for demo)
# In production, use proper authentication (OAuth, LDAP, etc.)
ADMIN_PASSWORDS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "manager": hashlib.sha256("manager123".encode()).hexdigest(),
}

if not st.session_state.authenticated:
    st.divider()
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    st.markdown("### Login with Staff Credentials")
    
    username = st.text_input(
        "Username",
        placeholder="Enter your username",
        help="Your government staff username"
    )
    
    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password",
        help="Your government staff password"
    )
    
    login_button = st.button("🔓 Login", type="primary", use_container_width=True)
    
    if login_button:
        if not username or not password:
            st.markdown("""
                <div class="error-message">
                ⚠️ Please enter both username and password
                </div>
            """, unsafe_allow_html=True)
        else:
            # Check credentials (demo only - not secure for production)
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            if username in ADMIN_PASSWORDS and ADMIN_PASSWORDS[username] == password_hash:
                st.session_state.authenticated = True
                st.session_state.admin_user = username
                st.rerun()
            else:
                st.markdown("""
                    <div class="error-message">
                    ❌ Invalid username or password
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    st.warning("""
    **Demo Credentials:**
    - Username: `admin` | Password: `admin123`
    - Username: `manager` | Password: `manager123`
    
    (In production, use your actual government authentication system)
    """)
    
    st.info("""
    **Why do we need login?**
    
    Only government staff should access:
    - All citizen grievances and personal information
    - Admin dashboard and management tools
    - Sensitive data about government services
    
    This protects citizen privacy.
    """)

else:
    # Logged in state
    st.markdown(f"""
        <div class="success-message">
        ✓ Welcome, {st.session_state.admin_user.title()}! You are now logged in.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    You can now access the Admin Dashboard to:
    - View all grievances
    - Update grievance status
    - Generate reports
    - Assign grievances to staff
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Go to Admin Dashboard", type="primary", use_container_width=True):
            st.switch_page("pages/04_Admin_Dashboard.py")
    
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("pages/app_home.py")
    
    st.divider()
    
    if st.button("🔓 Logout", type="secondary"):
        st.session_state.authenticated = False
        st.session_state.admin_user = None
        st.rerun()

# Footer
st.divider()
st.markdown("""
---
**Security Notice:** This is a demo system. In production:
- Use enterprise authentication (Active Directory, OAuth, SAML)
- Implement rate limiting to prevent brute force attacks
- Enable multi-factor authentication
- Use HTTPS only
- Keep audit logs of admin actions
""")
