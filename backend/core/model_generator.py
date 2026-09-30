import os
import torch
import numpy as np
from typing import Dict, Optional, Tuple
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ModelGenerator:
    """Genera modelos 3D a partir de imágenes procesadas."""
    
    def __init__(self, gpu_info: Dict):
        """
        Inicializa el generador de modelos.
        
        Args:
            gpu_info: Información sobre la GPU disponible.
        """
        self.gpu_info = gpu_info
        self.device = torch.device('cuda' if gpu_info['available'] else 'cpu')
        self.model = None
        
        # Cargar el modelo apropiado según la VRAM
        self._load_model()
    
    def _load_model(self):
        """Carga el modelo apropiado según la VRAM disponible."""
        recommended_model = self.gpu_info.get('recommended_model', 'hybrid')
        
        logger.info(f"Cargando modelo: {recommended_model}")
        
        if recommended_model == 'hunyuan3d-2':
            from models.hunyuan3d import Hunyuan3D
            self.model = Hunyuan3D(device=self.device)
        elif recommended_model == 'unique3d':
            from models.unique3d import Unique3D
            self.model = Unique3D(device=self.device)
        elif recommended_model == 'tripoSR':
            from models.tripoSR import TripoSR
            self.model = TripoSR(device=self.device)
        else:
            # Flujo híbrido - no se carga modelo local
            self.model = None
    
    def generate_model(
        self,
        image: np.ndarray,
        mask: np.ndarray,
        pinata_type: str,
        style_mode: str,
        progress_callback=None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera un modelo 3D a partir de una imagen procesada.
        
        Args:
            image: Imagen procesada.
            mask: Máscara del sujeto.
            pinata_type: Tipo de piñata seleccionado.
            style_mode: Modo de estilo seleccionado.
            progress_callback: Función para reportar progreso.
            
        Returns:
            Tuple[np.ndarray, np.ndarray]: Malla 3D y texturas.
        """
        if self.model is None:
            raise ValueError("No hay modelo local disponible. Use el flujo híbrido.")
        
        # Reportar progreso inicial
        if progress_callback:
            progress_callback(0, "Iniciando generación de modelo 3D...")
        
        # Generar modelo base
        if progress_callback:
            progress_callback(10, "Generando geometría base...")
        
        vertices, faces = self.model.generate_geometry(image, mask)
        
        # Adaptar geometría según el tipo de piñata
        if progress_callback:
            progress_callback(40, f"Adaptando geometría para tipo: {pinata_type}...")
        
        vertices, faces = self._adapt_to_pinata_type(vertices, faces, pinata_type)
        
        # Generar texturas
        if progress_callback:
            progress_callback(60, "Generando texturas...")
        
        textures = self.model.generate_textures(image, vertices, faces)
        
        # Aplicar estilo
        if progress_callback:
            progress_callback(80, f"Aplicando estilo: {style_mode}...")
        
        vertices, faces, textures = self._apply_style(vertices, faces, textures, style_mode)
        
        # Finalizar
        if progress_callback:
            progress_callback(100, "Modelo 3D generado correctamente.")
        
        return vertices, faces, textures
    
    def _adapt_to_pinata_type(
        self,
        vertices: np.ndarray,
        faces: np.ndarray,
        pinata_type: str
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Adapta la geometría según el tipo de piñata seleccionado.
        
        Args:
            vertices: Vértices del modelo.
            faces: Caras del modelo.
            pinata_type: Tipo de piñata.
            
        Returns:
            Tuple[np.ndarray, np.ndarray]: Vértices y caras adaptados.
        """
        if pinata_type == 'tambor':
            # Aplanar el modelo para crear silueta
            vertices[:, 2] *= 0.2  # Reducir profundidad
            
        elif pinata_type == 'tambor-alto-relieve':
            # Mantener forma base pero aumentar relieve en detalles
            vertices[:, 2] *= 0.5  # Reducir profundidad base
            
        elif pinata_type == 'rostro':
            # Aplanar la parte trasera
            z_mean = np.mean(vertices[:, 2])
            mask_back = vertices[:, 2] < z_mean
            vertices[mask_back, 2] = z_mean - 0.1
            
        elif pinata_type == 'globo-estallido':
            # Inflar el modelo
            center = np.mean(vertices, axis=0)
            directions = vertices - center
            distances = np.linalg.norm(directions, axis=1)
            vertices = center + directions * (1.2 * distances / np.max(distances))
        
        # Para 'escultura-3d' y 'tira-listones', mantener la geometría original
        
        return vertices, faces
    
    def _apply_style(
        self,
        vertices: np.ndarray,
        faces: np.ndarray,
        textures: np.ndarray,
        style_mode: str
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Aplica el estilo seleccionado al modelo.
        
        Args:
            vertices: Vértices del modelo.
            faces: Caras del modelo.
            textures: Texturas del modelo.
            style_mode: Modo de estilo.
            
        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray]: Modelo estilizado.
        """
        if style_mode == 'tradicional':
            # Simplificar geometría para un look más tradicional
            # Aumentar saturación de colores
            textures = self._enhance_colors(textures, saturation=1.5)
            
        # Para 'fiel', mantener el modelo original
        
        return vertices, faces, textures
    
    def _enhance_colors(self, textures: np.ndarray, saturation: float = 1.5) -> np.ndarray:
        """Aumenta la saturación de las texturas."""
        # Implementación simplificada
        return textures
