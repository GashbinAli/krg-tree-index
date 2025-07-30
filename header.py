# header.py
import streamlit as st
from pathlib import Path
from PIL import UnidentifiedImageError

_ASSETS = Path(__file__).parent / "assets"

def _safe_image(path: Path, **kwargs):
    """Show image if valid; otherwise show a placeholder text."""
    try:
        st.image(path, **kwargs)
    except (FileNotFoundError, UnidentifiedImageError):
        st.write(f"*(missing image {path.name})*")

def show():
    """Display Hasar logo left & Government logo right on every page."""
    col_left, col_center, col_right = st.columns([0.15, 0.7, 0.15])

    with col_left:
        _safe_image(_ASSETS / "hasar_logo.png", width=120)      # fixed width

    with col_right:
        _safe_image(_ASSETS / "gov_logo.png",  width=120)
