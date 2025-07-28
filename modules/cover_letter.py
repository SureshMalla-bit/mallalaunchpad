import streamlit as st
import google.generativeai as genai

def generate_cover_letter(name, job_title, company, resume_input, jd_input):
    prompt = f"""
    As an expert HR writer, generate a concise, professional, and enthusiastic cover letter.

    DETAILS:
    - Applicant Name: {name}
    - Job Title: {job_title}
    - Company: {company}
    - Key Resume Points: {resume_input}
    - Job Description: {jd_input}

    INSTRUCTIONS:
    1. Structure it as a formal letter.
    2. Keep it under 250 words.
    3. Match applicant’s strengths to the job description.
    4. Use a confident and enthusiastic tone.
    """
    model = genai.GenerativeModel("gemini-pro")
    return model.generate_content(prompt).text

def cover_letter_ai():
    """Generates a professional and tailored cover letter using Gemini AI."""
    st.title("📩 AI Cover Letter Generator")
    st.markdown("Provide your details and the job description to get a tailored cover letter in seconds.")

    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    except Exception:
        st.error("❌ Gemini API Key not found. Please add it to `.streamlit/secrets.toml`.")
        return

    with st.form("cover_letter_form"):
        st.subheader("🔎 Your Info")
        col1, col2 = st.columns(2)
        name = col1.text_input("Full Name")
        job_title = col2.text_input("Job Title You're Applying For")
        company = col1.text_input("Company Name")

        st.subheader("📎 Content")
        resume_input = st.text_area("Key Resume Highlights")
        jd_input = st.text_area("Job Description")

        submitted = st.form_submit_button("✨ Generate Cover Letter", use_container_width=True)

    if submitted:
        if not all([name, job_title, company, resume_input, jd_input]):
            st.warning("⚠️ Please fill in all fields.")
        else:
            with st.spinner("Crafting your perfect letter..."):
                try:
                    letter = generate_cover_letter(name, job_title, company, resume_input, jd_input)
                    st.success("✅ Cover letter generated!")
                except Exception as e:
                    st.error("Something went wrong while generating the cover letter.")
                    st.stop()

            st.subheader("📝 Your Cover Letter")
            st.markdown(
                f"""<div style="background-color:#f0f2f6; padding:20px; border-radius:10px;">
                {letter.replace('\n', '<br>')}
                </div>""",
                unsafe_allow_html=True
            )

            st.code(letter, language='markdown')
            st.download_button("📄 Download as Text", data=letter, file_name="cover_letter.txt")
