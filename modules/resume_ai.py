# modules/resume_ai.py

import streamlit as st
import google.generativeai as genai
import fitz # PyMuPDF

def resume_ai_suite(uid, db, storage):
    """Provides AI-powered feedback on a user's resume against a job description."""
    st.title("📤 Resume + AI Review")
    st.markdown("Upload your resume and paste a job description to get an AI-driven analysis and improvement suggestions.")

    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-pro")
    except Exception:
        st.error("Failed to configure Gemini API. Please check your GEMINI_API_KEY in secrets.toml.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Your Resume")
        resume_file = st.file_uploader("Upload your Resume (PDF or TXT)", type=["pdf", "txt"])

    with col2:
        st.subheader("🎯 Target Job")
        job_desc = st.text_area("Paste the Job Description Here", height=250)

    if st.button("🔬 Analyze My Resume", use_container_width=True):
        if not resume_file or not job_desc:
            st.warning("Please upload your resume and provide a job description.")
        else:
            with st.spinner("AI is analyzing your resume..."):
                # Read text from uploaded resume
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
                You are an expert career coach. Analyze the following resume and job description.

                RESUME TEXT:
                {resume_text}

                JOB DESCRIPTION:
                {job_desc}

                Provide a detailed analysis covering these three areas:
                1.  **First Impressions & Formatting:** Give feedback on the overall clarity and structure.
                2.  **Keyword & ATS Match:** Score the resume out of 10 for its match with the job description. List key missing keywords.
                3.  **Impact & Action Verbs:** Suggest 3-5 specific improvements to bullet points to make them more results-oriented.
                
                Present the output in clean, readable markdown.
                """
                
                try:
                    response = model.generate_content(prompt)
                    st.subheader("🧠 AI Analysis Complete")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"An error occurred during AI analysis: {e}")

