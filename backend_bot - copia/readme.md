prcoeso de precios descargando lista de precios desde chess erp web y redireccionarlo a la base de datos msql
[1] Cargar Excel de precios
[2] Leer idArticulo, descripcion, precioVenta
[3] Conectar a MongoDB
[4] Por cada artículo del Excel:
    [4.1] Buscar en Mongo el artículo por idArticulo
    [4.2] Verificar que la descripción también coincida
    [4.3] Si todo ok → actualizar campo precioVenta
    [4.4] Si algo no coincide → registrar en lista de errores
[5] Mostrar resumen final de:
     - Artículos actualizados
     - Artículos ignorados por error


carpetas y explicacion de cada una:

python unificar_precios_en_articulos.py
test.py
precios.py
mongo_conn.py
login.py
clientes.py
articulos.py

pip list

Package                Version
---------------------- -----------
aiohappyeyeballs       2.6.1
aiohttp                3.11.18
aiohttp-retry          2.9.1
aiosignal              1.3.2
annotated-types        0.7.0
anyio                  4.9.0
attrs                  25.3.0
blinker                1.9.0
certifi                2025.1.31
chardet                5.2.0
charset-normalizer     3.4.1
click                  8.1.8
colorama               0.4.6
distro                 1.9.0
dnspython              2.7.0
et_xmlfile             2.0.0
fastapi                0.115.12
Flask                  3.1.0
frozenlist             1.6.0
h11                    0.16.0
httpcore               1.0.9
httptools              0.6.4
httpx                  0.28.1
idna                   3.10
itsdangerous           2.2.0
Jinja2                 3.1.6
jiter                  0.9.0
lxml                   5.4.0
MarkupSafe             3.0.2
multidict              6.4.3
mysql-connector-python 9.3.0
numpy                  2.2.5
openai                 1.77.0
openpyxl               3.1.5
pandas                 2.2.3
pillow                 11.2.1
pip                    25.0.1
propcache              0.3.1
pydantic               2.11.4
pydantic_core          2.33.2
PyJWT                  2.10.1
pymongo                4.12.1
python-dateutil        2.9.0.post0
python-docx            1.1.2
python-dotenv          1.1.0
pytz                   2025.2
PyYAML                 6.0.2
redis                  6.0.0
reportlab              4.4.1
requests               2.32.3
six                    1.17.0
sniffio                1.3.1
starlette              0.46.2
tqdm                   4.67.1
typing_extensions      4.13.2
typing-inspection      0.4.0
tzdata                 2025.2
urllib3                2.4.0
uvicorn                0.34.2
watchfiles             1.0.5
websockets             15.0.1
Werkzeug               3.1.3
yarl                   1.20.0



conexionesa con el bot de twilio y open ai:

# 📦 backend_bot - Backend del Bot Preventista SIA

Este proyecto forma parte del sistema inteligente de pedidos `SIA Bot`, orientado a empresas de distribución y logística. El backend se conecta a Chess ERP, consulta artículos y vencimientos, y guarda la información en una base de datos MongoDB para su uso posterior por el bot de WhatsApp (Twilio + OpenAI).

---

## 📁 Estructura de Archivos

```
backend_bot/
├── .env                        # Variables de entorno (URLs, credenciales)
├── articulos.py               # Descarga y guarda artículos desde Chess ERP
├── exportar_vencimientos.py   # Filtra artículos con vencimientos próximos y genera reportes
```

---

## 📄 .env

Archivo oculto para guardar variables sensibles como:

```
CHESS_API_URL=http://appserver26.dyndns.org:
CHESS_USER=tu_usuario
CHESS_PASS=tu_contraseña
MONGO_URI=mongodb://localhost:
```

> ⚠️ Este archivo no debe subirse al repositorio. Usar `.gitignore`.

---

## 📄 articulos.py

Script que:
- Se conecta a la API de Chess ERP.
- Filtra los artículos no anulados (`anulado = False`).
- Inserta o actualiza los datos en la colección `sio_global.articulos` en MongoDB.

Librerías utilizadas:
- `requests`
- `pymongo`
- `dotenv`

---

## 📄 exportar_vencimientos.py

Script que:
- Consulta los artículos en MongoDB.
- Filtra aquellos con fechas de vencimiento menores a 2 meses.
- Genera un reporte con:
  - Código de producto
  - Nombre
  - Stock
  - Fecha de vencimiento
- (Opcional) Envía el PDF por correo.

Librerías utilizadas:
- `pandas`
- `datetime`
- `fpdf` (o similar para PDF)
- `yagmail` (opcional)

---

## 🚀 Cómo ejecutar

1. Crear y completar el archivo `.env` con tus credenciales.
2. Instalar dependencias:
```bash
pip install -r requirements.txt
```
3. Ejecutar el script que necesites:
```bash
python articulos.py
python exportar_vencimientos.py
```

---

## ✅ Próximas mejoras

- Separación modular de funciones (`services/`, `utils/`).
- Integración directa con el bot de WhatsApp (`twilio_bot.py`).
- Automatización de tareas vía cron o sistema programado.

---

## 🧠 Autor

Desarrollado por **Maximiliano Rodas Bartolozzi** junto a Geppie 🤖 como asistente técnico.
