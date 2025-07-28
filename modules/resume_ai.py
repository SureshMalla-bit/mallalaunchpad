# modules/resume_ai.py

import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF

def resume_ai_suite(uid, db, storage):
    st.title("📤 Resume Optimizer + Gemini AI")
    st.markdown("Upload your resume and paste a job description. Let our AI act as your personal career coach and ATS scanner.")

    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-pro")
    except Exception:
        st.error("❌ Gemini API key missing or misconfigured.")
        return

    col1, col2 = st.columns(2)
    with col1:
        resume_file = st.file_uploader("📎 Upload Resume (PDF/TXT)", type=["pdf", "txt"])
    with col2:
        job_desc = st.text_area("🧾 Paste Job Description", height=220)

    resume_text = ""

    if resume_file:
        st.markdown("✅ **Resume Uploaded:** Previewing content...")
        try:
            if resume_file.type == "application/pdf":
                doc = fitz.open(stream=resume_file.read(), filetype="pdf")
                for i, page in enumerate(doc):
                    resume_text += page.get_text()
                    if i > 2: break  # Only preview first 3 pages
            else:
                resume_text = resume_file.read().decode("utf-8")
            st.code(resume_text[:1000] + "...", language="markdown")
        except Exception as e:
            st.error(f"❌ Error reading resume file: {e}")
            return

    if st.button("🔬 Analyze My Resume", use_container_width=True):
        if not resume_text or not job_desc:
            st.warning("⚠️ Please upload a resume and job description.")
            return

        with st.spinner("Analyzing your resume with AI..."):
            prompt = f"""
            Act as a senior career coach and ATS expert.
            Analyze the resume below against the job description and respond in Markdown format with 3 structured sections:

            ### 1. First Impressions & Formatting
            - Layout, clarity, length, font, structure

            ### 2. Keyword Match & ATS Score
            - Score out of 10
            - List important missing keywords

            ### 3. Action Verbs & Resume Bullet Enhancements
            - Suggest 3–5 better bullet points to improve impact

            --- Resume ---
            {resume_text}

            --- Job Description ---
            {job_desc}
            """

            try:
                response = model.generate_content(prompt)
                st.success("✅ AI Review Complete")

                # Display using tabs
                tabs = st.tabs(["🖋 Formatting", "🔑 Keyword Match", "💥 Bullet Point Upgrade"])
                content = response.text

                for i, section in enumerate(["First Impressions", "Keyword", "Bullet"]):
                    with tabs[i]:
                        section_text = content.split("###")[i + 1] if f"### {section}" in content else content
                        st.markdown("### " + section_text.strip())

            except Exception as e:
                st.error(f"⚠️ AI failed to analyze resume: {e}")
