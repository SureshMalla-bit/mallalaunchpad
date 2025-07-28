# modules/ats_cv_optimizer.py

import streamlit as st
import google.generativeai as genai
import fitz # PyMuPDF

def ats_cv_optimizer():
    """Analyzes a resume against a job description for ATS keyword optimization."""
    st.title("📈 ATS Score Optimizer")
    st.markdown("Get specific keyword suggestions to improve your resume's score against an Applicant Tracking System (ATS).")

    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-pro")
    except Exception:
        st.error("Failed to configure Gemini API. Please check your GEMINI_API_KEY in secrets.toml.")
        return

    col1, col2 = st.columns(2)
    with col1:
        resume_file = st.file_uploader("Upload your Resume (PDF or TXT)", type=["pdf", "txt"])
    with col2:
        job_desc = st.text_area("Paste the Job Description Here", height=280)

    if st.button("🚀 Get ATS Suggestions", use_container_width=True):
        if not resume_file or not job_desc:
            st.warning("Please upload your resume and paste a job description.")
        else:
            with st.spinner("Analyzing for ATS keywords..."):
                # Read resume text
                resume_text = ""
                if resume_file.type == "application/pdf":
                    try:
                        doc = fitz.open(stream=resume_file.read(), filetype="pdf")
                        for page in doc:
                            resume_text += page.get_text()
                    except Exception as e:
                        st.error(f"Error reading PDF: {e}")
                        return
                else:
                    resume_text = resume_file.read().decode("utf-8")

                # Generate AI feedback
                prompt = f"""
                You are an expert ATS optimization tool. Analyze the resume and job description below.

                RESUME:
                {resume_text}

                JOB DESCRIPTION:
                {job_desc}

                INSTRUCTIONS:
                1.  Identify the top 10-15 most important keywords from the job description.
                2.  Compare the list against the resume.
                3.  List the critical keywords that are **missing** from the resume.
                4.  Provide 3 specific examples of how to naturally integrate these missing keywords into the resume's bullet points.
                
                Present the output in clean, readable markdown.
                """
                try:
                    response = model.generate_content(prompt)
                    st.subheader("✅ Optimization Suggestions")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"An error occurred during AI analysis: {e}")
