from mongo_conn import connect_mongo
import pandas as pd
from datetime import datetime, timedelta

def exportar_vencimientos():
    db = connect_mongo()
    col = db["articulos"]

    hoy = datetime.now()
    limite = hoy + timedelta(days=60)

    # Filtro: vencimiento entre hoy y +60 días, y distinto de null
    articulos = list(col.find({
        "vencimiento": {
            "$gte": hoy,
            "$lte": limite
        }
    }, {
        "_id": 0,
        "codigo": 1,
        "nombre": 1,
        "stock": 1,
        "vencimiento": 1
    }))

    if not articulos:
        print("⚠️ No se encontraron artículos por vencer en los próximos 60 días.")
        return

    # Crear DataFrame
    df = pd.DataFrame(articulos)

    # Formatear fecha
    df["vencimiento"] = pd.to_datetime(df["vencimiento"]).dt.strftime("%d/%m/%Y")

    # Exportar a Excel
    df.to_excel("vencimientos_60_dias.xlsx", index=False)
    print("✅ Archivo exportado: vencimientos_60_dias.xlsx")

if __name__ == "__main__":
    exportar_vencimientos()
