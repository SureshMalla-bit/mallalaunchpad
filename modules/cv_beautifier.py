import streamlit as st

try:
    import fitz  # PyMuPDF
except ImportError:
    from PyMuPDF import fitz

def extract_text_from_pdf(uploaded_file):
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text
    except Exception as e:
        st.error(f"Failed to extract text: {e}")
        return None

def format_cv_text(text):
    # You can add better formatting logic here if needed
    formatted = text.replace("\n", "<br>")
    return f"<div style='font-family: Inter, sans-serif; font-size: 14px; line-height: 1.6'>{formatted}</div>"

def beautify_cv_ui():
    st.subheader("🧾 CV Beautifier")
    st.markdown("Upload your resume in PDF format and see it beautifully rendered below.")

    uploaded_file = st.file_uploader("Upload your CV (PDF only)", type=["pdf"])

    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        if text:
            st.success("✅ CV text extracted successfully.")
            with st.container():
                st.markdown("---")
                st.markdown("### 🖋️ Formatted Resume Preview:")
                st.markdown(format_cv_text(text), unsafe_allow_html=True)
