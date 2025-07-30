import os
import streamlit as st
import pandas as pd
from pathlib import Path

# ─── header helper (same block) ────────────────────────────────
_ASSETS = Path(__file__).resolve().parent.parent / "assets"
def show_header():
    col_left, col_center, col_right = st.columns([0.15, 0.7, 0.15])
    with col_left:
        st.image(_ASSETS / "hasar_logo.png", use_column_width="auto")
    with col_right:
        st.image(_ASSETS / "gov_logo.png",  use_column_width="auto")
# ───────────────────────────────────────────────────────────────

# Page config + header
st.set_page_config(page_title="KRG Tree Index – Tree Search", layout="wide")
show_header()

# ----- robust import for db_handler -----
try:
    from db_handler import execute_query
except ModuleNotFoundError:
    import importlib.util, sys
    helper_path = Path(__file__).resolve().parent.parent / "db-handler.py"
    if helper_path.exists():
        spec = importlib.util.spec_from_file_location("db_handler", helper_path)
        db_handler = importlib.util.module_from_spec(spec)  # type: ignore
        sys.modules["db_handler"] = db_handler
        spec.loader.exec_module(db_handler)                 # type: ignore[arg-type]
        execute_query = db_handler.execute_query            # type: ignore[attr-defined]
    else:
        raise

# Optional secrets override
if "connections" in st.secrets and "postgres" in st.secrets["connections"]:
    os.environ["DATABASE_URL"] = st.secrets["connections"]["postgres"]["url"]

# ---- UI header ----
st.title("🔍 Tree Search")
st.markdown(
    "Type a *common* or *scientific* name. Click a result for its full profile."
)

# Session state for selected tree
if "selected_tree_id" not in st.session_state:
    st.session_state.selected_tree_id = None

# Search input
search_term = st.text_input("Search:").strip()

# Layout columns
cols = [1, 2] if st.session_state.selected_tree_id else [1, 0.05]
col_list, col_detail = st.columns(cols)

# ─── DETAIL panel (right) ─────────────────────────────────────
with col_detail:
    if st.session_state.selected_tree_id:
        tree = execute_query(
            "SELECT * FROM tree_data WHERE id = %s;",
            (st.session_state.selected_tree_id,),
            fetch=True,
        )[0]

        # Rating first
        st.header(tree["tree_name"])
        st.markdown(f"### Rating: {tree.get('rating', 'N/A')}")

        # Score table
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
        table_rows = [
            {"Criterion": label, "Score": tree[col]}
            for col, label in score_labels.items()
            if col in tree and tree[col] is not None
        ]
        if table_rows:
            df = pd.DataFrame(table_rows).set_index("Criterion")
            styled = (
                df.style
                .set_properties(**{"color": "black", "font-weight": "bold"})
                .set_table_styles(
                    [{"selector": "th",
                      "props": [("color", "black"), ("font-weight", "bold")]}]
                )
            )
            st.table(styled)

        # Info paragraphs
        st.markdown("---")
        st.markdown(f"**Information**\n\n{tree.get('information', 'N/A')}")
        st.markdown(f"**Suitability**\n\n{tree.get('suitability', 'N/A')}")
        st.markdown(f"**Challenges**\n\n{tree.get('challenges', 'N/A')}")
        st.markdown("---")

        if st.button("🔙 Back to results"):
            st.session_state.selected_tree_id = None
            st.rerun()

# ─── LIST panel (left) ────────────────────────────────────────
with col_list:
    if search_term:
        rows = execute_query(
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
        if rows:
            st.subheader(f"{len(rows)} result(s)")
            for r in rows:
                if st.button(f"{r['tree_name']} — {r['scientific_name']}",
                             key=f"row_{r['id']}",
                             use_container_width=True):
                    st.session_state.selected_tree_id = r["id"]
                    st.rerun()
        else:
            st.info("No match found.")
    else:
        st.info("Start typing, or click one below.")
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
            if st.button(f"{r['tree_name']} — {r['scientific_name']}",
                         key=f"preview_{r['id']}",
                         use_container_width=True):
                st.session_state.selected_tree_id = r["id"]
                st.rerun()
