# 🔄 Trigger rebuild for Streamlit Cloud cache
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from modules import job_tracker, interview_sim, cover_letter, roadmap, cv_beautifier, analytics

# Page configuration
st.set_page_config(page_title="MallaLaunchpad", layout="wide", page_icon="🧠")

# Initialize Firebase (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"].replace("\\n", "\n"),
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"]
    })
    firebase_admin.initialize_app(cred)

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
