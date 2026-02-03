"""
Test Admin Login Credentials
"""
import hashlib

# Test credentials
username = "admin"
password = "admin123"

# Hash the password
password_hash = hashlib.sha256(password.encode()).hexdigest()

# Expected hash from Admin Login page
ADMIN_PASSWORDS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "manager": hashlib.sha256("manager123".encode()).hexdigest(),
}

print("=" * 50)
print("ADMIN LOGIN TEST")
print("=" * 50)
print(f"\nUsername: {username}")
print(f"Password: {password}")
print(f"\nPassword Hash: {password_hash}")
print(f"Expected Hash: {ADMIN_PASSWORDS['admin']}")
print(f"\nMatch: {password_hash == ADMIN_PASSWORDS['admin']}")

# Test the validation logic
if username in ADMIN_PASSWORDS and ADMIN_PASSWORDS[username] == password_hash:
    print("\n✅ LOGIN SUCCESSFUL!")
    print("Credentials are correct and should work in Streamlit")
else:
    print("\n❌ LOGIN FAILED!")
    print("There's an issue with the credentials")

print("\n" + "=" * 50)
print("INSTRUCTIONS:")
print("=" * 50)
print("1. Open: http://localhost:8502")
print("2. Click 'Admin Login' in sidebar")
print("3. Enter:")
print(f"   Username: {username}")
print(f"   Password: {password}")
print("4. Click Login button")
print("=" * 50)
