# login.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.getenv("CHESS_API_URL")
USER = os.getenv("CHESS_USER")
PASS = os.getenv("CHESS_PASS")

def login():
    login_url = f"{API_BASE}/web/api/chess/v1/auth/login"
    payload = {
        "usuario": USER,
        "password": PASS
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(login_url, json=payload, headers=headers)

    if response.status_code == 200:
        session_id = response.json().get("sessionId", "")
        print(f"✅ Login exitoso: {session_id}")
        return session_id
    else:
        raise Exception(f"❌ Login fallido: {response.status_code} - {response.text}")

