import streamlit as st

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(page_title="KRG Tree Index", layout="wide")

st.title("🌳 KRG Tree Index")

st.markdown(
    """
Welcome to the **KRG Tree Index** — a data-driven guide for selecting the
best tree species for Kurdistan’s climate.

Use the buttons below *or* the left-hand sidebar to explore.
"""
)

# --------------------------------------------------
# Navigation buttons
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Tree Search", use_container_width=True):
        st.switch_page("pages/tree_search.py")     # 🟢 exact file path

with col2:
    if st.button("🌲 Tree Catalog", use_container_width=True):
        st.switch_page("pages/tree_catalog.py")    # 🟢 exact file path

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.caption("© 2025 Hasar Organization | KRG Tree Index")
