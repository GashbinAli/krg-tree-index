import streamlit as st

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(page_title="KRG Tree Index", layout="wide")

st.title("🌳 KRG Tree Index")

st.markdown(
    """
Welcome to the **KRG Tree Index** — a data-driven guide to selecting the
best species for Kurdistan’s climate.

Use the buttons below *or* the left-hand sidebar to explore the app.
"""
)

# --------------------------------------------------
# Navigation buttons
# (NOTE: use the exact file basename, no spaces, no ".py")
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Tree Search", use_container_width=True):
        st.switch_page("pages/tree_search")    # ✅ exact path to pages/tree_search.py

with col2:
    if st.button("🌲 Tree Catalog", use_container_width=True):
        st.switch_page("pages/tree_catalog")   # ✅ exact path to pages/tree_catalog.py

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.caption("© 2025 Hasar Organization | KRG Tree Index")
