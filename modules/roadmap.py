import streamlit as st
import google.generativeai as genai

def career_roadmap():
    """Generates a 6-month learning roadmap for a given job role using Gemini AI."""
    st.title("🗺️ AI-Powered Career Roadmap")
    st.markdown("Enter your desired job title and get a customized, month-wise skill roadmap with projects and resources.")

    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-pro")
    except Exception:
        st.error("❌ Gemini API Key not configured in `.streamlit/secrets.toml`.")
        return

    role = st.text_input("🎯 Target Job Role", placeholder="e.g., Cloud Engineer, Data Analyst, Product Designer")

    if st.button("🚀 Generate 6-Month Roadmap", use_container_width=True) and role:
        with st.spinner(f"Crafting a powerful roadmap for {role}..."):
            prompt = f"""
            You are a senior career mentor and expert planner.

            Create a detailed 6-month career roadmap for becoming a successful {role}. The roadmap must include:

            - **Month Theme** (e.g., "Foundations", "Tools & Frameworks")
            - **Key Topics** (bulleted list)
            - **Recommended Resources** (2–3 specific online courses, docs, or books)
            - **Mini Project** (one per month that applies the learnings)

            Format the entire response in clear **markdown**.
            Keep it practical, modern, and achievable for someone learning independently.
            """
            try:
                result = model.generate_content(prompt).text
                st.success(f"✅ Your 6-Month Roadmap for {role} is ready!")
                st.download_button("💾 Download Roadmap (.md)", data=result, file_name=f"{role}_roadmap.md", mime="text/markdown")
                st.markdown(result)
            except Exception as e:
                st.error("❌ Failed to generate roadmap. Please try again.")
