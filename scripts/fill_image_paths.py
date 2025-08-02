"""
scripts/fill_image_paths.py
---------------------------
Populates tree_data.image_path so Streamlit can display thumbnails.

Rules
-----
1. By default a file is matched by slugifying the *tree_name*
   Example:
       "Brants Oak"  ->  "Brants_Oak.png"
   so
       assets/tree_images/Brants_Oak.png
   will be linked to that row.

2. You can override / extend matches via assets/image_map.csv
   Columns: tree_name,scientific_name,image_file
   (scientific_name is optional but helps when two trees share a name.)

Run:
    python -m scripts.fill_image_paths
"""

from pathlib import Path
import csv
from db_handler import execute_query, execute_many

# ------------------------------------------------------------------ #
# Paths
# ------------------------------------------------------------------ #
REPO_ROOT = Path(__file__).resolve().parent.parent
IMG_DIR   = REPO_ROOT / "assets" / "tree_images"
MAP_CSV   = REPO_ROOT / "assets" / "image_map.csv"  # optional

# ------------------------------------------------------------------ #
# Helpers
# ------------------------------------------------------------------ #
def slugify(text: str) -> str:
    """
    Very simple slug: spaces, hyphens → underscores; remove punctuation.
    'Afghan Pine' -> 'afghan_pine'
    """
    import re, unicodedata

    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^\w\s-]", "", text, flags=re.A).strip().lower()
    return re.sub(r"[\s-]+", "_", text)


def relative_posix(path: Path) -> str:
    """assets\\tree_images\\x.png  ->  assets/tree_images/x.png"""
    return path.relative_to(REPO_ROOT).as_posix()


# ------------------------------------------------------------------ #
# 1) Build lookup: key -> image path
# key is slugified tree name (lowercase, underscores)
# ------------------------------------------------------------------ #
lookup: dict[str, str] = {}

for img in IMG_DIR.glob("*"):
    if img.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
        continue
    key = slugify(img.stem)
    lookup[key] = relative_posix(img)

# Optional explicit mappings
if MAP_CSV.exists():
    with MAP_CSV.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            k = slugify(row["tree_name"])
            lookup[k] = relative_posix(IMG_DIR / row["image_file"])

# ------------------------------------------------------------------ #
# 2) Fetch tree rows + prepare updates
# ------------------------------------------------------------------ #
rows = execute_query(
    "SELECT id, tree_name, image_path FROM tree_data;", fetch=True
)

updates: list[tuple[str, int]] = []
matched, missing = 0, 0

for r in rows:
    key = slugify(r["tree_name"])
    if key in lookup:
        new_path = lookup[key]
        if r["image_path"] != new_path:              # update only if changed
            updates.append((new_path, r["id"]))
        matched += 1
    else:
        missing += 1

# ------------------------------------------------------------------ #
# 3) Bulk update
# ------------------------------------------------------------------ #
if updates:
    execute_many(
        "UPDATE tree_data SET image_path = %s WHERE id = %s;",
        updates,
    )

print(f"✅  {matched} rows matched; {len(updates)} updated; {missing} with no image.")
