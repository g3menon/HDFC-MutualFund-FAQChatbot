import json
import os
from .config import STATUS_FILE_PATH

def init_status_tracker():
    os.makedirs(os.path.dirname(STATUS_FILE_PATH), exist_ok=True)
    if not os.path.exists(STATUS_FILE_PATH):
        update_status({"status": "initialized", "last_run": None})

def update_status(status_dict):
    init_status_tracker()
    with open(STATUS_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(status_dict, f, indent=4)

def read_status():
    if not os.path.exists(STATUS_FILE_PATH):
         return {}
    with open(STATUS_FILE_PATH, 'r', encoding='utf-8') as f:
         try:
             return json.load(f)
         except json.JSONDecodeError:
             return {}
