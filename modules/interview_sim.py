import streamlit as st
import google.generativeai as genai

def run_interview_simulator():
    """A realistic AI-powered mock interview with a Gemini chat interface."""
    st.title("🎤 AI Mock Interview Simulator")
    st.markdown("Prepare for your dream role with AI-driven mock interviews.")

    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-pro")
    except Exception as e:
        st.error("❌ Failed to connect with Gemini API. Please check your secrets.toml.")
        return

    # --- Setup Interview Parameters ---
    col1, col2 = st.columns(2)
    role = col1.selectbox("👔 Interviewer Persona", ["HR Manager", "Tech Lead", "Startup Founder", "Product Manager"])
    job_title = col2.text_input("💼 Job Title You're Applying For", placeholder="e.g., Backend Engineer")

    # --- Chat History Setup ---
    if "interview_history" not in st.session_state:
        st.session_state.interview_history = []

    # --- Start New Interview ---
    if st.button("🎬 Start New Interview"):
        st.session_state.interview_history = []
        intro_prompt = f"You are a {role} conducting a professional mock interview for a {job_title} role. Begin the interview with your first question."
        with st.spinner("AI Interviewer is preparing..."):
            response = model.generate_content(intro_prompt)
            st.session_state.interview_history.append({"role": "assistant", "content": response.text})
        st.rerun()

    # --- Display Chat ---
    for msg in st.session_state.interview_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- User Reply ---
    if prompt := st.chat_input("Type your answer..."):
        st.session_state.interview_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chat_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.interview_history])
                follow_up_prompt = f"This is a mock interview. Based on the conversation so far, ask the next best interview question.\n\n{chat_context}"
                try:
                    reply = model.generate_content(follow_up_prompt)
                    response_text = reply.text
                except Exception:
                    response_text = "Something went wrong with Gemini. Please try again."

                st.markdown(response_text)

        st.session_state.interview_history.append({"role": "assistant", "content": response_text})
