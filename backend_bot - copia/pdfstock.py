from pymongo import MongoClient
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
import os

# Cargar .env
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
LOGO_PATH = "sia logotipo.jpg"  # Debe estar en la misma carpeta que este script
PDF_PATH = "stock_con_precios.pdf"

# Conexión a MongoDB
client = MongoClient(MONGO_URI)
db = client["sio_global"]
col = db["articulos"]

# Obtener artículos con stock > 0
articulos = list(col.find({"stock": {"$gt": 0}}, {
    "idArticulo": 1,
    "nombre": 1,
    "stock": 1,
    "precioVenta": 1
}))

# Crear PDF
c = canvas.Canvas(PDF_PATH, pagesize=A4)
width, height = A4  # ← Esto es lo que faltaba
fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

# Título y fecha
c.setFont("Helvetica-Bold", 14)
c.drawString(2 * cm, height - 2 * cm, f"Listado de Stock y Precios - {fecha}")

# Logo a la derecha, escala 1/4 de hoja
logo_width = width / 4
logo_img = Image.open(LOGO_PATH)
aspect = logo_img.height / logo_img.width
logo_height = logo_width * aspect
c.drawImage(LOGO_PATH, width - logo_width - 2 * cm, height - logo_height - 2 * cm, logo_width, logo_height)

# Encabezado de tabla con márgenes de 1 cm entre campos
y = height - 4 * cm
c.setFont("Helvetica-Bold", 10)
c.drawString(1 * cm, y, "ID")
c.drawString(5 * cm, y, "Nombre")
c.drawString(14 * cm, y, "Stock")
c.drawString(17 * cm, y, "Precio")
y -= 0.5 * cm

# Contenido
c.setFont("Helvetica", 10)
for art in articulos:
    if y < 2 * cm:
        c.showPage()
        y = height - 2 * cm
    c.drawString(1 * cm, y, str(art.get("idArticulo", "")))
    c.drawString(5 * cm, y, str(art.get("nombre", "")[:40]))
    c.drawString(14 * cm, y, str(art.get("stock", "")))
    c.drawString(17 * cm, y, f"${art.get('precioVenta', 0):.2f}")
    y -= 0.5 * cm

c.save()
print(f"📄 PDF generado: {PDF_PATH}")
