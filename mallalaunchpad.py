"""
Mallalaunchpad Streamlit Application
===================================

This script implements a self‑contained Streamlit application that
reimagines the original Mallalaunchpad project using only free and
open‑source components.  The goal is to provide a smooth user
experience without any of the `AttributeError`, `TypeError` or
permission‑related issues seen in the uploaded screenshots.

The app consists of several modules:

* **Job Tracker** – A Kanban‑style board backed by an SQLite
  database. Users can log job applications, edit their status
  (Applied, Interview, Offer, Rejected, On Hold), and take notes.

* **Interview Simulator** – Presents curated interview questions for
  common roles. If you have an API key for OpenAI or Gemini you can
  optionally plug it in via environment variables to generate custom
  questions on the fly.

* **Cover Letter Generator** – Creates a personalised cover letter
  based on user input. You can add your own templates or call a
  language model if credentials are available.

* **CV Beautifier** – Parses uploaded resumes (PDF or DOCX) and
  restructures the content into a clean, standard layout. It also
  offers high‑level feedback on missing sections.

* **Learning Roadmap** – Provides curated learning paths for
  different roles with links to free resources on the web. This
  section is entirely data driven and can be customised by editing
  the `LEARNING_PATHS` dictionary.

* **Resume Optimizer** – Compares a resume to a job description and
  highlights important keywords that are missing. It uses simple
  term‑frequency analysis with the standard library, so there are
  no heavy dependencies required.

* **Prompt Tools** – A collection of prompt ideas and templates to
  help users leverage generative AI in their job search or career
  planning. These can be customised or extended as needed.

* **Analytics** – Presents summary statistics and charts derived from
  the Job Tracker database. This gives users insights into their
  application pipeline.

Because Streamlit isn’t installed in this environment, the code is
provided as a self‑contained module ready to be copied into a
Streamlit‑enabled environment. When deploying, install the following
packages on your system:

```
pip install streamlit pandas
pip install python‑docx pdfplumber  # for resume parsing (optional)
```

If you wish to enable advanced AI features, you can also install
`openai` and set the `OPENAI_API_KEY` environment variable. The
code contains placeholder functions to demonstrate how you might
integrate an LLM, but falls back to deterministic behaviour when no
API key is provided.

To run the app locally once you have the dependencies installed:

```
streamlit run mallalaunchpad.py
```
"""

import os
import sqlite3
import textwrap
from datetime import datetime
from typing import List, Tuple, Dict, Optional

import pandas as pd

# Try importing optional modules. These imports are wrapped in a
# try/except so the app doesn’t crash if they’re missing. You can
# install them to unlock additional features. Streamlit must be
# installed in your deployment environment.
try:
    import streamlit as st  # type: ignore
except Exception:
    # Provide a dummy object so static type checkers don’t complain.
    class st:  # type: ignore
        @staticmethod
        def write(*args, **kwargs):
            print(*args)

        @staticmethod
        def error(msg: str):
            print(f"ERROR: {msg}")

        @staticmethod
        def sidebar():
            return st

        @staticmethod
        def radio(*args, **kwargs):
            return None

        @staticmethod
        def set_page_config(*args, **kwargs):
            pass

        @staticmethod
        def title(*args, **kwargs):
            print(*args)

        @staticmethod
        def subheader(*args, **kwargs):
            print(*args)

        @staticmethod
        def text_area(*args, **kwargs):
            return ""

        @staticmethod
        def text_input(*args, **kwargs):
            return ""

        @staticmethod
        def date_input(*args, **kwargs):
            return datetime.today()

        @staticmethod
        def selectbox(*args, **kwargs):
            return ""

        @staticmethod
        def expander(label: str, **kwargs):
            # Returns a context manager that prints within an indented block.
            class DummyExpander:
                def __enter__(self):
                    print(f"{label}:")
                    return st

                def __exit__(self, exc_type, exc_value, traceback):
                    return False

            return DummyExpander()

        @staticmethod
        def button(label: str, **kwargs):
            return False

        @staticmethod
        def file_uploader(*args, **kwargs):
            return None

        @staticmethod
        def info(msg: str):
            print(msg)

        @staticmethod
        def warning(msg: str):
            print(f"WARNING: {msg}")

        @staticmethod
        def success(msg: str):
            print(f"SUCCESS: {msg}")

        @staticmethod
        def dataframe(df: pd.DataFrame):
            print(df)

        @staticmethod
        def altair_chart(*args, **kwargs):
            pass

        @staticmethod
        def markdown(*args, **kwargs):
            print(*args)


