"""
Tree Catalog page – shows all trees in a 4-column grid with thumbnails.
"""

import streamlit as st
from image_utils import show_tree_image
import header
from db_handler import execute_query

# --------------------------------------------------
# Page config + logos
# --------------------------------------------------
st.set_page_config(page_title="KRG Tree Index – Tree Catalog", layout="wide")
header.show()

st.title("🌲 Tree Catalog")
st.markdown("Browse all trees alphabetically. Use Ctrl-F to jump quickly.")

# --------------------------------------------------
# Pull the data, ordered by name
# --------------------------------------------------
rows = execute_query(
    """
    SELECT tree_name, scientific_name, image_path
    FROM tree_data
    ORDER BY tree_name;
    """,
    fetch=True,
)

# --------------------------------------------------
# Render in a 4-column grid
# --------------------------------------------------
cols_per_row = 4
row_cols = st.columns(cols_per_row)

for idx, r in enumerate(rows):
    col = row_cols[idx % cols_per_row]  # choose the column

    with col:
        st.subheader(r["tree_name"])
        show_tree_image(r["image_path"], width=140)
        st.markdown(f"<span style='font-style:italic;'>{r['scientific_name']}</span>",
                    unsafe_allow_html=True)
        st.markdown("---")

    # Every time we’ve filled 4 columns, start a new row
    if (idx + 1) % cols_per_row == 0:
        row_cols = st.columns(cols_per_row)
