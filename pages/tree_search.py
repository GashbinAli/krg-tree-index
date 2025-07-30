"""
Tree Search page – searches Neon DB and shows a detail panel.

Requires:
  • db_handler.execute_query
  • A table called `tree_data` with at least:
      id, tree_name, scientific_name, total_score,  …(other columns)
"""

import os
import streamlit as st
from db_handler import execute_query

# ----- optional: use secrets in prod -----
if "connections" in st.secrets and "postgres" in st.secrets["connections"]:
    os.environ["DATABASE_URL"] = st.secrets["connections"]["postgres"]["url"]

# ----- page config -----
st.set_page_config(page_title="KRG Tree Index – Tree Search", layout="wide")
st.title("🔍 Tree Search")

# Keep a place to store which tree the user clicked
if "selected_tree_id" not in st.session_state:
    st.session_state.selected_tree_id = None

# ----- search box -----
search_term = st.text_input("Type a common or scientific name:")

# -----------------------------------------------------------------
# If a tree has been chosen, show its full profile on the right
# -----------------------------------------------------------------
if st.session_state.selected_tree_id:
    col_list, col_detail = st.columns([1, 2])
else:
    col_list, col_detail = st.columns([1, 0.01])   # prevent layout jump

with col_detail:
    if st.session_state.selected_tree_id:
        tree = execute_query(
            "SELECT * FROM tree_data WHERE id = %s;",
            (st.session_state.selected_tree_id,),
            fetch=True,
        )[0]

        # ========== Tree profile ==========
        st.header(tree["tree_name"])
        st.markdown(f"**Scientific:** *{tree['scientific_name']}*")
        st.markdown(f"**Total Score:** {tree.get('total_score', 'N/A')}")
        st.markdown(f"**Suitability:** {tree.get('suitability', 'N/A')}")
        st.markdown(f"**Water Efficiency:** {tree.get('water_efficiency', 'N/A')}")
        st.markdown(f"**Shade / Public Use:** {tree.get('shade_public_use', 'N/A')}")
        st.markdown(f"**Biodiversity Support:** {tree.get('biodiversity_support', 'N/A')}")
        st.markdown(f"**Information:** {tree.get('information', '')}")
        st.markdown("---")
        st.button("🔙 Back to results", on_click=lambda: st.session_state.update(selected_tree_id=None))
        st.stop()   # stop rendering remainder of page

# -----------------------------------------------------------------
# Show list of matches in the left column
# -----------------------------------------------------------------
with col_list:
    if search_term:
        rows = execute_query(
            """
            SELECT id, tree_name, scientific_name
            FROM tree_data
            WHERE tree_name ILIKE %s OR scientific_name ILIKE %s
            ORDER BY tree_name;
            """,
            (f"%{search_term}%", f"%{search_term}%"),
            fetch=True,
        )
        if rows:
            st.subheader(f"{len(rows)} result(s):")
            for r in rows:
                if st.button(f"{r['tree_name']}  –  {r['scientific_name']}",
                             key=f"tree_{r['id']}"):
                    st.session_state.selected_tree_id = r["id"]
                    st.experimental_rerun()
        else:
            st.info("No match.")
    else:
        st.info("Start typing to search…")
