# mallalaunchpad.py

import streamlit as st
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore as admin_firestore

# Initialize Firebase
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

db = admin_firestore.client()

# Modules
from modules import (
    job_tracker,
    interview_sim,
    cover_letter,
    cv_beautifier,
    roadmap,
    analytics,
    ats_cv_optimizer,
    job_search_ui,
    prompts,
    resume_ai
)

# Custom Navigation UI
from streamlit_option_menu import option_menu

st.set_page_config(page_title="MallaLaunchpad", layout="wide")
st.markdown("<style>.st-emotion-cache-1v0mbdj {padding: 1rem 2rem;}</style>", unsafe_allow_html=True)

with st.sidebar:
    choice = option_menu(
        "🚀 MallaLaunchpad",
        ["Job Tracker", "Interview Simulator", "Cover Letter", "CV Beautifier", "Learning Roadmap",
         "Resume Optimizer", "Job Search", "Prompt Tools", "Analytics"],
        icons=["kanban", "chat-dots", "envelope", "file-earmark-person", "lightbulb", 
               "check2-square", "search", "stars", "bar-chart"],
        menu_icon="rocket",
        default_index=0,
    )

uid = "test_user_123"  # Replace with dynamic user system if needed

# Routing
if choice == "Job Tracker":
    job_tracker.job_tracker_pro(uid, db)

elif choice == "Interview Simulator":
    interview_sim.simulate_interview()

elif choice == "Cover Letter":
    cover_letter.generate_cover_letter()

elif choice == "CV Beautifier":
    cv_beautifier.beautify_cv()

elif choice == "Learning Roadmap":
    roadmap.generate_roadmap()

elif choice == "Resume Optimizer":
    ats_cv_optimizer.optimize_resume()

elif choice == "Job Search":
    job_search_ui.search_jobs_live()

elif choice == "Prompt Tools":
    prompts.prompt_hub()

elif choice == "Analytics":
    analytics.show_dashboard()
