"""
pages/tree_search.py
--------------------
• Shows Hasar (left) + Government (right) logos on top of page.
• Searches Neon `tree_data` by common/scientific name.
• Lists unique tree names on left; click -> full profile on right.
• Full profile order: Rating, all numeric scores table, Information,
  Suitability, Challenges.
"""

import os
import sys
import importlib.util
from pathlib import Path

import pandas as pd
import streamlit as st

# ───────────────────────────────────────────────────────────────
# 1) Logo header helper (self-contained, no extra file needed)
# ───────────────────────────────────────────────────────────────
_ASSETS = Path(__file__).resolve().parent.parent / "assets"  # .. / assets

def show_header() -> None:
    """Display Hasar logo (left) and KRG government logo (right)."""
    col_left, col_center, col_right = st.columns([0.15, 0.7, 0.15])
    with col_left:
        st.image(str(_ASSETS / "hasar_logo.png"), use_container_width=True)
    with col_right:
        st.image(str(_ASSETS / "gov_logo.png"), use_container_width=True)
# ───────────────────────────────────────────────────────────────

# ── 2) Page config + header ────────────────────────────────────
st.set_page_config(page_title="KRG Tree Index – Tree Search", layout="wide")
show_header()

st.title("🔍 Tree Search")
st.markdown(
    "Type a *common* or *scientific* name. Click a result to view its profile."
)

# ── 3) Robust import for db_handler --------------------------------
try:
    from db_handler import execute_query
except ModuleNotFoundError:
    helper_path = Path(__file__).resolve().parent.parent / "db-handler.py"
    if not helper_path.exists():
        st.error("db_handler.py (or db-handler.py) not found!")
        st.stop()

    spec = importlib.util.spec_from_file_location("db_handler", helper_path)
    db_handler = importlib.util.module_from_spec(spec)  # type: ignore
    sys.modules["db_handler"] = db_handler
    spec.loader.exec_module(db_handler)                 # type: ignore[arg-type]
    execute_query = db_handler.execute_query            # type: ignore[attr-defined]

# ── 4) Optional DB URL override from Streamlit secrets -----------
if "connections" in st.secrets and "postgres" in st.secrets["connections"]:
    os.environ["DATABASE_URL"] = st.secrets["connections"]["postgres"]["url"]

# ── 5) UI state & search box --------------------------------------
if "selected_tree_id" not in st.session_state:
    st.session_state.selected_tree_id = None

search_term = st.text_input("Search:").strip()

# Choose column widths
cols = [1, 2] if st.session_state.selected_tree_id else [1, 0.05]
col_list, col_detail = st.columns(cols)

# ── 6) DETAIL PANEL (right) ---------------------------------------
with col_detail:
    if st.session_state.selected_tree_id:
        tree = execute_query(
            "SELECT * FROM tree_data WHERE id = %s;",
            (st.session_state.selected_tree_id,),
            fetch=True,
        )[0]

        # Rating
        st.header(tree["tree_name"])
        st.markdown(f"### Rating: {tree.get('rating', 'N/A')}")

        # Numeric score table
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
        rows = [
            {"Criterion": label, "Score": tree[col]}
            for col, label in score_labels.items()
            if col in tree and tree[col] is not None
        ]
        if rows:
            df = pd.DataFrame(rows).set_index("Criterion")
            styled = (
                df.style
                .set_properties(**{"color": "black", "font-weight": "bold"})
                .set_table_styles(
                    [{"selector": "th",
                      "props": [("color", "black"), ("font-weight", "bold")]}]
                )
            )
            st.table(styled)

        # Descriptive paragraphs
        st.markdown("---")
        st.markdown(f"**Information**\n\n{tree.get('information', 'N/A')}")
        st.markdown(f"**Suitability**\n\n{tree.get('suitability', 'N/A')}")
        st.markdown(f"**Challenges**\n\n{tree.get('challenges', 'N/A')}")
        st.markdown("---")

        if st.button("🔙 Back to results"):
            st.session_state.selected_tree_id = None
            st.rerun()

# ── 7) LIST PANEL (left) ------------------------------------------
with col_list:
    if search_term:
        results = execute_query(
            """
            SELECT DISTINCT ON (tree_name)
                   id, tree_name, scientific_name
            FROM tree_data
            WHERE tree_name ILIKE %s OR scientific_name ILIKE %s
            ORDER BY tree_name, id;
            """,
            (f"%{search_term}%", f"%{search_term}%"),
            fetch=True,
        )
        if results:
            st.subheader(f"{len(results)} result(s)")
            for r in results:
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
            SELECT DISTINCT ON (tree_name)
                   id, tree_name, scientific_name
            FROM tree_data
            ORDER BY tree_name
            LIMIT 25;
            """,
            fetch=True,
        )
        for r in preview:
            if st.button(
                f"{r['tree_name']} — {r['scientific_name']}",
                key=f"preview_{r['id']}",
                use_container_width=True,
            ):
                st.session_state.selected_tree_id = r["id"]
                st.rerun()
