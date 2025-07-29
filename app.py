import streamlit as st
import pandas as pd

# === Page configuration ===
st.set_page_config(page_title="KRG Tree Index", layout="wide")

# === Load Excel data ===
@st.cache_data
def load_data():
    EXCEL_FILE = "data/tree_data_with_images.xlsx"  # ← Corrected path
    df = pd.read_excel(EXCEL_FILE)
    return df

df = load_data()

# === Sidebar Navigation ===
st.sidebar.title("🌳 KRG Tree Index")
page = st.sidebar.radio("Go to", ["Tree Search", "Tree Catalog"])

# === Page 1: Tree Search ===
if page == "Tree Search":
    st.title("🔍 Tree Search")
    st.write("Type a tree name in the search box below to see its details.")

    # Search box
    search_query = st.text_input("Search Tree by Name:")

    if search_query:
        # Filter dataframe by matching tree name
        results = df[df["Tree Name"].str.contains(search_query, case=False, na=False)]

        if not results.empty:
            for index, row in results.iterrows():
                st.subheader(row["Tree Name"])
                st.markdown(f"**Scientific Name:** {row['Scientific Name']}")
                st.markdown(f"**Suitability for Erbil:** {row['Suitability']}")
                st.markdown(f"**Water Need:** {row['Water Need']}")
                st.markdown(f"**Shade Value:** {row.get('Shade Value', 'N/A')}")
                st.markdown("---")
        else:
            st.warning("No tree found with that name.")

# === Page 2: Tree Catalog ===
elif page == "Tree Catalog":
    st.title("🌲 Tree Catalog")
    st.write("Here is the full visual catalog of trees.")

    # Show all tree names (add images later)
    for index, row in df.iterrows():
        st.subheader(row["Tree Name"])
        st.markdown(f"**Scientific Name:** {row['Scientific Name']}")
        st.markdown(f"**Suitability for Erbil:** {row['Suitability']}")
        st.markdown(f"**Water Need:** {row['Water Need']}")
        st.markdown("---")