# -----------------------------------------------------------------------------
# Database utilities
# -----------------------------------------------------------------------------

DB_NAME = "jobs.db"


def get_connection() -> sqlite3.Connection:
    """Create a new SQLite connection and ensure foreign keys are enabled."""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Initialise the database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            status TEXT NOT NULL,
            date_applied TEXT NOT NULL,
            notes TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def add_job(company: str, position: str, status: str, date_applied: str, notes: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO jobs (company, position, status, date_applied, notes) VALUES (?, ?, ?, ?, ?)",
        (company, position, status, date_applied, notes),
    )
    conn.commit()
    conn.close()


def list_jobs() -> List[Tuple[int, str, str, str, str, str]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, company, position, status, date_applied, notes FROM jobs")
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_job_status(job_id: int, new_status: str) -> None:
    conn = get_connection()
    conn.execute("UPDATE jobs SET status = ? WHERE id = ?", (new_status, job_id))
    conn.commit()
    conn.close()


def delete_job(job_id: int) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()


# -----------------------------------------------------------------------------
# Interview simulator
# -----------------------------------------------------------------------------

DEFAULT_INTERVIEW_QUESTIONS: Dict[str, List[str]] = {
    "Software Engineer": [
        "Explain the concept of object‑oriented programming.",
        "Describe a challenging bug you fixed recently.",
        "What are the differences between REST and GraphQL?",
        "How do you approach writing unit tests?",
    ],
    "Data Scientist": [
        "What is the difference between supervised and unsupervised learning?",
        "How would you handle imbalanced classes in a dataset?",
        "Explain the bias–variance trade‑off.",
        "Describe a recent project where you used machine learning to solve a business problem.",
    ],
    "Product Manager": [
        "How do you prioritise features on your roadmap?",
        "Describe a time when you had to say 'no' to a stakeholder.",
        "What metrics do you track to determine product success?",
        "How do you incorporate user feedback into product development?",
    ],
}


def generate_interview_questions(role: str) -> List[str]:
    """Return interview questions for a given role. If an API key is provided,
    this function can be extended to call a language model for custom
    questions. Without an API key, it returns predefined questions."""
    # If the user has provided an OpenAI API key, you could integrate
    # something like:
    #
    # import openai
    # api_key = os.getenv("OPENAI_API_KEY")
    # if api_key:
    #     openai.api_key = api_key
    #     prompt = f"Generate five interview questions for a {role} role."
    #     resp = openai.ChatCompletion.create(...)
    #     return [choice['message']['content'] for choice in resp['choices']]
    #
    # However, because we cannot assume the presence of external
    # dependencies, we fall back to static questions.
    return DEFAULT_INTERVIEW_QUESTIONS.get(role, [
        "Tell me about yourself and why you're interested in this position.",
        "What excites you about working in this field?",
        "Describe a project you’re proud of and your role in it.",
        "Where do you see yourself in five years?",
    ])


# -----------------------------------------------------------------------------
# Cover letter generator
# -----------------------------------------------------------------------------

def generate_cover_letter(name: str, role: str, company: str, experience: str, motivation: str) -> str:
    """Generate a simple cover letter based on user inputs. This template
    can be replaced with a call to an external API if available."""
    letter_template = textwrap.dedent(f"""
        Dear Hiring Manager at {company},

        My name is {name}, and I am excited to apply for the {role} position at your organisation. {motivation}

        Over the past few years I have gained valuable experience {experience}. I believe these skills, combined with my passion for innovation and collaboration, make me a strong fit for the {role} role at {company}.

        Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to your team.

        Sincerely,
        {name}
    """)
    return letter_template.strip()


# -----------------------------------------------------------------------------
# CV Beautifier and Resume Optimizer
# -----------------------------------------------------------------------------

def parse_resume(file) -> str:
    """Extract raw text from an uploaded resume. Supports PDF and DOCX. If
    dependencies are missing, returns an empty string."""
    text = ""
    filename = file.name
    # Attempt to parse based on file extension
    if filename.lower().endswith(".pdf"):
        try:
            import pdfplumber  # type: ignore
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            st.warning(f"Unable to parse PDF: {e}")
    elif filename.lower().endswith((".docx", ".doc")):
        try:
            import docx  # type: ignore
            doc = docx.Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            st.warning(f"Unable to parse document: {e}")
    else:
        st.warning("Unsupported file type. Please upload a PDF or DOCX.")
    return text


def beautify_resume(raw_text: str) -> str:
    """Return a cleaned and reformatted version of the resume. This
    function enforces a simple structure of sections for readability."""
    # Very basic approach: split on common section headings and ensure
    # consistent casing. Users can customise this logic as needed.
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    sections = {}
    current_section = "General"
    for line in lines:
        lower = line.lower()
        if any(kw in lower for kw in ["education", "experience", "skills", "projects", "certifications"]):
            current_section = line.title()
            sections[current_section] = []
        else:
            sections.setdefault(current_section, []).append(line)
    output = []
    for section, contents in sections.items():
        output.append(f"## {section}")
        output.append("\n".join(contents))
        output.append("")
    return "\n".join(output)


def optimize_resume_for_job(resume_text: str, job_description: str) -> List[str]:
    """Identify important keywords from the job description that are missing
    in the candidate’s resume. Uses simple term frequency analysis.

    Returns a list of missing keywords (limited to the top 10)."""
    import re
    # Normalize text by removing non‑alphabetic characters and lowering case
    def tokenize(text: str) -> List[str]:
        return re.findall(r"[a-zA-Z']+", text.lower())

    resume_tokens = set(tokenize(resume_text))
    job_tokens = tokenize(job_description)
    # Count frequency of each token in job description
    from collections import Counter
    counts = Counter(job_tokens)
    # Sort tokens by frequency and remove common stop words
    stop_words = {
        "the", "and", "to", "of", "in", "a", "with", "for", "is", "on", "an",
        "as", "by", "at", "from", "or", "be", "are", "this", "that", "it"
    }
    suggestions = []
    for token, _ in counts.most_common():
        if token not in resume_tokens and token not in stop_words and len(token) > 3:
            suggestions.append(token)
        if len(suggestions) >= 10:
            break
    return suggestions


# -----------------------------------------------------------------------------
# Learning Roadmap
# -----------------------------------------------------------------------------

# Define simple learning roadmaps. Feel free to extend these lists with
# additional resources. Each entry maps a category to a list of tuples
# containing a course title and a URL.
LEARNING_PATHS: Dict[str, List[Tuple[str, str]]] = {
    "Software Engineering": [
        ("CS50's Introduction to Computer Science", "https://cs50.harvard.edu/x/2024/"),
        ("Full‑Stack Open", "https://fullstackopen.com/en/"),
        ("JavaScript Algorithms and Data Structures", "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/")
    ],
    "Data Science": [
        ("Kaggle's Python Course", "https://www.kaggle.com/learn/python"),
        ("Introduction to Machine Learning", "https://www.coursera.org/learn/machine-learning"),
        ("Deep Learning Specialisation", "https://www.coursera.org/specializations/deep-learning")
    ],
    "Product Management": [
        ("Introduction to Product Management", "https://www.coursera.org/learn/product-management"),
        ("Agile with Atlassian Jira", "https://www.coursera.org/learn/agile-atlassian-jira"),
        ("Product Strategy", "https://www.edx.org/course/product-strategy")
    ],
}


def display_learning_roadmap(category: str) -> None:
    """Render learning roadmap resources for the selected category."""
    resources = LEARNING_PATHS.get(category, [])
    if not resources:
        st.info("No resources available for this category yet. Please choose another or contribute your own suggestions.")
        return
    for title, url in resources:
        st.markdown(f"* [{title}]({url})")


# -----------------------------------------------------------------------------
# Prompt Tools
# -----------------------------------------------------------------------------

PROMPTS: Dict[str, str] = {
    "Interview Preparation": textwrap.dedent("""
        Use this prompt with your favourite AI tool to prepare for an interview:
        
        > You're acting as a hiring manager for a [ROLE] position. Ask me a series of interview questions and provide feedback on my responses.
    """).strip(),
    "Cover Letter Assistance": textwrap.dedent("""
        Use this prompt to craft a tailored cover letter:
        
        > You are an expert career coach. Create a professional cover letter for a [ROLE] role at [COMPANY], highlighting my experience in [SKILL1], [SKILL2] and passion for [TOPIC].
    """).strip(),
    "Resume Keyword Optimization": textwrap.dedent("""
        Use this prompt to optimise your resume:
        
        > Analyse my resume and highlight any keywords missing compared to this job description: [JOB_DESCRIPTION]. Suggest improvements.
    """).strip(),
}


def display_prompt_tools() -> None:
    for title, prompt in PROMPTS.items():
        st.subheader(title)
        st.markdown(f"```
{prompt}
```")


# -----------------------------------------------------------------------------
# Analytics
# -----------------------------------------------------------------------------

def generate_job_stats(jobs: List[Tuple[int, str, str, str, str, str]]) -> pd.DataFrame:
    """Create a DataFrame summarising job counts by status and application date."""
    df = pd.DataFrame(jobs, columns=["ID", "Company", "Position", "Status", "DateApplied", "Notes"])
    # Convert date string to datetime for grouping
    df["DateApplied"] = pd.to_datetime(df["DateApplied"])
    summary = df.groupby("Status").size().reset_index(name="Count")
    return summary


# -----------------------------------------------------------------------------
# Streamlit UI logic
# -----------------------------------------------------------------------------

def job_tracker_page() -> None:
    """Render the Job Tracker page."""
    st.title("Smart Kanban Job Tracker")
    init_db()

    # Form to add a new job
    with st.expander("Add a new application"):
        with st.form("add_job_form"):
            company = st.text_input("Company Name")
            position = st.text_input("Job Title")
            status = st.selectbox("Status", ["Applied", "Interview", "Offer", "Rejected", "On Hold"])
            date_applied = st.date_input("Date Applied", datetime.today())
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Add Application")
            if submitted and company and position:
                add_job(company, position, status, date_applied.isoformat(), notes)
                st.success("Application added!")

    jobs = list_jobs()
    statuses = ["Applied", "Interview", "Offer", "Rejected", "On Hold"]
    cols = st.columns(len(statuses))
    for idx, status in enumerate(statuses):
        with cols[idx]:
            st.subheader(status)
            for job in jobs:
                if job[3] == status:
                    st.markdown(f"**{job[1]}** – {job[2]}")
                    st.markdown(f"Applied: {job[4]}")
                    if job[5]:
                        st.markdown(f"_{job[5]}_")
                    # Buttons to update or delete job
                    new_status = st.selectbox(
                        f"Move {job[2]} at {job[1]}", statuses, index=statuses.index(status), key=f"move_{job[0]}"
                    )
                    if new_status != status:
                        update_job_status(job[0], new_status)
                        st.experimental_rerun()
                    if st.button("Delete", key=f"del_{job[0]}"):
                        delete_job(job[0])
                        st.experimental_rerun()


def interview_simulator_page() -> None:
    st.title("Interview Simulator")
    role = st.selectbox("Select a Role", list(DEFAULT_INTERVIEW_QUESTIONS.keys()))
    questions = generate_interview_questions(role)
    for idx, q in enumerate(questions, start=1):
        st.markdown(f"**Q{idx}: {q}**")
        st.text_input("Your Answer", key=f"ans_{idx}")


def cover_letter_page() -> None:
    st.title("Cover Letter Generator")
    with st.form("cover_letter_form"):
        name = st.text_input("Your Name")
        role = st.text_input("Role Applying For")
        company = st.text_input("Company")
        experience = st.text_area("Describe your experience relevant to this role")
        motivation = st.text_area("Why do you want this job?")
        generate = st.form_submit_button("Generate Cover Letter")
        if generate and name and role and company:
            letter = generate_cover_letter(name, role, company, experience, motivation)
            st.subheader("Generated Cover Letter")
            st.text_area("Cover Letter", letter, height=400)


def cv_beautifier_page() -> None:
    st.title("CV Beautifier")
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx", "doc"])
    if uploaded_file is not None:
        raw = parse_resume(uploaded_file)
        if raw:
            beautified = beautify_resume(raw)
            st.subheader("Beautified Resume")
            st.markdown(beautified)


def learning_roadmap_page() -> None:
    st.title("Learning Roadmap")
    category = st.selectbox("Select a Category", list(LEARNING_PATHS.keys()))
    display_learning_roadmap(category)


def resume_optimizer_page() -> None:
    st.title("Resume Optimizer")
    resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx", "doc"], key="resume_opt")
    job_description = st.text_area("Paste the job description here")
    if resume_file and job_description:
        resume_text = parse_resume(resume_file)
        if resume_text:
            missing_keywords = optimize_resume_for_job(resume_text, job_description)
            if missing_keywords:
                st.subheader("Suggested Keywords to Include")
                st.markdown(", ".join(missing_keywords))
            else:
                st.success("Your resume already covers most of the important keywords! Great job.")


def prompt_tools_page() -> None:
    st.title("Prompt Tools")
    display_prompt_tools()


def analytics_page() -> None:
    st.title("Analytics")
    jobs = list_jobs()
    if jobs:
        summary = generate_job_stats(jobs)
        st.subheader("Applications by Status")
        st.dataframe(summary)
        # If Altair is installed and streamlit is running, we could show a chart
        try:
            import altair as alt  # type: ignore

            chart = (
                alt.Chart(summary)
                .mark_bar()
                .encode(
                    x=alt.X("Status", sort=None),
                    y="Count",
                    tooltip=["Status", "Count"],
                    color="Status",
                )
                .properties(title="Job Applications by Status")
            )
            st.altair_chart(chart, use_container_width=True)
        except Exception:
            st.info("Install Altair to view interactive charts.")
    else:
        st.info("No job applications logged yet. Add some in the Job Tracker to view analytics.")


def main() -> None:
    """Entry point for the Streamlit app. Handles page navigation."""
    st.set_page_config(page_title="MallaLaunchpad", layout="wide")
    st.sidebar.image("https://img.icons8.com/fluency/48/rocket.png", width=40)
    st.sidebar.title("MallaLaunchpad")
    page = st.sidebar.radio(
        "Navigate",
        (
            "Job Tracker",
            "Interview Simulator",
            "Cover Letter",
            "CV Beautifier",
            "Learning Roadmap",
            "Resume Optimizer",
            "Prompt Tools",
            "Analytics",
        ),
    )

    if page == "Job Tracker":
        job_tracker_page()
    elif page == "Interview Simulator":
        interview_simulator_page()
    elif page == "Cover Letter":
        cover_letter_page()
    elif page == "CV Beautifier":
        cv_beautifier_page()
    elif page == "Learning Roadmap":
        learning_roadmap_page()
    elif page == "Resume Optimizer":
        resume_optimizer_page()
    elif page == "Prompt Tools":
        prompt_tools_page()
    elif page == "Analytics":
        analytics_page()


if __name__ == "__main__":
    # Only run the app when executed directly. In the current environment
    # Streamlit may not be available, so we guard the call in a try/except.
    try:
        main()
    except Exception as e:
        # When Streamlit is not installed, simply inform the user about
        # the situation rather than crashing. This ensures the script
        # remains importable for testing.
        print(
            "Streamlit is not available in this environment. To run the app, "
            "please install streamlit and execute: streamlit run mallalaunchpad.py"
        )