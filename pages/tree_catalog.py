"""
Tree Catalog page – shows all trees in a 4-column grid with clickable thumbnails.
Clicking any image jumps to the Tree Search page and opens the selected tree’s
full details.
"""

import streamlit as st
from image_utils import show_tree_image
import header
from db_handler import execute_query

# ────────────────────────────────────────────────────────────────────────────────
# Page configuration + top-bar logos
# ────────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="KRG Tree Index – Tree Catalog", layout="wide")
header.show()

st.title("🌲 Tree Catalog")
st.markdown(
    "Browse all trees alphabetically. Use **Ctrl + F** (or ⌘ + F) to jump quickly."
)

# ────────────────────────────────────────────────────────────────────────────────
# Fetch data (include the primary key so we can pass it to the detail page)
# ────────────────────────────────────────────────────────────────────────────────
rows = execute_query(
    """
    SELECT id, tree_name, scientific_name, image_path
    FROM tree_data
    ORDER BY tree_name;
    """,
    fetch=True,
)

# ────────────────────────────────────────────────────────────────────────────────
# 4-column grid layout
# ────────────────────────────────────────────────────────────────────────────────
COLS_PER_ROW = 4
row_cols = st.columns(COLS_PER_ROW)

for idx, r in enumerate(rows):
    # choose the column (0-based) within the current row
    col = row_cols[idx % COLS_PER_ROW]

    with col:
        # ── title ───────────────────────────────────────────────────────────────
        st.subheader(r["tree_name"])

        # ── invisible button over the image ────────────────────────────────────
        clicked = st.button(
            key=f"img_{r['id']}",
            label="",                     # empty label keeps the button unseen
            help="Click for full details",
        )
        show_tree_image(r["image_path"], width=140)

        # when clicked → store id in session and switch pages
        if clicked:
            st.session_state.selected_tree_id = r["id"]
            st.switch_page("pages/tree_search.py")   # adjust path if file name differs

        # ── scientific name + divider ──────────────────────────────────────────
        st.markdown(
            f"<span style='font-style:italic;'>{r['scientific_name']}</span>",
            unsafe_allow_html=True,
        )
        st.markdown("---")

    # ── after filling 4 columns, start a new row ───────────────────────────────
    if (idx + 1) % COLS_PER_ROW == 0:
        row_cols = st.columns(COLS_PER_ROW)
