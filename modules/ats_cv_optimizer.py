import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF

def ats_cv_optimizer():
    """Analyzes a resume against a job description for ATS keyword optimization."""
    st.title("📈 ATS Score Optimizer")
    st.markdown("Improve your resume's score against an Applicant Tracking System (ATS) by identifying missing keywords.")

    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-pro")
    except Exception:
        st.error("❌ Gemini API Key missing. Please set GEMINI_API_KEY in `.streamlit/secrets.toml`.")
        return

    col1, col2 = st.columns(2)
    with col1:
        resume_file = st.file_uploader("📄 Upload your Resume (PDF or TXT)", type=["pdf", "txt"])
    with col2:
        job_desc = st.text_area("📝 Paste the Job Description", height=280)

    if st.button("🚀 Analyze Resume for ATS", use_container_width=True):
        if not resume_file or not job_desc:
            st.warning("Please upload your resume and enter a job description.")
            return

        with st.spinner("🔍 Running AI-powered analysis..."):
            resume_text = ""

            # Handle resume parsing
            if resume_file.type == "application/pdf":
                try:
                    doc = fitz.open(stream=resume_file.read(), filetype="pdf")
                    for page in doc:
                        resume_text += page.get_text()
                except Exception as e:
                    st.error(f"❌ PDF Parsing Failed: {e}")
                    return
            else:
                try:
                    resume_text = resume_file.read().decode("utf-8")
                except Exception as e:
                    st.error(f"❌ Text File Reading Failed: {e}")
                    return

            prompt = f"""
            You are an expert in resume optimization and ATS systems.

            Compare the RESUME with the JOB DESCRIPTION.

            RESUME:
            {resume_text}

            JOB DESCRIPTION:
            {job_desc}

            TASK:
            - Extract 10–15 important keywords from the job description.
            - Identify which ones are **missing** from the resume.
            - Suggest how to naturally integrate 3–5 of those keywords with real bullet-point examples.

            Format your output in **markdown**, with clear headings.
            """

            try:
                response = model.generate_content(prompt)
                st.subheader("✅ ATS Optimization Suggestions")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"❌ Gemini analysis failed: {e}")
