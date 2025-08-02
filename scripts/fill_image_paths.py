"""
fill_image_paths.py
----------------------------------
Looks at every picture in assets/tree_images/
and writes its relative path into tree_data.image_path.

File-name rule:
  Brants Oak   →  Brants_Oak.png
  (spaces & punctuation -> underscores)
"""

from pathlib import Path
from db_handler import execute_query   # <- same helper you already use

# --- Where are we? ---------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent       # krg-tree-index/
IMG_DIR   = REPO_ROOT / "assets" / "tree_images"         # images folder

# --- Simple helper ---------------------------------------------------
def slug_to_tree_name(slug: str) -> str:
    """Brants_Oak  ->  Brants Oak"""
    return slug.replace("_", " ")

# --- Main work -------------------------------------------------------
def main():
    for img in IMG_DIR.iterdir():
        if img.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
            continue   # skip non-image files

        tree_name = slug_to_tree_name(img.stem)
        rel_path = img.relative_to(REPO_ROOT).as_posix()  # always forward slashes      # e.g. assets/tree_images/Brants_Oak.png

        execute_query(
            "UPDATE tree_data SET image_path = %s WHERE tree_name ILIKE %s;",
            (rel_path, tree_name),
        )
        print(f"{tree_name}  ->  {rel_path}")

    print("✅  image_path column populated.")

if __name__ == "__main__":
    main()
