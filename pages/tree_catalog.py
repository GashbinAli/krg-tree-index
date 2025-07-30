import streamlit as st
from pathlib import Path
from db_handler import execute_query

# ─── header helper ─────────────────────────────────────────────
_ASSETS = Path(__file__).resolve().parent.parent / "assets"
def show_header():
    col_left, col_center, col_right = st.columns([0.15, 0.7, 0.15])
    with col_left:
        st.image(_ASSETS / "hasar_logo.png", use_column_width="auto")
    with col_right:
        st.image(_ASSETS / "gov_logo.png",  use_column_width="auto")
# ───────────────────────────────────────────────────────────────

st.set_page_config(page_title="KRG Tree Index – Tree Catalog", layout="wide")
show_header()

st.title("🌲 Tree Catalog")

rows = execute_query(
    "SELECT tree_name, scientific_name FROM tree_data ORDER BY tree_name;",
    fetch=True,
)
for r in rows:
    st.subheader(r["tree_name"])
    st.markdown(f"*{r['scientific_name']}*")
    st.markdown("---")
