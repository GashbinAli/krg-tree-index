# image_utils.py
from pathlib import Path
import streamlit as st
from PIL import UnidentifiedImageError

REPO_ROOT = Path(__file__).parent          # krg-tree-index/

def show_tree_image(rel_path: str, *, width: int = 250) -> None:
    """
    Display an image from a relative path (assets/…).
    If the file is missing or unreadable, show a placeholder.
    """
    if not rel_path:
        st.caption("*(no image)*")
        return

    path = REPO_ROOT / rel_path
    try:
        st.image(path, width=width)
    except (FileNotFoundError, UnidentifiedImageError):
        st.caption(f"*(image not found: {rel_path})*")

