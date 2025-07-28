# modules/job_tracker.py (Kanban UI with Firestore)

import streamlit as st
import pandas as pd
import datetime

def display_kanban_board(df):
    """Creates a visually appealing Kanban board from the job dataframe."""
    st.subheader("📋 Your Job Application Pipeline")

    # Define Kanban stages and their corresponding colors
    stages = ["Wishlist", "Applied", "Interview", "Offer", "Rejected"]
    stage_colors = {
        "Wishlist": "#FFC107", "Applied": "#0D6EFD",
        "Interview": "#6F42C1", "Offer": "#198754", "Rejected": "#DC3545"
    }

    cols = st.columns(len(stages))

    for i, stage in enumerate(stages):
        with cols[i]:
            st.markdown(f'<h5 style="color:{stage_colors.get(stage, "#FAFAFA")};">{stage}</h5>', unsafe_allow_html=True)
            
            stage_jobs = df[df["Status"] == stage] if "Status" in df.columns else pd.DataFrame()

            if stage_jobs.empty:
                st.markdown("_No jobs here._")
            else:
                for index, job in stage_jobs.iterrows():
                    st.markdown(
                        f"""
                        <div style="background-color:#262730; padding:15px; border-radius:10px; margin:10px 0; border-left: 5px solid {stage_colors.get(stage)};">
                            <h6 style="margin:0; color:white; font-weight:bold;">{job.get('Role', 'N/A')}</h6>
                            <p style="margin:0; font-size:14px; color:#A9A9A9;">{job.get('Company', 'N/A')}</p>
                            <a href="{job.get('Link', '#')}" target="_blank" style="font-size:12px; color:#636AF2;">Job Link</a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

def job_tracker_pro(uid, db):
    """The main function for the Job Tracker Pro module."""
    st.title("📊 Job Tracker Pro")
    st.markdown("Track your job applications from wishlist to offer with this interactive board.")

    jobs_ref = db.collection("users").document(uid).collection("jobs")

    with st.form("job_form", clear_on_submit=True):
        st.subheader("➕ Add New Job Application")
        col1, col2 = st.columns(2)
        company = col1.text_input("Company Name")
        role = col2.text_input("Job Role")
        status = col1.selectbox("Application Status", ["Wishlist", "Applied", "Interview", "Offer", "Rejected"])
        link = col2.text_input("Job Link/URL")
        submitted = st.form_submit_button("Add to Tracker", use_container_width=True)

        if submitted and company and role:
            new_job_data = {
                "Company": company, "Role": role, "Status": status,
                "Link": link, "AddedOn": datetime.datetime.now(datetime.timezone.utc)
            }
            jobs_ref.add(new_job_data)
            st.success(f"✅ Added '{role}' at '{company}' to your tracker!")

    try:
        jobs_query = jobs_ref.order_by("AddedOn", direction="DESCENDING").stream()
        jobs_list = [job.to_dict() for job in jobs_query]
        
        df = pd.DataFrame(jobs_list) if jobs_list else pd.DataFrame()
        display_kanban_board(df)
            
    except Exception as e:
        st.error(f"Failed to load job data from Firestore: {e}")
