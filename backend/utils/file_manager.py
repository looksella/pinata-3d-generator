import os
import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FileManager:
    """Gestiona el almacenamiento y recuperación de archivos."""
    
    def __init__(self):
        """Inicializa el gestor de archivos."""
        self.history_file = Path("history.json")
        self.history: List[Dict] = self._load_history()
    
    async def save_upload(self, file, upload_dir: Path) -> Path:
        """
        Guarda un archivo subido.
        
        Args:
            file: Archivo subido.
            upload_dir: Directorio de subidas.
            
        Returns:
            Path: Ruta al archivo guardado.
        """
        upload_dir.mkdir(exist_ok=True)
        file_path = upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Archivo guardado: {file_path}")
        return file_path
    
    def save_processed_image(self, image: np.ndarray, output_dir: Path) -> Path:
        """
        Guarda una imagen procesada.
        
        Args:
            image: Imagen procesada.
            output_dir: Directorio de salida.
            
        Returns:
            Path: Ruta a la imagen guardada.
        """
        output_dir.mkdir(exist_ok=True)
        filename = f"processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        file_path = output_dir / filename
        
        from PIL import Image
        Image.fromarray(image).save(file_path)
        
        logger.info(f"Imagen procesada guardada: {file_path}")
        return file_path
    
    def save_mask(self, mask: np.ndarray, output_dir: Path) -> Path:
        """
        Guarda una máscara.
        
        Args:
            mask: Máscara.
            output_dir: Directorio de salida.
            
        Returns:
            Path: Ruta a la máscara guardada.
        """
        output_dir.mkdir(exist_ok=True)
        filename = f"mask_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        file_path = output_dir / filename
        
        from PIL import Image
        Image.fromarray(mask).save(file_path)
        
        logger.info(f"Máscara guardada: {file_path}")
        return file_path
    
    def save_model(
        self,
        vertices: np.ndarray,
        faces: np.ndarray,
        textures: np.ndarray,
        output_dir: Path
    ) -> Path:
        """
        Guarda un modelo 3D.
        
        Args:
            vertices: Vértices del modelo.
            faces: Caras del modelo.
            textures: Texturas del modelo.
            output_dir: Directorio de salida.
            
        Returns:
            Path: Ruta al modelo guardado.
        """
        output_dir.mkdir(exist_ok=True)
        filename = f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.glb"
        file_path = output_dir / filename
        
        # Aquí se implementaría la conversión a GLB
        # Por ahora, guardamos los datos como numpy arrays
        np.savez(file_path.with_suffix('.npz'), vertices=vertices, faces=faces, textures=textures)
        
        # Guardar en historial
        self._add_to_history(file_path, vertices, faces, textures)
        
        logger.info(f"Modelo guardado: {file_path}")
        return file_path
    
    def load_model(self, model_path: str) -> tuple:
        """
        Carga un modelo 3D.
        
        Args:
            model_path: Ruta al modelo.
            
        Returns:
            tuple: Vértices, caras y texturas.
        """
        path = Path(model_path)
        
        if path.suffix == '.npz':
            data = np.load(path)
            return data['vertices'], data['faces'], data['textures']
        else:
            # Aquí se implementaría la carga de GLB/OBJ
            raise ValueError(f"Formato no soportado: {path.suffix}")
    
    def _add_to_history(
        self,
        model_path: Path,
        vertices: np.ndarray,
        faces: np.ndarray,
        textures: np.ndarray
    ):
        """
        Añade un modelo al historial.
        
        Args:
            model_path: Ruta al modelo.
            vertices: Vértices del modelo.
            faces: Caras del modelo.
            textures: Texturas del modelo.
        """
        # Generar thumbnail
        thumbnail_path = model_path.with_suffix('.png')
        # Aquí se generaría un thumbnail real
        # Por ahora, copiamos el archivo
        shutil.copy(model_path, thumbnail_path)
        
        # Crear entrada de historial
        entry = {
            'name': model_path.stem,
            'model_path': str(model_path),
            'thumbnail_path': str(thumbnail_path),
            'created_at': datetime.now().isoformat(),
            'vertices_count': len(vertices),
            'faces_count': len(faces)
        }
        
        self.history.append(entry)
        self._save_history()
    
    def _load_history(self) -> List[Dict]:
        """Carga el historial desde el archivo."""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_history(self):
        """Guarda el historial en el archivo."""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def get_history(self) -> List[Dict]:
        """
        Obtiene el historial de proyectos.
        
        Returns:
            List[Dict]: Historial de proyectos.
        """
        return self.history
