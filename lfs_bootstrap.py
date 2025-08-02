# lfs_bootstrap.py
"""
Pull Git-LFS files (images) the first time a Streamlit session starts.

Why?  On Streamlit Cloud (and any fresh container) `git clone`
fetches only small pointer files.  We need to do `git lfs pull`
once so real PNG/JPG bytes are present for st.image().
"""

from pathlib import Path
import subprocess
import sys

def ensure_lfs_pulled() -> None:
    repo_root = Path(__file__).resolve().parent
    marker = Path("/tmp/lfs_done")

    # Skip if we've already pulled in this container session
    if marker.exists():
        return

    # Only run if repo uses LFS (check .gitattributes for "filter=lfs")
    gattr = repo_root / ".gitattributes"
    if not gattr.exists() or "filter=lfs" not in gattr.read_text():
        return  # nothing to pull

    try:
        # Initialize LFS in this repo (local) and pull all objects
        subprocess.run(["git", "lfs", "install", "--local"], check=True, cwd=repo_root)
        subprocess.run(["git", "lfs", "pull"], check=True, cwd=repo_root)
        marker.touch()  # create marker so we don't repeat
        print("✔️  Git-LFS images pulled.")
    except Exception as e:
        print("⚠️  Git-LFS pull failed:", e, file=sys.stderr)

