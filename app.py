import streamlit as st

# --------------------------------------------------
# Basic page config
# --------------------------------------------------
st.set_page_config(page_title="KRG Tree Index", layout="wide")

st.title("🌳 KRG Tree Index")

st.markdown(
    """
Welcome to the **KRG Tree Index** — a data-driven guide for selecting the right
trees for Kurdistan’s climate.

Use the buttons below *or* the sidebar to explore the app.
"""
)

# --------------------------------------------------
# Button-based navigation
# (NOTE: st.switch_page needs the relative path WITHOUT .py)
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Tree Search", use_container_width=True):
        st.switch_page("pages/tree_search")      # ← exact file path (no .py)

with col2:
    if st.button("🌲 Tree Catalog", use_container_width=True):
        st.switch_page("pages/tree_catalog")     # ← exact file path (no .py)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.caption("© 2025 Hasar Organization | KRG Tree Index")
