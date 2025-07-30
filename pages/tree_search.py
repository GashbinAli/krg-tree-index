"""
Tree Search page
----------------
• Searches the Neon PostgreSQL `tree_data` table.
• Shows matches in a left column.
• Click a tree to view its full profile (all columns) in the right column.
"""

import os
import streamlit as st

# ---------------------------------------------------------------------
# Robust import for the DB helper
# ---------------------------------------------------------------------
try:
    from db_handler import execute_query  # preferred
except ModuleNotFoundError:
    # Fallback if helper is still named db-handler.py
    import importlib.util
    from pathlib import Path
    import sys

    helper_path = Path(__file__).resolve().parent.parent / "db-handler.py"
    if helper_path.exists():
        spec = importlib.util.spec_from_file_location("db_handler", helper_path)
        db_handler = importlib.util.module_from_spec(spec)  # type: ignore
        sys.modules["db_handler"] = db_handler
        spec.loader.exec_module(db_handler)  # type: ignore[arg-type]
        execute_query = db_handler.execute_query  # type: ignore[attr-defined]
    else:
        raise

# ---------------------------------------------------------------------
# Optional: override DB URL from Streamlit secrets (prod deploys)
# ---------------------------------------------------------------------
if "connections" in st.secrets and "postgres" in st.secrets["connections"]:
    os.environ["DATABASE_URL"] = st.secrets["connections"]["postgres"]["url"]

# ---------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------
st.set_page_config(page_title="KRG Tree Index – Tree Search", layout="wide")
st.title("🔍 Tree Search")

st.markdown(
    """
Type a *common* or *scientific* name below.  
Click on a result to see all its data (including total score) on the right.
"""
)

# ---------------------------------------------------------------------
# Session state to remember the selected tree ID
# ---------------------------------------------------------------------
if "selected_tree_id" not in st.session_state:
    st.session_state.selected_tree_id = None

# ---------------------------------------------------------------------
# Search box
# ---------------------------------------------------------------------
search_term = st.text_input("Search for a tree:").strip()

# ---------------------------------------------------------------------
# Decide column widths: if a tree is selected, show wide detail panel
# ---------------------------------------------------------------------
if st.session_state.selected_tree_id:
    col_list, col_detail = st.columns([1, 2])
else:
    col_list, col_detail = st.columns([1, 0.05])  # tiny placeholder

# ---------------------------------------------------------------------
# Right column = detailed profile
# ---------------------------------------------------------------------
with col_detail:
    if st.session_state.selected_tree_id:
        tree = execute_query(
            "SELECT * FROM tree_data WHERE id = %s;",
            (st.session_state.selected_tree_id,),
            fetch=True,
        )[0]  # we know there's exactly one

        # --- Full profile ---
        st.header(tree["tree_name"])
        st.markdown(f"**Scientific name:** *{tree['scientific_name']}*")
        st.markdown(f"**Total score:** {tree.get('total_score', 'N/A')}")
        st.markdown(f"**Suitability:** {tree.get('suitability', 'N/A')}")
        st.markdown(f"**Water efficiency:** {tree.get('water_efficiency', 'N/A')}")
        st.markdown(f"**Shade / public use:** {tree.get('shade_public_use', 'N/A')}")
        st.markdown(f"**Biodiversity support:** {tree.get('biodiversity_support', 'N/A')}")
        st.markdown(f"**Rating:** {tree.get('rating', 'N/A')}")
        st.markdown(f"**Information:** {tree.get('information', '')}")
        st.markdown(f"**Challenges:** {tree.get('challenges', '')}")
        st.markdown("---")

        # Back button resets session state then reloads page
        if st.button("🔙 Back to results"):
            st.session_state.selected_tree_id = None
            st.rerun()

# ---------------------------------------------------------------------
# Left column = list of matches
# ---------------------------------------------------------------------
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
            st.subheader(f"{len(rows)} result(s)")
            for r in rows:
                if st.button(
                    f"{r['tree_name']}  –  {r['scientific_name']}",
                    key=f"tree_{r['id']}",
                    use_container_width=True,
                ):
                    st.session_state.selected_tree_id = r["id"]
                    st.rerun()   # <-- new name replaces experimental_rerun
        else:
            st.info("No match found.")
    else:
        st.info("Start typing to search. Here are 25 random trees:")
        preview = execute_query(
            "SELECT id, tree_name, scientific_name FROM tree_data ORDER BY random() LIMIT 25;",
            fetch=True,
        )
        for r in preview:
            if st.button(
                f"{r['tree_name']}  –  {r['scientific_name']}",
                key=f"tree_preview_{r['id']}",
                use_container_width=True,
            ):
                st.session_state.selected_tree_id = r["id"]
                st.rerun()
