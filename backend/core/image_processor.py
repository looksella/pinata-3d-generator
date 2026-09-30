import numpy as np
from PIL import Image
import rembg
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Procesa imágenes para preparación de generación 3D."""
    
    def __init__(self, max_size: int = 1024):
        """
        Inicializa el procesador de imágenes.
        
        Args:
            max_size: Tamaño máximo de la imagen en píxeles.
        """
        self.max_size = max_size
        self.session = rembg.new_session('birefnet-general')
    
    def process_image(self, image_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Procesa una imagen para generación 3D.
        
        Args:
            image_path: Ruta a la imagen de entrada.
            
        Returns:
            Tuple[np.ndarray, np.ndarray]: Imagen procesada y máscara.
        """
        # Cargar imagen
        image = Image.open(image_path)
        
        # Eliminar fondo
        image_no_bg = self._remove_background(image)
        
        # Recortar al sujeto principal
        image_cropped = self._crop_to_subject(image_no_bg)
        
        # Normalizar resolución
        image_normalized = self._normalize_resolution(image_cropped)
        
        # Generar máscara
        mask = self._generate_mask(image_normalized)
        
        return np.array(image_normalized), mask
    
    def _remove_background(self, image: Image.Image) -> Image.Image:
        """Elimina el fondo de la imagen usando BiRefNet."""
        logger.info("Eliminando fondo con BiRefNet...")
        result = rembg.remove(image, session=self.session)
        return result
    
    def _crop_to_subject(self, image: Image.Image) -> Image.Image:
        """Recorta la imagen al sujeto principal."""
        # Convertir a array numpy
        img_array = np.array(image)
        
        # Encontrar bounding box del contenido no transparente
        if img_array.shape[2] == 4:  # RGBA
            alpha = img_array[:, :, 3]
            rows = np.any(alpha > 0, axis=1)
            cols = np.any(alpha > 0, axis=0)
            rmin, rmax = np.where(rows)[0][[0, -1]]
            cmin, cmax = np.where(cols)[0][[0, -1]]
            
            # Añadir margen
            margin = 20
            rmin = max(0, rmin - margin)
            rmax = min(img_array.shape[0], rmax + margin)
            cmin = max(0, cmin - margin)
            cmax = min(img_array.shape[1], cmax + margin)
            
            # Recortar
            return image.crop((cmin, rmin, cmax, rmax))
        
        return image
    
    def _normalize_resolution(self, image: Image.Image) -> Image.Image:
        """Normaliza la resolución manteniendo la relación de aspecto."""
        width, height = image.size
        
        # Determinar nueva dimensión
        if width > height:
            new_width = self.max_size
            new_height = int(height * (self.max_size / width))
        else:
            new_height = self.max_size
            new_width = int(width * (self.max_size / height))
        
        # Redimensionar con alta calidad
        return image.resize((new_width, new_height), Image.LANCZOS)
    
    def _generate_mask(self, image: Image.Image) -> np.ndarray:
        """Genera una máscara binaria a partir del canal alpha."""
        img_array = np.array(image)
        
        if img_array.shape[2] == 4:  # RGBA
            mask = img_array[:, :, 3] > 0
        else:
            # Si no hay canal alpha, usar umbralización
            gray = np.array(image.convert('L'))
            mask = gray > 10
        
        return mask.astype(np.uint8) * 255
