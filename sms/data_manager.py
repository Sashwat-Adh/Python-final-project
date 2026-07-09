"""
data_manager.py
----------------
Week 4 (File Handling) + Week 8 (JSON) concepts live here.

This module gives us ONE reusable class, DataManager, that knows how to:
  - read a .json file into a Python list/dict
  - write a Python list/dict back out to a .json file
  - handle errors gracefully (missing file, corrupted file, etc.)

Every other part of the app (students, teachers, courses, marks, attendance)
reuses this same class instead of repeating file-handling code. This is the
"Don't Repeat Yourself" (DRY) principle.
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


class DataManager:
    """Handles loading and saving a single JSON file."""

    def __init__(self, filename):
        # filename e.g. "students.json"
        self.filepath = os.path.join(DATA_DIR, filename)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """If the JSON file doesn't exist yet, create it with an empty list."""
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load(self):
        """Read the JSON file and return its contents (a list of dicts)."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file is missing or corrupted, fail safe with an empty list
            return []

    def save(self, data):
        """Write `data` (a list of dicts) back to the JSON file."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return True
        except OSError as e:
            print(f"Error saving {self.filepath}: {e}")
            return False
