# --------------------------------------------------
# Pull Git-LFS images the first time the app starts
# --------------------------------------------------
import lfs_bootstrap
lfs_bootstrap.ensure_lfs_pulled()   # downloads PNG/JPG blobs if needed

# --------------------------------------------------
# Normal Streamlit imports
# --------------------------------------------------
import streamlit as st
import header                        # shows Hasar + Government logos

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(page_title="KRG Tree Index", layout="wide")
header.show()                        # logos (left + right)

# --------------------------------------------------
# Landing content
# --------------------------------------------------
st.title("🌳 KRG Tree Index")

st.markdown(
    """
Welcome to the **KRG Tree Index** — a data-driven guide to selecting the
right tree species for Kurdistan’s climate.

Choose a section below or use the left sidebar.
"""
)

# --------------------------------------------------
# Navigation buttons
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Tree Search", use_container_width=True):
        st.switch_page("pages/tree_search.py")    # search page

with col2:
    if st.button("🌲 Tree Catalog", use_container_width=True):
        st.switch_page("pages/tree_catalog.py")   # catalog page

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.caption("© 2025 Hasar Organization | KRG Tree Index")
