import streamlit as st
from modules import (
    analytics,
    ats_cv_optimizer,
    cover_letter,
    cv_beautifier,
    interview_sim,
    job_search_ui,
    job_tracker,
    prompts,
    resume_ai,
    roadmap,
)
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import google.generativeai as genai
import os

# Firebase & Gemini configuration
FIREBASE_CONFIG = {
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
}

# Initialize Firebase
firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth = firebase.auth()

# Firestore DB setup
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CONFIG)
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Gemini Pro setup
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Page configuration
st.set_page_config(page_title="MallaLaunchpad", layout="wide")

# Custom CSS styling
st.markdown("""
    <style>
        .css-18e3th9 {padding-top: 1rem;}
        .css-1d391kg {padding: 1rem;}
        .sidebar .sidebar-content {background-color: #111927;}
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.title("🔰 MallaLaunchpad")
    selected = st.radio("Choose Feature", [
        "Job Tracker", "Interview Simulator", "CV Beautifier",
        "Cover Letter Generator", "Resume Optimizer",
        "Career Roadmap", "Job Search UI", "Prompt Toolkit",
        "Admin Analytics"
    ])

# Page routing
if selected == "Job Tracker":
    job_tracker.job_tracker_pro(db)

elif selected == "Interview Simulator":
    interview_sim.interview_chat()

elif selected == "CV Beautifier":
    cv_beautifier.cv_viewer()

elif selected == "Cover Letter Generator":
    cover_letter.generate_cover_letter()

elif selected == "Resume Optimizer":
    ats_cv_optimizer.analyze_resume()

elif selected == "Career Roadmap":
    roadmap.generate_roadmap()

elif selected == "Job Search UI":
    job_search_ui.job_listing_page()

elif selected == "Prompt Toolkit":
    prompts.prompt_lab()

elif selected == "Admin Analytics":
    analytics.admin_dashboard(db)

# Optional footer
st.markdown("---")
st.markdown("🚀 Built with ❤️ by MallaLaunchpad Team")
