import streamlit as st

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(page_title="KRG Tree Index", layout="wide")

# --------------------------------------------------
# Welcome message
# --------------------------------------------------
st.title("🌳 KRG Tree Index")

st.markdown(
    """
Welcome to the **KRG Tree Index** — a data‑driven guide to selecting the
right trees for Kurdistan’s climate.

Use the buttons below (or Streamlit’s sidebar) to explore the application.
    """,
)

# --------------------------------------------------
# Simple button‑based navigation
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Tree Search", use_container_width=True):
        st.switch_page("pages/Tree Search")

with col2:
    if st.button("🌲 Tree Catalog", use_container_width=True):
        st.switch_page("pages/Tree Catalog")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.caption("© 2025 Hasar Organization | KRG Tree Index")
