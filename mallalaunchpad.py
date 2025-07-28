# mallalaunchpad.py (MallaLaunchpad X - The Career Co-Pilot)

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
import datetime
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="MallaLaunchpad X",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LOTTIE ANIMATION LOADER ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- 2. SECURE FIREBASE INITIALIZATION ---
try:
    # This block initializes Firebase using the secure credentials from secrets.toml
    firebase_config = st.secrets["firebase_web_config"]
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase_admin_sdk"]))
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()
except Exception as e:
    st.error("🚨 Firebase configuration failed. This is likely an issue with your secrets on Streamlit Cloud.")
    st.error(f"Specific Error: {e}")
    st.stop()

# --- 3. MODULE IMPORTS (We'll build these advanced modules next) ---
# from modules.job_tracker import job_tracker_pro # Assuming this is the Kanban version
# from modules.interview_sim import interview_simulator # Assuming this is the chat version
# ... import other advanced modules as they are built

# --- 4. STYLISH LOGIN UI with ANIMATION ---
def login_ui():
    st.title("Welcome to MallaLaunchpad X ✨")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Your AI-Powered Career Co-Pilot")
        st.markdown("Go beyond tracking. Get proactive insights, live resume feedback, and interview coaching that lands you the job.")
        
        # Login Form
        with st.form("login_form"):
            st.subheader("Login")
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Secure Login", use_container_width=True, type="primary"):
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    st.session_state["user"] = user
                    st.rerun()
                except Exception:
                    st.error("❌ Invalid email or password.")
        
        # Signup Form
        with st.form("signup_form"):
            st.subheader("Create an Account")
            email = st.text_input("Email", placeholder="your@email.com", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            if st.form_submit_button("Create My Account", use_container_width=True):
                try:
                    user = auth.create_user_with_email_and_password(email, password)
                    st.session_state["user"] = user
                    uid = user['localId']
                    db.collection("users").document(uid).set({"email": email, "joined": datetime.datetime.now(datetime.timezone.utc)})
                    st.success("✅ Account created! Welcome aboard.")
                    st.rerun()
                except Exception:
                    st.error("❌ Account may already exist or email is invalid.")

    with col2:
        # Load a beautiful Lottie animation
        lottie_url = "https://lottie.host/95282928-1329-4538-9189-ab2d62725593/a3bkyV2s6l.json"
        lottie_animation = load_lottieurl(lottie_url)
        if lottie_animation:
            st_lottie(lottie_animation, height=400, key="login_animation")

# --- 5. THE MAIN APPLICATION LAUNCHER ---
def launch_app():
    user = st.session_state.get("user")
    uid = user["localId"]
    user_email = user['email']

    # --- Modern Sidebar Navigation ---
    with st.sidebar:
        st.image("https://i.imgur.com/5J6l4UH.png", use_column_width=True)
        st.markdown(f"Welcome, **{user_email.split('@')[0]}**")
        
        page = option_menu(
            menu_title="MallaLaunchpad X",
            options=["Today", "Resume Editor", "Job Discovery", "Interview Prep", "Tracker", "Admin"],
            icons=['bi-sun-fill', 'bi-file-earmark-text-fill', 'bi-search', 'bi-camera-video-fill', 'bi-kanban-fill', 'bi-shield-lock-fill'],
            menu_icon="bi-rocket-takeoff-fill", default_index=0,
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

    # --- Page Routing ---
    if page == "Today":
        st.title(f"☀️ Your Dashboard, {user_email.split('@')[0]}")
        st.markdown("Here's your personalized command center for your job search.")
        
        # --- Mock Dashboard ---
        st.subheader("Your Next Step:")
        st.info("🚀 **AI Suggestion:** Your resume is a 75% match for the new 'Data Analyst' role you saved. Let's optimize it in the **Resume Editor**.")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Jobs Tracked", "12", "2 New")
        col2.metric("Interviews", "1", "Upcoming")
        col3.metric("Avg. Resume Score", "82%", "up 5%")
        
        st.subheader("Proactive Job Discovery")
        st.success("✨ **New Opportunity Found:** A 'Senior Python Developer' role at **TechCorp** just opened up. It's a 92% match with your profile. [View Details](#)")

    elif page == "Resume Editor":
        st.title("✍️ Interactive Resume Editor")
        st.info("This is where the live resume editor with real-time AI feedback will be built using streamlit-ace.")
        # from modules.resume_editor import live_resume_editor
        # live_resume_editor(uid, db)

    elif page == "Job Discovery":
        st.title("🛰️ Proactive Job Discovery Engine")
        st.info("This is where the AI-powered job discovery engine will push new opportunities.")
        # from modules.job_discovery import job_discovery_engine
        # job_discovery_engine(uid, db)

    elif page == "Interview Prep":
        st.title("🎥 Interview Preparation Center")
        st.info("This is where you'll find AI question banks and the video practice tool.")
        # from modules.interview_prep import interview_prep_center
        # interview_prep_center(uid, db)

    elif page == "Tracker":
        st.info("Loading your advanced job tracker...")
        # from modules.job_tracker import job_tracker_pro
        # job_tracker_pro(uid, db)

    elif page == "Admin":
        if uid == "REPLACE_WITH_YOUR_ADMIN_FIREBASE_UID":
             st.title("👑 Admin Analytics")
             # from modules.analytics import admin_analytics
             # admin_analytics(db)
        else:
            st.error("🔒 You do not have permission to access this page.")

# --- App Start Point ---
if "user" not in st.session_state:
    login_ui()
else:
    launch_app()
