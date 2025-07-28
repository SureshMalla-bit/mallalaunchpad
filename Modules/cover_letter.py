# modules/cover_letter.py

import streamlit as st
import google.generativeai as genai

def cover_letter_ai():
    """Generates a professional and tailored cover letter using AI."""
    st.title("📩 AI Cover Letter Generator")
    st.markdown("Provide your details and a job description to generate a compelling cover letter in seconds.")

    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-pro")
    except Exception:
        st.error("Failed to configure Gemini API. Please check your GEMINI_API_KEY in secrets.toml.")
        return

    with st.form("cover_letter_form"):
        st.subheader("Your Details")
        col1, col2 = st.columns(2)
        name = col1.text_input("Your Full Name")
        job_title = col2.text_input("Job Title You're Applying For")
        company = col1.text_input("Company Name")
        
        st.subheader("Content")
        resume_input = st.text_area("Paste key highlights from your resume (e.g., summary, key skills, achievements)")
        jd_input = st.text_area("Paste the full job description")

        submitted = st.form_submit_button("✨ Generate Cover Letter", use_container_width=True)

        if submitted:
            if not all([name, job_title, company, resume_input, jd_input]):
                st.warning("Please fill in all fields.")
            else:
                with st.spinner("Crafting your cover letter..."):
                    prompt = f"""
                    As an expert HR writer, generate a concise, professional, and enthusiastic cover letter.

                    DETAILS:
                    - Applicant Name: {name}
                    - Job Title: {job_title}
                    - Company: {company}
                    - Key Resume Points: {resume_input}
                    - Job Description: {jd_input}

                    INSTRUCTIONS:
                    1.  Structure it as a formal letter.
                    2.  Keep it under 250 words.
                    3.  Directly address how the applicant's skills (from resume points) match the job description.
                    4.  Maintain a confident and professional tone.
                    """
                    response = model.generate_content(prompt)
                    
                    st.subheader("Your Generated Cover Letter")
                    st.markdown(
                        f"""
                        <div style="background-color:#262730; padding:20px; border-radius:10px; border: 1px solid #636AF2;">
                        {response.text.replace("\n", "<br>")}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
