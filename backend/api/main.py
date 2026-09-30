from fastapi import FastAPI, WebSocket, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
import os
import json
import asyncio
from pathlib import Path
from typing import Optional

from core.gpu_detector import GPUDetector
from core.image_processor import ImageProcessor
from core.model_generator import ModelGenerator
from core.blender_integration import BlenderIntegration
from utils.file_manager import FileManager

app = FastAPI(title="Generador de Piñatas 3D", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar componentes
gpu_info = GPUDetector.detect_gpu()
image_processor = ImageProcessor(max_size=1536 if gpu_info['total_memory_mb'] >= 12288 else 1024)
model_generator = ModelGenerator(gpu_info)
blender_integration = BlenderIntegration()
file_manager = FileManager()

# Directorios
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Montar directorios estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

@app.get("/api/gpu-info")
async def get_gpu_info():
    """Obtiene información sobre la GPU disponible."""
    return gpu_info

@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    """Sube una imagen para procesamiento."""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen.")
    
    # Guardar imagen
    file_path = await file_manager.save_upload(file, UPLOAD_DIR)
    
    return {"file_path": str(file_path), "filename": file.filename}

@app.post("/api/preprocess")
async def preprocess_image(file_path: str):
    """Preprocesa una imagen para generación 3D."""
    try:
        # Procesar imagen
        image, mask = image_processor.process_image(file_path)
        
        # Guardar imagen procesada
        processed_path = file_manager.save_processed_image(image, OUTPUT_DIR)
        mask_path = file_manager.save_mask(mask, OUTPUT_DIR)
        
        return {
            "processed_image_path": str(processed_path),
            "mask_path": str(mask_path)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/generate")
async def generate_model(websocket: WebSocket):
    """Genera un modelo 3D a través de WebSocket."""
    await websocket.accept()
    
    try:
        # Recibir parámetros
        data = await websocket.receive_text()
        params = json.loads(data)
        
        # Procesar imagen
        await websocket.send_json({"progress": 0, "message": "Procesando imagen..."})
        image, mask = image_processor.process_image(params['image_path'])
        
        # Generar modelo
        def progress_callback(progress, message):
            asyncio.create_task(websocket.send_json({"progress": progress, "message": message}))
        
        vertices, faces, textures = model_generator.generate_model(
            image=image,
            mask=mask,
            pinata_type=params['pinata_type'],
            style_mode=params['style_mode'],
            progress_callback=progress_callback
        )
        
        # Guardar modelo
        model_path = file_manager.save_model(vertices, faces, textures, OUTPUT_DIR)
        
        await websocket.send_json({
            "progress": 100,
            "message": "Modelo generado correctamente.",
            "model_path": str(model_path)
        })
        
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()

@app.post("/api/edit")
async def edit_model(model_path: str, edit_params: dict):
    """Edita un modelo 3D existente."""
    try:
        # Cargar modelo
        vertices, faces, textures = file_manager.load_model(model_path)
        
        # Aplicar ediciones
        if 'pinata_type' in edit_params:
            vertices, faces = model_generator._adapt_to_pinata_type(
                vertices, faces, edit_params['pinata_type']
            )
        
        if 'style_mode' in edit_params:
            vertices, faces, textures = model_generator._apply_style(
                vertices, faces, textures, edit_params['style_mode']
            )
        
        # Guardar modelo editado
        edited_path = file_manager.save_model(vertices, faces, textures, OUTPUT_DIR)
        
        return {"model_path": str(edited_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/export")
async def export_model(model_path: str, format: str, output_path: Optional[str] = None):
    """Exporta un modelo en el formato especificado."""
    try:
        # Determinar ruta de salida
        if not output_path:
            output_path = str(OUTPUT_DIR / f"pinata.{format}")
        
        # Exportar modelo
        success = blender_integration.export_model(model_path, output_path, format)
        
        if success:
            return {"output_path": output_path}
        else:
            raise HTTPException(status_code=500, detail="Error al exportar el modelo.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/open-in-blender")
async def open_in_blender(model_path: str, pinata_type: str, materials: dict):
    """Abre un modelo en Blender con scripts preconfigurados."""
    try:
        success = blender_integration.open_in_blender(
            model_path=model_path,
            pinata_type=pinata_type,
            materials=materials
        )
        
        if success:
            return {"message": "Blender abierto correctamente."}
        else:
            raise HTTPException(status_code=500, detail="Error al abrir Blender.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
async def get_history():
    """Obtiene el historial de proyectos."""
    return file_manager.get_history()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
