# mallalaunchpad.py (Final Version - Fully Connected)

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
import datetime
from streamlit_option_menu import option_menu

# --- Page Configuration (Must be the first Streamlit command) ---
st.set_page_config(
    page_title="MallaLaunchpad",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Firebase Initialization ---
try:
    firebase_config = st.secrets["firebase_web_config"]
    firebase_admin_creds = st.secrets["firebase_admin_sdk"]
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("GEMINI_API_KEY not found in secrets.toml. AI features will fail.")
        st.stop()

    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()
    storage = firebase.storage()

    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase_admin_sdk"]))
        firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    st.error(f"Firebase configuration failed. Please ensure your .streamlit/secrets.toml file is correct. Error: {e}")
    st.stop()

# --- MODULE IMPORTS ---
# Import all the functions from your upgraded module files
from modules.job_tracker import job_tracker_pro
from modules.interview_sim import interview_simulator
from modules.cover_letter import cover_letter_ai
from modules.resume_ai import resume_ai_suite
from modules.roadmap import career_roadmap
from modules.prompts import prompt_toolkit
from modules.cv_beautifier import cv_beautifier
from modules.ats_cv_optimizer import ats_cv_optimizer
from modules.job_search_ui import job_search_ui
from modules.analytics import admin_analytics

# --- STYLISH LOGIN UI ---
def login_ui():
    st.title("🚀 Welcome to MallaLaunchpad")
    st.markdown("Your all-in-one AI career assistant. Please log in or create an account to continue.")
    col1, col2 = st.columns(2)
    with col1:
        with st.form("login_form"):
            st.subheader("Login")
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login", use_container_width=True):
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    st.session_state["user"] = user
                    st.rerun()
                except Exception:
                    st.error("❌ Invalid email or password.")
    with col2:
        with st.form("signup_form"):
            st.subheader("Create an Account")
            email = st.text_input("Email", placeholder="your@email.com", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            if st.form_submit_button("Create Account", use_container_width=True):
                try:
                    user = auth.create_user_with_email_and_password(email, password)
                    st.session_state["user"] = user
                    uid = user['localId']
                    db.collection("users").document(uid).set({"email": email, "joined": datetime.datetime.now(datetime.timezone.utc)})
                    st.success("✅ Account created! Logging you in...")
                    st.rerun()
                except Exception:
                    st.error("❌ Account may already exist or email is invalid.")

# --- MAIN APPLICATION LAUNCHER ---
def launch_app():
    user = st.session_state.get("user")
    uid = user["localId"]
    
    with st.sidebar:
        st.image("https://i.imgur.com/5J6l4UH.png", use_column_width=True)
        st.markdown(f"Welcome, **{user['email']}**")
        
        # --- Modern Icon-Based Navigation Menu ---
        page = option_menu(
            menu_title="Navigation",
            options=["Home", "Resume AI", "Job Tracker", "Interview Bot", "Generators", "Toolkit", "Admin"],
            icons=['house-fill', 'file-earmark-person-fill', 'clipboard2-data-fill', 'robot', 'pencil-square', 'tools', 'shield-lock-fill'],
            menu_icon="rocket-takeoff-fill", default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#0E1117"},
                "icon": {"color": "#FAFAFA", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#262730"},
                "nav-link-selected": {"background-color": "#636AF2"},
            }
        )
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # --- Page Routing: Connects navigation to the correct module ---
    if page == "Home":
        st.title("🏠 Home Dashboard")
        st.header(f"Welcome back to MallaLaunchpad!")
        st.markdown("Select a tool from the sidebar to get started. All your progress is saved automatically.")
        st.image("https://i.imgur.com/gJ50a7c.png", caption="Your Career Journey Starts Here")

    elif page == "Resume AI":
        resume_ai_suite(uid, db, storage)

    elif page == "Job Tracker":
        job_tracker_pro(uid, db)

    elif page == "Interview Bot":
        interview_simulator()

    elif page == "Generators":
        st.title("✨ AI Generators")
        tab1, tab2, tab3 = st.tabs(["Cover Letter", "CV Beautifier", "Career Roadmap"])
        with tab1:
            cover_letter_ai()
        with tab2:
            cv_beautifier()
        with tab3:
            career_roadmap()

    elif page == "Toolkit":
        st.title("🛠️ Career Toolkit")
        tab1, tab2, tab3 = st.tabs(["ATS Optimizer", "Prompt Toolkit", "Job Search"])
        with tab1:
            ats_cv_optimizer()
        with tab2:
            prompt_toolkit()
        with tab3:
            job_search_ui()
            
    elif page == "Admin":
        # Note: For real security, you should check a 'role' field in the user's Firestore document.
        # This is a simple check for demonstration. Replace with your actual Firebase UID.
        if uid == "REPLACE_WITH_YOUR_ADMIN_FIREBASE_UID":
             admin_analytics(db)
        else:
            st.error("🔒 You do not have permission to access this page.")

# --- App Start Point ---
if "user" not in st.session_state:
    login_ui()
else:
    launch_app()
