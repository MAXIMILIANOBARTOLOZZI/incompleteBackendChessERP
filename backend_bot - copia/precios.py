from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

# Cargar entorno
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:")
EXCEL_PATH = "preciosmacros.xltm"  # Archivo definitivo

# Leer Excel
df = pd.read_excel(EXCEL_PATH)

# Renombrar columnas correctamente
df = df.rename(columns={
    "Artículo": "idArticulo",
    "Descripción": "descripcion",
    "Precio Final": "precioVenta"
})

# Limpieza de datos
df["idArticulo"] = pd.to_numeric(df["idArticulo"], errors="coerce").astype("Int64")
df["precioVenta"] = pd.to_numeric(df["precioVenta"], errors="coerce")
df = df.dropna(subset=["idArticulo", "precioVenta"])
df = df[df["precioVenta"] > 0]

# Conectar a MongoDB
client = MongoClient(MONGO_URI)
db = client["sio_global"]
col = db["precios"]

actualizados = 0
errores = []

# Guardar precios en colección 'precios'
for _, row in df.iterrows():
    id_articulo = int(row["idArticulo"])
    descripcion = row["descripcion"]
    precio = row["precioVenta"]

    doc = {
        "idArticulo": id_articulo,
        "descripcion": descripcion,
        "precioVenta": precio,
        "fechaCarga": datetime.now()
    }

    result = col.update_one(
        {"idArticulo": id_articulo},
        {"$set": doc},
        upsert=True
    )

    if result.matched_count or result.upserted_id:
        print(f"✅ Guardado: {id_articulo} - {descripcion} → ${precio:.2f}")
        actualizados += 1
    else:
        errores.append(f"❌ No se pudo guardar ID {id_articulo} - {descripcion}")

# Reporte final
print("\n📊 Proceso completado.")
print(f"✔️ Precios cargados/actualizados: {actualizados}")
print(f"⚠️ Errores detectados: {len(errores)}")

for error in errores:
    print(error)
