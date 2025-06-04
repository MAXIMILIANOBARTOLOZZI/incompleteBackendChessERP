# articulos.py con idArticulo como entero
import os
import requests
import time
from datetime import datetime
from dotenv import load_dotenv
from login import login
from mongo_conn import connect_mongo

load_dotenv()
API_BASE = os.getenv("CHESS_API_URL").rstrip("/")

def obtener_stock_general(headers):
    url = f"{API_BASE}/web/api/chess/v1/stock/?idDeposito=001"
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            stock_items = data.get("dsStockFisicoApi", {}).get("dsStock", [])
            stock_dict = {}
            vencimiento_dict = {}
            for item in stock_items:
                id_articulo = int(item.get("idArticulo"))
                bultos = item.get("cantBultos", 0)
                vencimiento = item.get("fecVtoLote")
                stock_dict[id_articulo] = bultos
                if vencimiento:
                    vencimiento_dict.setdefault(id_articulo, vencimiento)
            print(f"📦 Stock (bultos) recibido para {len(stock_dict)} artículos.")
            return stock_dict, vencimiento_dict
        else:
            print(f"⚠️ Error al obtener stock: {resp.status_code}")
            return {}, {}
    except Exception as e:
        print(f"❌ Error consultando stock general: {e}")
        return {}, {}

def fetch_articulos(session_id):
    db = connect_mongo()
    col = db["articulos"]

    headers = {
        "Accept": "application/json",
        "Cookie": session_id
    }

    stock_dict, vencimiento_dict = obtener_stock_general(headers)
    total_guardados = 0
    nro_lote = 1

    while True:
        url = f"{API_BASE}/web/api/chess/v1/articulos/?nroLote={nro_lote}"
        print(f"🔄 Consultando lote {nro_lote}...")
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"❌ Error al consultar lote {nro_lote}: {response.status_code}")
            break

        try:
            data = response.json()
        except Exception as e:
            print("⚠️ Error interpretando JSON")
            print(response.text)
            break

        articulos = data.get("Articulos", {}).get("eArticulos", [])
        if not articulos:
            print("✅ No hay más artículos. Fin de lotes.")
            break

        print(f"📦 Artículos recibidos en lote {nro_lote}: {len(articulos)}")

        for art in articulos:
            if not art.get("anulado", False):
                try:
                    id_articulo = int(art.get("idArticulo"))
                except:
                    print(f"❌ ID inválido: {art.get('idArticulo')}")
                    continue

                stock = stock_dict.get(id_articulo, 0)
                vencimiento_str = vencimiento_dict.get(id_articulo)
                vencimiento_dt = None

                if vencimiento_str:
                    try:
                        vencimiento_dt = datetime.strptime(vencimiento_str[:10], "%Y-%m-%d")
                    except:
                        vencimiento_dt = None

                documento = {
                    "idArticulo": id_articulo,
                    "codigo": str(id_articulo),
                    "nombre": art.get("desArticulo", "").strip(),
                    "stock": stock,
                    "unidadesBulto": art.get("unidadesBulto", 0),
                    "activo": True,
                    "vencimiento": vencimiento_dt
                }

                print(f"💾 Guardando {id_articulo} - {documento['nombre']} - Bultos: {stock}")
                col.update_one(
                    {"idArticulo": id_articulo},
                    {"$set": documento},
                    upsert=True
                )
                total_guardados += 1

        nro_lote += 1

    print(f"✅ Total artículos actualizados y limpiados: {total_guardados}")

def run_eternamente():
    while True:
        session_id = login()
        fetch_articulos(session_id)
        print("⏳ Esperando 2 minutos para próxima actualización...\n")
        time.sleep(120)

if __name__ == "__main__":
    run_eternamente()
