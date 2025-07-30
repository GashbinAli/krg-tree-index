"""
Tree Search page
----------------
• Searches Neon `tree_data`.
• Lists unique tree names.
• Click a row → full profile (rating, score table, info paragraphs).
"""

import os
import streamlit as st
import pandas as pd  # for the score table

# ---------------------------------------------------------------------
# Robust import for db_helper
# ---------------------------------------------------------------------
try:
    from db_handler import execute_query
except ModuleNotFoundError:
    import importlib.util, sys
    from pathlib import Path

    helper_path = Path(__file__).resolve().parent.parent / "db-handler.py"
    if helper_path.exists():
        spec = importlib.util.spec_from_file_location("db_handler", helper_path)
        db_handler = importlib.util.module_from_spec(spec)            # type: ignore
        sys.modules["db_handler"] = db_handler
        spec.loader.exec_module(db_handler)                           # type: ignore[arg-type]
        execute_query = db_handler.execute_query                      # type: ignore[attr-defined]
    else:
        raise

# ---------------------------------------------------------------------
# Optional secrets override
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
Type part of a *common* or *scientific* name.  
Click a result to view its full profile.
"""
)

# ---------------------------------------------------------------------
# Session state (selected tree)
# ---------------------------------------------------------------------
if "selected_tree_id" not in st.session_state:
    st.session_state.selected_tree_id = None

# ---------------------------------------------------------------------
# Search box
# ---------------------------------------------------------------------
search_term = st.text_input("Search:").strip()

# ---------------------------------------------------------------------
# Layout columns
# ---------------------------------------------------------------------
if st.session_state.selected_tree_id:
    col_list, col_detail = st.columns([1, 2])
else:
    col_list, col_detail = st.columns([1, 0.05])

# ---------------------------------------------------------------------
# DETAIL PANEL
# ---------------------------------------------------------------------
with col_detail:
    if st.session_state.selected_tree_id:
        tree = execute_query(
            "SELECT * FROM tree_data WHERE id = %s;",
            (st.session_state.selected_tree_id,),
            fetch=True,
        )[0]

        # 1️⃣ Rating
        st.header(tree["tree_name"])
        st.markdown(f"### Rating: {tree.get('rating', 'N/A')}")

        # 2️⃣ Score table (black bold text)
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

        score_rows = [
            {"Criterion": label, "Score": tree[col]}
            for col, label in score_labels.items()
            if col in tree and tree[col] is not None
        ]

        if score_rows:
            df = pd.DataFrame(score_rows).set_index("Criterion")

            styled_df = (
                df.style
                .set_properties(**{"color": "black", "font-weight": "bold"})
                .set_table_styles(
                    [{"selector": "th", "props": [("color", "black"), ("font-weight", "bold")]}]
                )
            )
            st.table(styled_df)

        # 3️⃣ Info paragraphs
        st.markdown("---")
        st.markdown(f"**Information**  \n{tree.get('information', 'N/A')}")
        st.markdown(f"**Suitability**  \n{tree.get('suitability', 'N/A')}")
        st.markdown(f"**Challenges**  \n{tree.get('challenges', 'N/A')}")
        st.markdown("---")

        if st.button("🔙 Back to results"):
            st.session_state.selected_tree_id = None
            st.rerun()

# ---------------------------------------------------------------------
# LIST PANEL
# ---------------------------------------------------------------------
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
        st.info("Start typing to search, or click a sample below.")
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
