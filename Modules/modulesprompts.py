# modules/prompts.py

import streamlit as st

def prompt_toolkit():
    """A curated library of expert prompts for job seekers."""
    st.title("🧠 AI Prompt Toolkit")
    st.markdown("A collection of expert-crafted prompts to use with any AI assistant (like Gemini or ChatGPT) to accelerate your job search.")
    
    prompt_library = {
        "🔍 Job Search": [
            "Act as a career coach. Based on my skills in [List 3-5 key skills], what are 5 niche job titles I should be searching for that I might not have considered?",
            "Find me 5 remote-first companies in the [industry, e.g., FinTech] sector that have recently received funding and are likely hiring for [role, e.g., marketing] roles."
        ],
        "📝 Resume Writing": [
            "My resume bullet point is: 'Responsible for managing social media'. Rewrite this to be results-oriented, assuming I increased engagement by 15%.",
            "Generate 3 powerful, professional summary statements for a resume. My target role is [Job Role] and I have [Number] years of experience in [field/industry]."
        ],
        "✉️ Cover Letters": [
            "Write a 3-paragraph cover letter for the [Job Title] role at [Company Name]. Use a confident but not arrogant tone. My key achievement relevant to this role is [describe a key achievement].",
            "Analyze this job description and tell me the top 3 skills the hiring manager is looking for. Job Description: [Paste job description]"
        ],
        "🧠 Interviews": [
            "Generate 5 challenging behavioral interview questions for a [Job Role] position, focusing on the theme of 'adaptability' and 'problem-solving'.",
            "I was asked, 'Tell me about a time you failed.' I want to talk about [briefly describe the situation]. Frame this story using the STAR (Situation, Task, Action, Result) method to sound professional and competent."
        ]
    }

    for category, prompts in prompt_library.items():
        with st.expander(f"**{category}**"):
            for p in prompts:
                st.markdown(f"**Prompt:**")
                st.code(p, language="markdown")
                if st.button("📋 Copy", key=p):
                    st.code(f"Copied to clipboard!") # In a real app, this would use a clipboard library
                    # pyperclip.copy(p) # Requires pyperclip library
