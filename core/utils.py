import json
import os

# Assuming this file lives in project_matchmaker/core/
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return json.load(f)

def save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
