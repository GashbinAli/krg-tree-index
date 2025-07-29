import streamlit as st
import pandas as pd
import os
from pathlib import Path

# ───────────────────────────────────────────────
#  PAGE CONFIG
# ───────────────────────────────────────────────
st.set_page_config(page_title="KRG Tree Index", page_icon="🌳", layout="centered")
st.title("🌳 Smart Tree System")
st.subheader("KRG Tree Index – Search Tree Suitability")
st.markdown("Type a tree name below to check if it's suitable for planting in Erbil.")

# ───────────────────────────────────────────────
#  CONSTANTS
# ───────────────────────────────────────────────
EXCEL_FILE     = "tree_data_with_images.xlsx"  # your data file
IMAGE_FOLDER   = Path("Images")                # local images folder
IMAGE_EXTS     = [".jpg", ".jpeg", ".png", ".webp"]  # allowed extensions

# ───────────────────────────────────────────────
#  LOAD DATA
# ───────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel(EXCEL_FILE)
    df = df.rename(columns={
        "Suitability (Erbil climate)": "Suitability",
        "Score (1–5)": "Score"
    })
    return df

df = load_data()

# ───────────────────────────────────────────────
#  HELPER TO FIND IMAGE
# ───────────────────────────────────────────────
def find_image_path(row) -> Path | None:
    """
    1) If the row has 'Image File' column with a value, use that.
    2) Else, build filename from the tree name and look for any allowed extension.
    Returns a Path object or None.
    """
    # 1️⃣ explicit filename
    if "Image File" in row and pd.notna(row["Image File"]):
        explicit = IMAGE_FOLDER / str(row["Image File"])
        if explicit.exists():
            return explicit

    # 2️⃣ auto‑build filename  (e.g.  Brant’s Oak  →  Brants_Oak.jpg)
    base = (
        str(row["Tree Name"])
        .replace("’", "")
        .replace("'", "")
        .replace(" ", "_")
    )
    for ext in IMAGE_EXTS:
        candidate = IMAGE_FOLDER / f"{base}{ext}"
        if candidate.exists():
            return candidate
    return None

# ───────────────────────────────────────────────
#  UI – SEARCH
# ───────────────────────────────────────────────
query = st.text_input("Enter a tree name (e.g., Oak, Olive, Pine):")

if query:
    results = df[df["Tree Name"].str.contains(query, case=False, na=False)]
    if results.empty:
        st.warning("Tree not found. Try another name.")
    else:
        for _, row in results.iterrows():
            st.markdown("---")

            # ▸ SHOW IMAGE (local)
            img_path = find_image_path(row)
            if img_path:
                st.image(str(img_path), caption=row["Tree Name"], use_column_width=True)
            else:
                st.info("📷 No local image found for this tree.")

            # ▸ SHOW DATA
            st.markdown(f"**🌳 Tree Name:** {row['Tree Name']}")
            st.markdown(f"**🔬 Scientific Name:** {row['Scientific Name']}")
            st.markdown(f"**📍 Local Name:** {row['Local Name (Kurdish)']}")
            st.markdown(f"**🌦️ Suitability:** {row['Suitability']}")
            st.markdown(f"**💧 Water Needs:** {row['Water Needs']}")
            st.markdown(f"**🌳 Shade Value:** {row['Shade Value']}")
            st.markdown(f"**🌱 Soil Compatibility:** {row['Soil Compatibility']}")
            st.markdown(f"**🧬 Native?** {row['Native?']}")
            st.markdown(f"**📊 Score:** {row['Score']}/5")
            st.markdown(f"**📚 Notes:** {row['Notes / Scientific Reasoning']}")
