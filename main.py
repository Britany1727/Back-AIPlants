import os
import requests
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional  # <--- Faltaba esta importación

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PLANT_DATABASE = {
    "rose": {
        "beneficios": "Planta medicinal/ornamental. Ayuda a mejorar el ambiente y tiene propiedades relajantes.",
        "cuidados": "Luz natural abundante y riego moderado evitando el encharcamiento."
    },
    "sunflower": {
        "beneficios": "Produce semillas nutritivas y mejora el ánimo por su color vibrante.",
        "cuidados": "Requiere luz solar directa y riego según la humedad del suelo."
    }
}

@app.post("/identificar")
async def identificar_planta(
    file: Optional[UploadFile] = File(None),
    descripcion: Optional[str] = Form(None)
):
    # 1. Validación inicial: ¿Hay algo que procesar?
    if not file and not descripcion:
        return {"error": "Debes proporcionar una imagen o una descripción."}

    # 2. Lógica si hay imagen (Uso de PlantNet API)
    if file:
        API_KEY = "2b10LqAzfUGLOSey2V9xx2ZaO" 
        url = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"
        
        try:
            # IMPORTANTE: Debes leer el contenido del archivo
            contents = await file.read()
            files = [('images', (file.filename, contents, file.content_type))]
            
            response = requests.post(url, files=files)
            data = response.json()
            
            if response.status_code != 200 or not data.get('results'):
                return {"error": "No se pudo identificar la planta en la imagen."}

            nombre_planta = data['results'][0]['species']['commonNames'][0]
        except Exception as e:
            return {"error": f"Error en el servidor de identificación: {str(e)}"}
    else:
        # 3. Lógica si solo hay descripción de texto
        nombre_planta = descripcion

    # 4. Búsqueda de información en nuestra "base de datos" local
    # Buscamos coincidencias parciales en minúsculas
    info = {"beneficios": "Información no disponible.", "cuidados": "Consulta a un experto botánico."}
    
    for key, value in PLANT_DATABASE.items():
        if key.lower() in nombre_planta.lower():
            info = value
            break
    else:
        # Info genérica si no está en nuestro diccionario
        info = {
            "beneficios": "Planta identificada. Generalmente contribuye a la purificación del aire.",
            "cuidados": "Luz natural indirecta y riego moderado (verificar humedad del sustrato)."
        }

    return {
        "planta": nombre_planta,
        "beneficios": info["beneficios"],
        "cuidados": info["cuidados"]
    }