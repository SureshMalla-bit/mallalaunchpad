# modules/cv_beautifier.py

import streamlit as st

def cv_beautifier():
    """Formats raw resume text into a beautiful HTML template."""
    st.title("🖌️ CV Beautifier")
    st.markdown("Input your raw resume text and get a professionally formatted HTML version that you can copy or print.")
    
    with st.form("beautifier_form"):
        st.subheader("Enter Your Details")
        col1, col2 = st.columns(2)
        full_name = col1.text_input("Full Name")
        contact = col2.text_input("Contact (Email / Phone / LinkedIn)")
        
        summary = st.text_area("Professional Summary")
        experience = st.text_area("Work Experience (use bullet points, one per line)")
        education = st.text_area("Education")
        skills = st.text_area("Skills (comma-separated)")
        
        submitted = st.form_submit_button("✨ Beautify My CV", use_container_width=True)

        if submitted:
            # Simple conversion of bullet points to HTML list items
            exp_html = "<ul>" + "".join([f"<li>{line}</li>" for line in experience.split('\n') if line.strip()]) + "</ul>"
            
            # Themed HTML Template
            html_template = f"""
            <div style="font-family:sans-serif; border:1px solid #333; padding:2rem; border-radius:10px; background-color:#1E1E1E;">
                <div style="text-align:center; border-bottom: 2px solid #636AF2; padding-bottom: 1rem;">
                    <h1 style="color:#FAFAFA; margin:0;">{full_name}</h1>
                    <p style="margin:5px; color:#A9A9A9;">{contact}</p>
                </div>
                <h3 style="color:#636AF2; margin-top:1.5rem; border-bottom:1px solid #333; padding-bottom:5px;">Professional Summary</h3>
                <p style="color:#FAFAFA;">{summary}</p>
                <h3 style="color:#636AF2; margin-top:1.5rem; border-bottom:1px solid #333; padding-bottom:5px;">Work Experience</h3>
                <div style="color:#FAFAFA;">{exp_html}</div>
                <h3 style="color:#636AF2; margin-top:1.5rem; border-bottom:1px solid #333; padding-bottom:5px;">Education</h3>
                <p style="color:#FAFAFA;">{education}</p>
                <h3 style="color:#636AF2; margin-top:1.5rem; border-bottom:1px solid #333; padding-bottom:5px;">Key Skills</h3>
                <p style="color:#FAFAFA;">{skills}</p>
            </div>
            """
            st.subheader("Your Beautified CV")
            st.markdown(html_template, unsafe_allow_html=True)
