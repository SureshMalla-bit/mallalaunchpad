import streamlit as st
import google.generativeai as genai

def prompt_toolkit():
    st.title("🧠 AI Prompt Studio")
    st.markdown("Use expert-crafted prompts to supercharge your resume, job search, and interview prep. You can also customize them and run live with Gemini.")

    # Configure Gemini
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-pro")
    except Exception:
        st.error("❌ Gemini API key missing.")
        return

    prompt_categories = {
        "🔍 Job Search": [
            {
                "title": "Find jobs using my interests and skills",
                "template": "Find me remote jobs in [industry or role] that align with my skills: [list your skills] and my experience: [brief summary]."
            },
            {
                "title": "Generate cold outreach message for recruiter",
                "template": "Write a professional LinkedIn message to a recruiter for the role of [job title] at [company name]. Highlight my background in [field]."
            },
        ],
        "📝 Resume Writing": [
            {
                "title": "Resume summary generator",
                "template": "Write a resume summary for a [job title] with [years] years of experience in [field/industry]. Emphasize achievements and soft skills."
            },
            {
                "title": "Convert job duties into strong bullet points",
                "template": "Convert this plain job duty into an impactful resume bullet with metrics: [your current job duty]."
            },
        ],
        "✉️ Cover Letters": [
            {
                "title": "Write a personalized cover letter",
                "template": "Write a cover letter for the role of [job title] at [company]. Highlight my experience in [field] and interest in [specific company value or mission]."
            }
        ],
        "🧠 Interview Prep": [
            {
                "title": "Behavioral interview answer",
                "template": "Answer this behavioral interview question using the STAR format: [question]. Use my experience: [your experience summary]."
            }
        ]
    }

    query = st.text_input("🔍 Search Prompts", placeholder="e.g. resume bullet, recruiter message, STAR format")
    query_lower = query.lower()

    for category, prompts in prompt_categories.items():
        filtered_prompts = [
            p for p in prompts
            if query_lower in p["title"].lower() or query_lower in p["template"].lower()
        ] if query else prompts

        if filtered_prompts:
            with st.expander(category, expanded=True):
                for prompt in filtered_prompts:
                    st.subheader(prompt["title"])
                    base_prompt = prompt["template"]

                    st.caption("🧩 Fill in the blanks:")
                    placeholders = [part.strip("[]") for part in base_prompt.split() if part.startswith("[")]
                    filled = base_prompt
                    for ph in placeholders:
                        user_input = st.text_input(f"{ph}", key=f"{prompt['title']}_{ph}")
                        filled = filled.replace(f"[{ph}]", user_input or f"[{ph}]")

                    st.code(filled, language="markdown")

                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.button("📋 Copy Prompt", key=f"copy_{prompt['title']}", on_click=lambda text=filled: st.session_state.update({"copied": text}))
                    with col2:
                        if st.button("🤖 Run with Gemini", key=f"gemini_{prompt['title']}"):
                            with st.spinner("Gemini is crafting your output..."):
                                try:
                                    response = model.generate_content(filled)
                                    st.success("✅ Gemini Response")
                                    st.markdown(response.text)
                                except Exception as e:
                                    st.error(f"⚠️ Error: {e}")
