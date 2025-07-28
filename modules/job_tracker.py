# modules/job_tracker.py

import streamlit as st
import datetime
from google.cloud.firestore import Client
from google.generativeai import GenerativeModel
import google.generativeai as genai

# Setup Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-pro")

def job_tracker_pro(uid: str, db: Client):
    st.title("🗂️ Smart Kanban Job Tracker + Gemini AI")

    stages = ["Wishlist", "Applied", "Interview", "Offer", "Rejected"]
    user_jobs_ref = db.collection("users").document(uid).collection("jobs")
    jobs_by_stage = {stage: [] for stage in stages}

    job_docs = user_jobs_ref.stream()
    for doc in job_docs:
        job = doc.to_dict()
        job["id"] = doc.id
        if job.get("stage") in jobs_by_stage:
            jobs_by_stage[job["stage"]].append(job)

    st.markdown("### 📊 Your Job Pipeline (with AI help)")
    cols = st.columns(len(stages))

    for idx, stage in enumerate(stages):
        with cols[idx]:
            st.subheader(f"🗂️ {stage} ({len(jobs_by_stage[stage])})")
            for job in jobs_by_stage[stage]:
                with st.expander(f"📌 {job['title']} @ {job['company']}"):
                    st.markdown(f"""
                    - 📍 Location: **{job.get('location', 'N/A')}**
                    - 📅 Applied: `{job.get('applied_date', 'N/A')}`
                    - 🔁 Current Stage: `{job['stage']}`
                    """)

                    # 🔁 Stage change
                    new_stage = st.selectbox("Move to", stages, index=stages.index(stage), key=f"stage_{job['id']}")
                    if new_stage != job["stage"]:
                        user_jobs_ref.document(job["id"]).update({"stage": new_stage})
                        st.success("✅ Stage updated")
                        st.experimental_rerun()

                    # ✏️ Edit Job
                    if st.checkbox("✏️ Edit", key=f"edit_{job['id']}"):
                        new_title = st.text_input("Job Title", value=job["title"], key=f"title_{job['id']}")
                        new_company = st.text_input("Company", value=job["company"], key=f"company_{job['id']}")
                        new_location = st.text_input("Location", value=job["location"], key=f"loc_{job['id']}")
                        new_date = st.date_input("Applied Date", value=datetime.date.fromisoformat(job["applied_date"]), key=f"date_{job['id']}")

                        if st.button("💾 Save", key=f"save_{job['id']}"):
                            user_jobs_ref.document(job["id"]).update({
                                "title": new_title,
                                "company": new_company,
                                "location": new_location,
                                "applied_date": new_date.strftime("%Y-%m-%d")
                            })
                            st.success("✅ Job updated")
                            st.experimental_rerun()

                    # 🤖 Gemini Suggestions
                    if st.button("🤖 Suggest Improvements", key=f"suggest_{job['id']}"):
                        with st.spinner("Gemini is thinking..."):
                            prompt = f"""
                            I'm applying for a job titled '{job['title']}' at '{job['company']}' in location '{job['location']}'.
                            Suggest a better job title or a way to improve my positioning. Also give one interview question to prepare for this stage: {job['stage']}.
                            """
                            response = model.generate_content(prompt)
                            st.markdown("#### 💡 Gemini Suggestions:")
                            st.info(response.text)

                    # 🗑️ Delete
                    if st.button("❌ Delete", key=f"delete_{job['id']}"):
                        user_jobs_ref.document(job["id"]).delete()
                        st.success("🗑️ Deleted")
                        st.experimental_rerun()

    # ➕ Add New Job
    st.divider()
    with st.form("add_job_form", clear_on_submit=True):
        st.subheader("➕ Add New Job")
        title = st.text_input("Job Title")
        company = st.text_input("Company")
        location = st.text_input("Location")
        applied_date = st.date_input("Applied Date", datetime.date.today())
        stage = st.selectbox("Stage", stages)

        submitted = st.form_submit_button("Add Job")
        if submitted:
            job_data = {
                "title": title,
                "company": company,
                "location": location,
                "applied_date": applied_date.strftime("%Y-%m-%d"),
                "stage": stage,
                "status": "Pending",
                "created_at": datetime.datetime.now().isoformat()
            }
            user_jobs_ref.add(job_data)
            st.success("✅ Job added")
            st.experimental_rerun()
