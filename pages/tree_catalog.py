"""
Tree Catalog page – alphabetical list with thumbnails.
"""

import streamlit as st
from image_utils import show_tree_image
import header
from db_handler import execute_query

# ---------------------- page config + logos --------------------------
st.set_page_config(page_title="KRG Tree Index – Tree Catalog", layout="wide")
header.show()

st.title("🌲 Tree Catalog")
st.markdown("Browse all trees alphabetically. Use Ctrl-F to jump quickly.")

rows = execute_query(
    "SELECT tree_name, scientific_name, image_path FROM tree_data ORDER BY tree_name;",
    fetch=True,
)

for r in rows:
    st.subheader(r["tree_name"])
    show_tree_image(r["image_path"], width=120)   # thumbnail
    st.markdown(f"*{r['scientific_name']}*")
    st.markdown("---")
