from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Cargar entorno
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:")

# Conexión Mongo
client = MongoClient(MONGO_URI)
db = client["sio_global"]
articulos_col = db["articulos"]
precios_col = db["precios"]

# Crear diccionario de precios por idArticulo
precios_dict = {
    doc["idArticulo"]: doc["precioVenta"]
    for doc in precios_col.find({}, {"idArticulo": 1, "precioVenta": 1})
}

# Contadores
actualizados = 0
sin_precio = 0

# Actualizar artículos con precio
for articulo in articulos_col.find():
    id_articulo = articulo.get("idArticulo")

    if id_articulo in precios_dict:
        precio = precios_dict[id_articulo]
        articulos_col.update_one(
            {"_id": articulo["_id"]},
            {"$set": {"precioVenta": precio}}
        )
        print(f"✅ Precio actualizado: {id_articulo} → ${precio}")
        actualizados += 1
    else:
        sin_precio += 1
        print(f"⚠️ Sin precio: {id_articulo}")

# Reporte final
print("\n📊 Sincronización completada.")
print(f"✔️ Artículos actualizados con precio: {actualizados}")
print(f"⚠️ Artículos sin precio cargado: {sin_precio}")
