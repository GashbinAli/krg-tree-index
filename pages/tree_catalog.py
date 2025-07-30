import streamlit as st
from db_handler import execute_query

st.set_page_config(page_title="KRG Tree Index – Tree Catalog", layout="wide")

st.title("🌲 Tree Catalog")

st.markdown(
    "Browse the full list of trees currently in the database. Scroll or use the "
    "sidebar search (Ctrl‑F) in your browser for quick navigation.",
)

rows = execute_query("SELECT tree_name, scientific_name FROM tree_data ORDER BY tree_name;", fetch=True)

for row in rows:
    st.subheader(row["tree_name"])
    st.markdown(f"*{row['scientific_name']}*")
    st.markdown("---")
