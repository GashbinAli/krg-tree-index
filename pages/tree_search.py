# pages/Tree Search.py
import os
import streamlit as st
from db_handler import execute_query   # uses the helper you pasted

# --------------------------------------------------
# (Optional) pull DB URL from Streamlit secrets
# --------------------------------------------------
if "connections" in st.secrets and "postgres" in st.secrets["connections"]:
    os.environ["DATABASE_URL"] = st.secrets["connections"]["postgres"]["url"]

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(page_title="KRG Tree Index – Tree Search", layout="wide")
st.title("🔍 Tree Search")

st.markdown(
    """
Search the live **KRG Tree Index** database hosted on Neon.  
Type a common or scientific name (even a partial word) and press **Enter**.
"""
)

# --------------------------------------------------
# Search box
# --------------------------------------------------
search_query = st.text_input("Tree name (common or scientific):").strip()

# --------------------------------------------------
# Helper to render one row
# --------------------------------------------------
def render_tree(row: dict) -> None:
    st.subheader(row["tree_name"].title())
    st.markdown(f"**Scientific Name:** *{row['scientific_name']}*")
    st.markdown(f"**Suitability:** {row.get('suitability', 'N/A')}")
    st.markdown(f"**Water Efficiency (1-5):** {row.get('water_efficiency', 'N/A')}")
    st.markdown(f"**Shade / Public Use (1-5):** {row.get('shade_public_use', 'N/A')}")
    st.markdown(f"**Rating:** {row.get('rating', 'N/A')}")
    st.markdown(f"**Info:** {row.get('information', '')}")
    st.markdown("---")

# --------------------------------------------------
# Query + display logic
# --------------------------------------------------
if search_query:
    sql = """
        SELECT *
        FROM tree_data
        WHERE tree_name       ILIKE %s
           OR scientific_name ILIKE %s
        ORDER BY tree_name
    """
    rows = execute_query(sql, (f"%{search_query}%", f"%{search_query}%"), fetch=True)

    if rows:
        for row in rows:
            render_tree(row)
    else:
        st.warning("Nothing matched that search term.")
else:
    st.info("Start typing to search, or browse the first 25 trees below.")
    preview = execute_query(
        "SELECT tree_name, scientific_name FROM tree_data ORDER BY tree_name LIMIT 25;",
        fetch=True,
    )
    for row in preview:
        st.write(f"• **{row['tree_name']}** – *{row['scientific_name']}*")
