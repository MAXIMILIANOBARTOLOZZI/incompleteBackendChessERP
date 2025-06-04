import os
import requests
import json
from dotenv import load_dotenv
from login import login  # Usa tu login actual

load_dotenv()
API_BASE = os.getenv("CHESS_API_URL").rstrip("/")

def exportar_stock_json():
    session_id = login()
    headers = {
        "Accept": "application/json",
        "Cookie": session_id
    }

    url = f"{API_BASE}/web/api/chess/v1/stock/?idDeposito=001"
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        data = resp.json()
        with open("respuesta_stock.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("✅ Archivo JSON guardado como respuesta_stock.json")
    else:
        print(f"❌ Error al obtener stock: {resp.status_code}")

if __name__ == "__main__":
    exportar_stock_json()
