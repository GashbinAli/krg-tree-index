import streamlit as st

# --------------------------------------------------
# Main landing page
# --------------------------------------------------
st.set_page_config(page_title="KRG Tree Index", layout="wide")

st.title("🌳 KRG Tree Index")

st.markdown(
    """
Welcome to the **KRG Tree Index** — a data-driven guide to selecting the
right species for Kurdistan’s climate.

Use the buttons below *or* the Streamlit sidebar to navigate.
"""
)

# --------------------------------------------------
# Button-based navigation (uses file basenames only)
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Tree Search", use_container_width=True):
        st.switch_page("tree_search")      # <- file: pages/tree_search.py

with col2:
    if st.button("🌲 Tree Catalog", use_container_width=True):
        st.switch_page("tree_catalog")     # <- file: pages/tree_catalog.py

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.caption("© 2025 Hasar Organization | KRG Tree Index")
