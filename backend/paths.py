import sys
import os
from pathlib import Path

def get_base_path():
    """Get the absolute path to the directory containing the application."""
    if hasattr(sys, '_MEIPASS'):
        # Running as a PyInstaller bundle
        return Path(sys._MEIPASS)
    return Path(os.path.abspath("."))

def get_static_path():
    """Resolve the path to the 'static' directory."""
    return get_base_path() / "static"
