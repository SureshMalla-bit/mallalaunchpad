import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

def job_search_ui():
    st.title("🔍 AI-Powered Job Discovery")
    st.markdown("Find high-quality, relevant jobs based on your skills, location, and interests.")

    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-pro")
    except Exception:
        st.error("❌ Gemini API key missing. Please configure it in `.streamlit/secrets.toml`.")
        return

    with st.form("job_search_form"):
        col1, col2 = st.columns(2)
        role = col1.text_input("🎯 Job Title", placeholder="e.g., Frontend Developer")
        location = col2.text_input("🌍 Location", placeholder="e.g., Berlin, Remote")
        skills = st.text_area("🛠️ Key Skills", placeholder="e.g., React, JavaScript, UI/UX, Agile")
        submitted = st.form_submit_button("🔍 Search Jobs")

    if submitted and role:
        with st.spinner("🤖 Fetching jobs and analyzing matches..."):

            try:
                # ⏳ Simulate real job data (replace with real API or scraping)
                mock_jobs = [
                    {
                        "title": "React Frontend Engineer – Remote",
                        "company": "Codeverse Inc.",
                        "url": "https://example.com/job1",
                        "description": "Looking for someone with React, Redux, and UX experience. Agile team."
                    },
                    {
                        "title": "UI/UX Designer – Berlin Hybrid",
                        "company": "StudioZen",
                        "url": "https://example.com/job2",
                        "description": "Design clean user interfaces with Figma. Bonus for React knowledge."
                    },
                    {
                        "title": "Full Stack Developer – Remote (Europe)",
                        "company": "BrightStack",
                        "url": "https://example.com/job3",
                        "description": "Node.js, MongoDB, React. Must love agile and design-thinking."
                    }
                ]

                # Gemini prompt: Match jobs to skills
                skill_prompt = f"""
You are a career advisor. Given the candidate's desired job role: "{role}", location: "{location}", and skills: {skills},
analyze the following jobs and rank the top 3 matches with explanation:

{mock_jobs}
                """

                response = model.generate_content(skill_prompt).text
                st.success("✅ Top Matches Found")
                st.markdown(response)

                st.markdown("💡 *Real-time listings coming soon. Contact us to get early access.*")

            except Exception as e:
                st.error(f"⚠️ AI Matching Failed: {e}")
