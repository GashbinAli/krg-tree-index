import streamlit as st
from db_handler import execute_query

# --------------------------------------------------
# This page is automatically shown at startup via st.switch_page() in app.py
# --------------------------------------------------

st.set_page_config(page_title="KRG Tree Index – Tree Search", layout="wide")

st.title("🔍 Tree Search")

st.markdown(
    """
Type a tree name below to view its details. The data comes directly from the **Neon** PostgreSQL
instance through the lightweight `db_handler` module, so any updates to the database show up here
instantly.
    """
)

# --------------------------------------------------
# Search box
# --------------------------------------------------
search_query = st.text_input("Search Tree by Name:").strip()

# --------------------------------------------------
# Helper to render a single tree record
# --------------------------------------------------

def render_tree(row: dict):
    """Pretty‑print a single tree row returned from the DB."""
    st.subheader(row["tree_name"].title())
    st.markdown(f"**Scientific Name:** {row['scientific_name']}")
    st.markdown(f"**Suitability for Erbil:** {row.get('suitability', 'N/A')}")
    st.markdown(f"**Water Need:** {row.get('water_need', 'N/A')}")
    st.markdown(f"**Shade Value:** {row.get('shade_public_use', 'N/A')}")
    st.markdown("---")

# --------------------------------------------------
# Query + display logic
# --------------------------------------------------
if search_query:
    query = """
        SELECT *
        FROM tree_data
        WHERE tree_name ILIKE %s
        ORDER BY tree_name
    """
    rows = execute_query(query, (f"%{search_query}%",), fetch=True)

    if rows:
        for row in rows:
            render_tree(row)
    else:
        st.warning("No tree found with that name.")
else:
    # Optional: show a quick alphabetical list when no search term is given
    st.info("Start typing to search, or browse the list below.")
    rows = execute_query(
        "SELECT tree_name, scientific_name FROM tree_data ORDER BY tree_name LIMIT 25;",
        fetch=True,
    )
    for row in rows:
        st.write(f"• **{row['tree_name']}** – *{row['scientific_name']}*")
