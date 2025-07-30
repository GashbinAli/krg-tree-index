# header.py
import streamlit as st
from pathlib import Path

_ASSETS = Path(__file__).parent / "assets"   # points to /assets folder

def show():
    """Display Hasar logo (left) and Government logo (right)."""
    col_left, col_center, col_right = st.columns([0.15, 0.7, 0.15])

    with col_left:
        st.image(_ASSETS / "hasar_logo.png", use_column_width="auto")

    with col_right:
        st.image(_ASSETS / "gov_logo.png", use_column_width="auto")

