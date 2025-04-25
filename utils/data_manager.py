# utils/data_manager.py
import json
import os
from datetime import datetime

PREMIUM_FILE = "premium_users.json"
TEMP_FILE = "temp_login.json"

def load_premium_users():
    if os.path.exists(PREMIUM_FILE):
        with open(PREMIUM_FILE, "r") as f:
            return json.load(f)
    return {}

def save_premium_users(premium_users):
    with open(PREMIUM_FILE, "w") as f:
        json.dump(premium_users, f, indent=2)

def load_temp_data():
    if os.path.exists(TEMP_FILE):
        with open(TEMP_FILE, "r") as f:
            return json.load(f)
    return {}

def save_temp_data(user_data):
    with open(TEMP_FILE, "w") as f:
        json.dump(user_data, f, indent=2)