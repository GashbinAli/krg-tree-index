import streamlit as st

# --------------------------------------------------
# Basic page configuration (sidebar collapsed by default)
# --------------------------------------------------
st.set_page_config(
    page_title="KRG Tree Index",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# Main page
# --------------------------------------------------
st.title("🌳 KRG Tree Index")

st.markdown(
    """
Welcome to the **KRG Tree Index**.

Choose one of the sections below to explore the application.
    """
)

# --------------------------------------------------
# Simple 2‑column navigation (no sidebar)
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Tree Search", use_container_width=True):
        # "Tree Search" is the *page name* inside the pages folder
        st.switch_page("Tree Search")

with col2:
    if st.button("🌲 Tree Catalog", use_container_width=True):
        # "Tree Catalog" is the *page name* inside the pages folder
        st.switch_page("Tree Catalog")

# --------------------------------------------------
# Optional footer or instructions
# --------------------------------------------------
st.markdown("---")
st.caption("© 2025 Hasar Organization | KRG Tree Index")
