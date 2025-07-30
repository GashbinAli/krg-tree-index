import streamlit as st
from pathlib import Path

# ──────────────────────────────────────────────────────────────
# 1)  HEADER helper (copy this into every page file)
# ──────────────────────────────────────────────────────────────
_ASSETS = Path(__file__).parent / "assets"   # assets/hasar_logo.png, gov_logo.png

def show_header():
    col_left, col_center, col_right = st.columns([0.15, 0.7, 0.15])
    with col_left:
        st.image(_ASSETS / "hasar_logo.png", use_column_width="auto")
    with col_right:
        st.image(_ASSETS / "gov_logo.png",  use_column_width="auto")

# ──────────────────────────────────────────────────────────────
# 2)  Page config + HEADER
# ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="KRG Tree Index", layout="wide")
show_header()          # ← logos appear

st.title("🌳 KRG Tree Index")

st.markdown(
    """
Welcome to the **KRG Tree Index** — a data-driven guide for selecting the
best species for Kurdistan’s climate.

Use the buttons below *or* the left sidebar to explore.
"""
)

# navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 Tree Search", use_container_width=True):
        st.switch_page("pages/tree_search.py")
with col2:
    if st.button("🌲 Tree Catalog", use_container_width=True):
        st.switch_page("pages/tree_catalog.py")

st.markdown("---")
st.caption("© 2025 Hasar Organization | KRG Tree Index")
