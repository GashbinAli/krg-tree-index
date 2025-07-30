import os
import streamlit as st
from db_handler import execute_query   # ← your helper lives in the project root

# --------------------------------------------------
# Pull DB URL from secrets in production (optional)
# --------------------------------------------------
if "connections" in st.secrets and "postgres" in st.secrets["connections"]:
    os.environ["DATABASE_URL"] = st.secrets["connections"]["postgres"]["url"]

# --------------------------------------------------
# Page config & header
# --------------------------------------------------
st.set_page_config(page_title="KRG Tree Index – Tree Search", layout="wide")

st.title("🔍 Tree Search")

st.markdown(
    """
Search the live **KRG Tree Index** database hosted on Neon.
Type a *common* or *scientific* name & press **Enter**.
"""
)

# --------------------------------------------------
# Search box
# --------------------------------------------------
search_term = st.text_input("Tree name (partial is OK):").strip()

# --------------------------------------------------
# Helper to format one row
# --------------------------------------------------
def show_tree(row: dict) -> None:
    st.subheader(row["tree_name"].title())
    st.markdown(f"**Scientific Name:** *{row['scientific_name']}*")
    st.markdown(f"**Suitability:** {row.get('suitability', 'N/A')}")
    st.markdown(
        f"**Water Efficiency (1-5):** {row.get('water_efficiency', 'N/A')}"
    )
    st.markdown(
        f"**Shade / Public Use (1-5):** {row.get('shade_public_use', 'N/A')}"
    )
    st.markdown(f"**Rating:** {row.get('rating', 'N/A')}")
    st.markdown("---")

# --------------------------------------------------
# DB query & display
# --------------------------------------------------
if search_term:
    sql = """
        SELECT *
        FROM tree_data
        WHERE tree_name ILIKE %s
           OR scientific_name ILIKE %s
        ORDER BY tree_name;
    """
    rows = execute_query(sql, (f"%{search_term}%", f"%{search_term}%"), fetch=True)

    if rows:
        for r in rows:
            show_tree(r)
    else:
        st.warning("No match found.")
else:
    st.info("Start typing to search. Here’s a quick preview ↓")
    preview = execute_query(
        "SELECT tree_name, scientific_name FROM tree_data ORDER BY tree_name LIMIT 25;",
        fetch=True,
    )
    for r in preview:
        st.write(f"• **{r['tree_name']}** — *{r['scientific_name']}*")
