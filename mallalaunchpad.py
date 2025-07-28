# 🔄 Trigger rebuild for Streamlit Cloud cache
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from modules import job_tracker, interview_sim, cover_letter, roadmap, cv_beautifier, analytics

# Page configuration
st.set_page_config(page_title="MallaLaunchpad", layout="wide", page_icon="🧠")

# Initialize Firebase Admin SDK (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": st.secrets["firebase_admin_sdk"]["type"],
        "project_id": st.secrets["firebase_admin_sdk"]["project_id"],
        "private_key_id": st.secrets["firebase_admin_sdk"]["private_key_id"],
        "private_key": st.secrets["firebase_admin_sdk"]["private_key"].replace("\\n", "\n"),
        "client_email": st.secrets["firebase_admin_sdk"]["client_email"],
        "client_id": st.secrets["firebase_admin_sdk"]["client_id"],
        "auth_uri": st.secrets["firebase_admin_sdk"]["auth_uri"],
        "token_uri": st.secrets["firebase_admin_sdk"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["firebase_admin_sdk"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["firebase_admin_sdk"]["client_x509_cert_url"]
    })
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# Sidebar navigation
with st.sidebar:
    st.title("🚀 MallaLaunchpad")
    page = st.radio("Navigate", [
        "Job Tracker",
        "Interview Simulator",
        "Cover Letter Generator",
        "Career Roadmap",
        "CV Beautifier",
        "Admin Dashboard"
    ])

# Load selected module
if page == "Job Tracker":
    job_tracker.job_tracker_pro(db)
elif page == "Interview Simulator":
    interview_sim.run_interview_simulator()
elif page == "Cover Letter Generator":
    cover_letter.generate_cover_letter()
elif page == "Career Roadmap":
    roadmap.build_roadmap()
elif page == "CV Beautifier":
    cv_beautifier.beautify_cv()
elif page == "Admin Dashboard":
    analytics.show_admin_dashboard(db)
