import streamlit as st

def cv_beautifier():
    """Formats raw resume data into a beautiful, downloadable HTML CV."""
    st.title("🖌️ CV Beautifier")
    st.markdown("Transform your raw resume text into a clean, modern HTML CV you can copy or print.")

    with st.form("beautifier_form"):
        col1, col2 = st.columns(2)
        full_name = col1.text_input("Full Name")
        contact = col2.text_input("Contact Info (Email / Phone / LinkedIn)")
        
        summary = st.text_area("🧾 Professional Summary")
        experience = st.text_area("💼 Work Experience (use bullet points)")
        education = st.text_area("🎓 Education")
        skills = st.text_area("🛠️ Key Skills (comma-separated)")

        submitted = st.form_submit_button("✨ Beautify My CV", use_container_width=True)

    if submitted:
        if not full_name or not contact:
            st.warning("Please fill in at least your name and contact.")
            return

        exp_html = "<ul>" + "".join(
            f"<li>{line.strip()}</li>" for line in experience.split('\n') if line.strip()
        ) + "</ul>"

        html_template = f"""
        <div style="font-family:sans-serif; border:1px solid #333; padding:2rem; border-radius:10px; background-color:#1E1E1E;">
            <div style="text-align:center; border-bottom: 2px solid #636AF2; padding-bottom: 1rem;">
                <h1 style="color:#FAFAFA; margin:0;">{full_name}</h1>
                <p style="margin:5px; color:#A9A9A9;">{contact}</p>
            </div>
            <h3 style="color:#636AF2; margin-top:1.5rem;">Professional Summary</h3>
            <p style="color:#FAFAFA;">{summary}</p>
            <h3 style="color:#636AF2; margin-top:1.5rem;">Work Experience</h3>
            <div style="color:#FAFAFA;">{exp_html}</div>
            <h3 style="color:#636AF2; margin-top:1.5rem;">Education</h3>
            <p style="color:#FAFAFA;">{education}</p>
            <h3 style="color:#636AF2; margin-top:1.5rem;">Key Skills</h3>
            <p style="color:#FAFAFA;">{skills}</p>
        </div>
        """

        st.subheader("🧾 Your Beautified CV")
        st.markdown(html_template, unsafe_allow_html=True)

        # Show HTML code for copying
        st.code(html_template, language="html")

        # Download button
        st.download_button("💾 Download CV as HTML", data=html_template, file_name="beautified_cv.html", mime="text/html")
