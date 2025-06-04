# test.py
import os
import requests
import json
from dotenv import load_dotenv
from login import login

# Cargar variables del .env
load_dotenv()
API_BASE = os.getenv("CHESS_API_URL").rstrip("/")
ID_DEPOSITO = "001"

def test_stock_disponible():
    # Hacer login y armar headers
    session_id = login()
    headers = {
        "Accept": "application/json",
        "Cookie": session_id
    }

    # Consultar el endpoint actual de stock
    url = f"{API_BASE}/web/api/chess/v1/stock/?idDeposito={ID_DEPOSITO}"
    try:
        print(f"🔎 Consultando: {url}")
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            print("🧾 Respuesta completa:")
            print(json.dumps(data, indent=2))  # Mostrar todo el JSON bien formateado
        else:
            print(f"⚠️ Error {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

# Ejecutar test
if __name__ == "__main__":
    test_stock_disponible()
