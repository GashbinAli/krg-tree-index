"""
Tree Catalog page
-----------------
Shows every tree in the database alphabetically.
"""

import streamlit as st
import header                       # logos
from db_handler import execute_query

# ------------------------ Page config + logos ------------------------
st.set_page_config(page_title="KRG Tree Index – Tree Catalog", layout="wide")
header.show()                       # display the two logos

st.title("🌲 Tree Catalog")
st.markdown(
    "Browse the full list of trees. Use your browser’s search (Ctrl-F) to jump quickly."
)

# Fetch and display
rows = execute_query(
    "SELECT tree_name, scientific_name FROM tree_data ORDER BY tree_name;",
    fetch=True,
)

for r in rows:
    st.subheader(r["tree_name"])
    st.markdown(f"*{r['scientific_name']}*")
    st.markdown("---")
