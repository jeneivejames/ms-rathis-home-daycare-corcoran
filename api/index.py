import sys
import os

# Ensure the project root (where app.py and static/ live) is on the path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app  # noqa: E402,F401  (Vercel looks for the `app` variable)
