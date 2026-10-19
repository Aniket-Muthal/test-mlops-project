"""
paths.py
"""


from pathlib import Path


# Project root
ROOT_DIR = Path(__file__).resolve().parents[3]

# Configuration files
PARAMS_FILE_PATH = ROOT_DIR / "params.yaml"