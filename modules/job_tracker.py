
import streamlit as st
import datetime
from google.cloud.firestore import Client

def job_tracker_pro(uid: str, db: Client):
    st.title("🗂️ Job Application Kanban Tracker")

    stages = ["Wishlist", "Applied", "Interview", "Offer", "Rejected"]
    user_jobs_ref = db.collection("users").document(uid).collection("jobs")

    # Load existing jobs
    job_docs = user_jobs_ref.stream()
    jobs_by_stage = {stage: [] for stage in stages}

    for doc in job_docs:
        job = doc.to_dict()
        job["id"] = doc.id
        if job.get("stage") in jobs_by_stage:
            jobs_by_stage[job["stage"]].append(job)

    st.markdown("### 🧾 Job Board")
    cols = st.columns(len(stages))

    for idx, stage in enumerate(stages):
        with cols[idx]:
            st.subheader(f"{stage} ({len(jobs_by_stage[stage])})")
            for job in jobs_by_stage[stage]:
                with st.expander(f"{job['title']} @ {job['company']}", expanded=False):
                    st.text(f"📍 {job.get('location', 'N/A')} | 🗓 {job.get('applied_date', 'N/A')}")
                    st.text(f"🔁 Current Stage: {job.get('stage')}")

                    new_stage = st.selectbox("Move to stage", stages, index=stages.index(stage), key=f"stage_{job['id']}")
                    if new_stage != job["stage"]:
                        user_jobs_ref.document(job["id"]).update({"stage": new_stage})
                        st.success("✅ Stage updated")
                        st.experimental_rerun()

                    if st.checkbox("✏️ Edit this job", key=f"edit_{job['id']}"):
                        new_title = st.text_input("Job Title", value=job["title"], key=f"title_{job['id']}")
                        new_company = st.text_input("Company", value=job["company"], key=f"company_{job['id']}")
                        new_location = st.text_input("Location", value=job["location"], key=f"loc_{job['id']}")
                        new_date = st.date_input("Applied Date", value=datetime.date.fromisoformat(job["applied_date"]), key=f"date_{job['id']}")

                        if st.button("💾 Save Changes", key=f"save_{job['id']}"):
                            user_jobs_ref.document(job["id"]).update({
                                "title": new_title,
                                "company": new_company,
                                "location": new_location,
                                "applied_date": new_date.strftime("%Y-%m-%d")
                            })
                            st.success("✅ Job updated")
                            st.experimental_rerun()

                    if st.button("❌ Delete", key=f"delete_{job['id']}"):
                        user_jobs_ref.document(job["id"]).delete()
                        st.success("🗑️ Deleted")
                        st.experimental_rerun()

    st.markdown("---")
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
