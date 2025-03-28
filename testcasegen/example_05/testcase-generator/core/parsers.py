import fitz
import streamlit as st


@st.cache_data(show_spinner=False)
def parse_pdf(uploaded_file):
    """带加密验证的PDF解析器"""
    try:
        doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
        if doc.is_encrypted and not doc.authenticate(st.secrets.get("PDF_PASSWORD", "")):
            raise PermissionError("需要文档密码")

        return {
            "text": "\n".join([page.get_text() for page in doc]),
            "page_count": len(doc)
        }
    except fitz.FileDataError as e:
        st.error(f"文档解析失败: {str(e)}")
        return None