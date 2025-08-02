# header.py
"""
Shows Hasar logo (left) and Government logo (right) on every page.
Also pulls Git-LFS objects once per container session so images work.
"""

import streamlit as st
from pathlib import Path
from PIL import UnidentifiedImageError

# --- pull Git-LFS blobs once ----------------------------------------
import lfs_bootstrap
lfs_bootstrap.ensure_lfs_pulled()     # << NEW: runs on every page

# --------------------------------------------------------------------
_ASSETS = Path(__file__).parent / "assets"

def _safe_image(path: Path, *, width: int | None = None):
    try:
        st.image(path, width=width)
    except (FileNotFoundError, UnidentifiedImageError):
        st.write(f"*(missing {path.name})*")

def show():
    """Render logos."""
    col_left, col_center, col_right = st.columns([0.15, 0.7, 0.15])
    with col_left:
        _safe_image(_ASSETS / "hasar_logo.png", width=120)
    with col_right:
        _safe_image(_ASSETS / "gov_logo.png", width=120)
