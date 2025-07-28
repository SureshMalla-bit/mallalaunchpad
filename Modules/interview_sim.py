# modules/interview_sim.py (Chat UI)

import streamlit as st
import google.generativeai as genai

def interview_simulator():
    """A realistic AI-powered mock interview with a chat interface."""
    st.title("🎤 Interview AI Bot")
    st.markdown("Prepare for your next big opportunity. Select a persona and start the interview.")

    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-pro")
    except Exception as e:
        st.error("Failed to configure Gemini API. Please check your GEMINI_API_KEY in secrets.toml.")
        return

    # --- Interview Setup ---
    col1, col2 = st.columns(2)
    role = col1.selectbox("👔 Choose Interviewer Persona", ["HR Manager", "Technical Lead", "Product Manager", "Startup Founder"])
    job_title = col2.text_input("💼 Your Target Job Title", placeholder="e.g., Data Analyst")

    # --- Session State for Chat History ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- Start/Reset Button ---
    if st.button("🎬 Start New Interview"):
        st.session_state.messages = [] # Clear previous chat
        initial_prompt = f"You are a strict but fair {role} conducting a mock interview for the position of {job_title}. Ask me the first question now."
        with st.spinner("Interviewer is ready..."):
            response = model.generate_content(initial_prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.rerun()

    # --- Display Chat History ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- User Input ---
    if prompt := st.chat_input("Your answer..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI's next question
        with st.chat_message("assistant"):
            with st.spinner("..."):
                # Construct a simple history for the model
                chat_history = [f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages]
                prompt_for_next_q = f"This is a mock interview. Based on the history below, ask the next logical question. Keep it to one question at a time.\n\nHISTORY:\n{chat_history}"
                
                response = model.generate_content(prompt_for_next_q)
                ai_response = response.text
                st.markdown(ai_response)
        
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
