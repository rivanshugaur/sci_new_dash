from firebase_admin import firestore
import streamlit as st 
import firebase_admin
import pyrebase
from datetime import datetime
from sci_dashboard import sci_kpi_dashboard  # Adjust if the dashboard function is in a different file

from firebase_admin import credentials
from firebase_admin import auth

firebaseConfig = {
  'apiKey': "AIzaSyCEzM7Bm6woaLDUACGx1_pyi4qbC2pL59A",
  'authDomain': "sci-login-page.firebaseapp.com",
  'projectId': "sci-login-page",
  'storageBucket': "sci-login-page.appspot.com",
  'messagingSenderId': "213502986475",
  'appId': "1:213502986475:web:36106990ec803a6f3096ae",
  'measurementId': "G-6YX55R6H5D",
  'databaseURL': "https://sci-login-page.firebaseio.com"
}

# Firebase Authentication
firebass = pyrebase.initialize_app(firebaseConfig)
auth = firebass.auth()

# Firestore Admin Setup
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")  # path to your downloaded service account key
    firebase_admin.initialize_app(cred)
db = firestore.client()

def is_approved_user(email):
    doc_ref = db.collection("approved_users").document(email)
    doc = doc_ref.get()
    return doc.exists

# SCI Login Page

st.set_page_config(page_title="SCI Dashboard", layout="wide")


# Session state tracking
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "email" not in st.session_state:
    st.session_state.email = ""

# ---------- DASHBOARD ----------
if st.session_state.is_logged_in:
    sci_kpi_dashboard()
    st.stop()

# Tabs: Login | Signup
tab = st.radio("Select Action", ["🔐 Login", "📝 Sign Up", "🔁 Reset Password"])

# ---------- LOGIN ----------
if tab == "🔐 Login":
    st.title("🔐 SCI Dashboard Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)

            if is_approved_user(email):
                st.session_state.is_logged_in = True
                st.session_state.email = email
                st.rerun()
            else:
                st.error("❌ Access denied. You are not approved to use this dashboard.")
        except Exception as e:
            st.error("❌ Login failed, please try again")

# ---------- SIGNUP ----------
elif tab == "📝 Sign Up":
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Create Account"):
        try:
            auth.create_user_with_email_and_password(email, password)
            st.success("✅ Account created. Please log in.")
        except:
            st.error("❌ Account creation failed. Use a strong password (6+ chars).")
            
# -----------Reset password------

elif tab == "🔁 Reset Password":
    email = st.text_input("Enter your registered email")

    if st.button("Send Reset Link"):
        try:
            auth.send_password_reset_email(email)
            st.success(f"✅ Password reset link sent to {email}")
        except Exception as e:
            st.error(f"❌ Failed to send reset email: {e}")