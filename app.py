import streamlit as st
from pathlib import Path

# ─── LOGO HEADER helper ─────────────────────────────────────────
_ASSETS = Path(__file__).parent / "assets"   # assets/hasar_logo.png, gov_logo.png

def show_header() -> None:
    """Display Hasar logo (left) and Govt logo (right)."""
    col_left, col_center, col_right = st.columns([0.15, 0.7, 0.15])
    with col_left:
        st.image(str(_ASSETS / "hasar_logo.png"), use_container_width=True)
    with col_right:
        st.image(str(_ASSETS / "gov_logo.png"),  use_container_width=True)
# ───────────────────────────────────────────────────────────────

st.set_page_config(page_title="KRG Tree Index", layout="wide")
show_header()                       # ← logos appear

st.title("🌳 KRG Tree Index")

st.markdown(
    """
Welcome to the **KRG Tree Index** — a data-driven guide for selecting the
right tree species for Kurdistan’s climate.

Use the buttons below *or* the sidebar to explore.
"""
)

col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 Tree Search", use_container_width=True):
        st.switch_page("pages/tree_search.py")
with col2:
    if st.button("🌲 Tree Catalog", use_container_width=True):
        st.switch_page("pages/tree_catalog.py")

st.markdown("---")
st.caption("© 2025 Hasar Organization | KRG Tree Index")
