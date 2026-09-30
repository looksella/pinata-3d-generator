import subprocess
import re
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class GPUDetector:
    """Detecta la presencia y características de GPUs NVIDIA."""
    
    @staticmethod
    def detect_gpu() -> Dict:
        """
        Detecta si hay una GPU NVIDIA disponible y devuelve información sobre ella.
        
        Returns:
            Dict: Información sobre la GPU detectada.
        """
        try:
            # Ejecutar nvidia-smi para obtener información de la GPU
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=name,memory.total,memory.free,driver_version', '--format=csv,noheader'],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parsear la salida
            gpu_info = result.stdout.strip().split(', ')
            if len(gpu_info) >= 4:
                gpu_name = gpu_info[0]
                total_memory = int(re.search(r'(\d+)', gpu_info[1]).group(1))
                free_memory = int(re.search(r'(\d+)', gpu_info[2]).group(1))
                driver_version = gpu_info[3]
                
                logger.info(f"GPU detectada: {gpu_name} con {total_memory} MiB de VRAM")
                
                return {
                    'available': True,
                    'name': gpu_name,
                    'total_memory_mb': total_memory,
                    'free_memory_mb': free_memory,
                    'driver_version': driver_version,
                    'recommended_model': GPUDetector._get_recommended_model(total_memory)
                }
            
        except (subprocess.SubprocessError, FileNotFoundError, IndexError) as e:
            logger.warning(f"No se pudo detectar GPU NVIDIA: {e}")
            
        return {
            'available': False,
            'name': None,
            'total_memory_mb': 0,
            'free_memory_mb': 0,
            'driver_version': None,
            'recommended_model': None
        }
    
    @staticmethod
    def _get_recommended_model(vram_mb: int) -> str:
        """
        Determina el modelo recomendado basado en la VRAM disponible.
        
        Args:
            vram_mb: Cantidad de VRAM en MiB.
            
        Returns:
            str: Nombre del modelo recomendado.
        """
        if vram_mb >= 12288:  # 12 GB o más
            return 'hunyuan3d-2'
        elif vram_mb >= 8192:  # 8-11 GB
            return 'unique3d'
        elif vram_mb >= 4096:  # 4-7 GB
            return 'tripoSR'
        else:
            return 'hybrid'  # Flujo híbrido para GPUs con poca VRAM o sin GPU
