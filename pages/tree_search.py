"""
Tree Search page
----------------
• Searches the Neon `tree_data` table by common OR scientific name.
• Shows matches in a left column.
• Clicking a row opens a full profile (all score columns) on the right.
"""

import os
import streamlit as st

# ---------------------------------------------------------------------
# Robust import for the DB helper
# ---------------------------------------------------------------------
try:
    from db_handler import execute_query           # preferred file name
except ModuleNotFoundError:                         # fallback if helper is db-handler.py
    import importlib.util, sys
    from pathlib import Path

    helper_path = Path(__file__).resolve().parent.parent / "db-handler.py"
    if helper_path.exists():
        spec = importlib.util.spec_from_file_location("db_handler", helper_path)
        db_handler = importlib.util.module_from_spec(spec)        # type: ignore
        sys.modules["db_handler"] = db_handler                    # register
        spec.loader.exec_module(db_handler)                       # type: ignore[arg-type]
        execute_query = db_handler.execute_query                  # type: ignore[attr-defined]
    else:
        raise

# ---------------------------------------------------------------------
# Optional: override DB URL from Streamlit secrets (for cloud deploys)
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
Type a *common* or *scientific* name, press **Enter**, then click a result
to view the tree’s full profile (all score criteria).
"""
)

# ---------------------------------------------------------------------
# Session state – remember which tree is selected
# ---------------------------------------------------------------------
if "selected_tree_id" not in st.session_state:
    st.session_state.selected_tree_id = None

# ---------------------------------------------------------------------
# Search input
# ---------------------------------------------------------------------
search_term = st.text_input("Search:").strip()

# ---------------------------------------------------------------------
# Column layout – wider right panel when a tree is selected
# ---------------------------------------------------------------------
if st.session_state.selected_tree_id:
    col_list, col_detail = st.columns([1, 2])
else:
    col_list, col_detail = st.columns([1, 0.05])  # skinny placeholder

# ---------------------------------------------------------------------
# DETAIL PANEL (right column)
# ---------------------------------------------------------------------
with col_detail:
    if st.session_state.selected_tree_id:
        tree = execute_query(
            "SELECT * FROM tree_data WHERE id = %s;",
            (st.session_state.selected_tree_id,),
            fetch=True,
        )[0]  # exactly one row

        st.header(tree["tree_name"])
        st.markdown(f"**Scientific name:** *{tree['scientific_name']}*")
        st.markdown("---")

        # Every score column -> human-readable label
        score_labels = {
            "climate_adaptation":       "Climate adaptation",
            "water_efficiency":         "Water efficiency",
            "biodiversity_support":     "Biodiversity support",
            "community_acceptance":     "Community acceptance",
            "aesthetic_cultural_fit":   "Aesthetic & cultural fit",
            "shade_public_use":         "Shade / public use",
            "cost_of_planting":         "Cost of planting",
            "maintenance_needs":        "Maintenance needs",
            "lifespan_durability":      "Lifespan & durability",
            "total_score":              "TOTAL score",
        }

        for col, label in score_labels.items():
            if col in tree and tree[col] is not None:
                st.markdown(f"**{label}:** {tree[col]}")

        # Extra descriptive fields
        st.markdown("---")
        st.markdown(f"**Suitability:** {tree.get('suitability', 'N/A')}")
        st.markdown(f"**Rating:** {tree.get('rating', 'N/A')}")
        st.markdown(f"**Information:** {tree.get('information', '')}")
        st.markdown(f"**Challenges:** {tree.get('challenges', '')}")
        st.markdown("---")

        # Back button
        if st.button("🔙 Back to results"):
            st.session_state.selected_tree_id = None
            st.rerun()

# ---------------------------------------------------------------------
# LIST PANEL (left column)
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
                    f"{r['tree_name']} — {r['scientific_name']}",
                    key=f"tree_{r['id']}",
                    use_container_width=True,
                ):
                    st.session_state.selected_tree_id = r["id"]
                    st.rerun()
        else:
            st.info("No match found.")
    else:
        st.info("Start typing to search, or click a random sample below.")
        preview = execute_query(
            """
            SELECT id, tree_name, scientific_name
            FROM tree_data
            ORDER BY RANDOM()
            LIMIT 25;
            """,
            fetch=True,
        )
        for r in preview:
            if st.button(
                f"{r['tree_name']} — {r['scientific_name']}",
                key=f"tree_preview_{r['id']}",
                use_container_width=True,
            ):
                st.session_state.selected_tree_id = r["id"]
                st.rerun()
