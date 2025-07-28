# modules/roadmap.py

import streamlit as st
import google.generativeai as genai

def career_roadmap():
    """Generates a 6-month learning roadmap for a given job role using AI."""
    st.title("🌱 Career Roadmap Generator")
    st.markdown("Enter a job role to get a detailed, 6-month learning and project plan powered by AI.")
    
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-pro")
    except Exception:
        st.error("API key not configured. Please check your .streamlit/secrets.toml file.")
        return

    role = st.text_input("🎯 Enter Your Target Job Role", placeholder="e.g., Cloud Engineer, UI/UX Designer, Data Scientist")

    if st.button("📈 Generate My Roadmap", use_container_width=True) and role:
        with st.spinner(f"Crafting your 6-month roadmap for a {role}... This may take a moment."):
            prompt = f"""
            You are a senior career mentor. Create a detailed 6-month skill development roadmap for someone aiming to become a proficient {role}.

            The output must be in markdown format. For each month, provide the following:
            - **Theme:** A clear focus for the month (e.g., "Month 1: Foundational Python & Data Structures").
            - **Key Topics:** A bulleted list of specific concepts or technologies to learn.
            - **Learning Resources:** Suggest 1-2 specific and high-quality online courses (from platforms like Coursera, Udemy, or freeCodeCamp) or official documentation.
            - **Project:** Define a tangible mini-project that applies the skills learned during that month. The project should be practical and build upon the previous month's work.
            """
            try:
                response = model.generate_content(prompt)
                st.subheader(f"📘 Your Roadmap to Becoming a {role}")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred while generating the roadmap: {e}")

