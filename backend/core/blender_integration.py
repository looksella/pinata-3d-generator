import subprocess
import os
import tempfile
from typing import Dict, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class BlenderIntegration:
    """Integra el sistema con Blender para edición avanzada."""
    
    def __init__(self, blender_path: str = None):
        """
        Inicializa la integración con Blender.
        
        Args:
            blender_path: Ruta al ejecutable de Blender.
        """
        self.blender_path = blender_path or self._find_blender()
        self.scripts_dir = Path(__file__).parent.parent.parent / "blender_scripts"
    
    def _find_blender(self) -> str:
        """Busca la instalación de Blender en el sistema."""
        # Intentar rutas comunes
        common_paths = [
            "/usr/bin/blender",
            "/usr/local/bin/blender",
            "/Applications/Blender.app/Contents/MacOS/Blender",
            "C:\\Program Files\\Blender Foundation\\Blender\\blender.exe"
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        # Intentar encontrar en PATH
        try:
            result = subprocess.run(['which', 'blender'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        logger.warning("No se encontró Blender. Especifique la ruta manualmente.")
        return None
    
    def open_in_blender(
        self,
        model_path: str,
        pinata_type: str,
        materials: Dict,
        output_path: Optional[str] = None
    ) -> bool:
        """
        Abre un modelo en Blender con scripts preconfigurados.
        
        Args:
            model_path: Ruta al modelo 3D.
            pinata_type: Tipo de piñata.
            materials: Materiales seleccionados.
            output_path: Ruta de salida opcional.
            
        Returns:
            bool: True si se abrió correctamente.
        """
        if not self.blender_path:
            logger.error("Blender no está disponible.")
            return False
        
        # Crear script temporal
        script_content = self._generate_blender_script(pinata_type, materials, model_path, output_path)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(script_content)
            script_path = f.name
        
        try:
            # Ejecutar Blender con el script
            cmd = [self.blender_path, '--python', script_path]
            subprocess.Popen(cmd)
            
            logger.info("Blender iniciado correctamente.")
            return True
            
        except Exception as e:
            logger.error(f"Error al abrir Blender: {e}")
            return False
        finally:
            # Limpiar script temporal
            os.unlink(script_path)
    
    def export_model(
        self,
        model_path: str,
        output_path: str,
        format: str
    ) -> bool:
        """
        Exporta un modelo en el formato especificado usando Blender.
        
        Args:
            model_path: Ruta al modelo de entrada.
            output_path: Ruta de salida.
            format: Formato de exportación.
            
        Returns:
            bool: True si se exportó correctamente.
        """
        if not self.blender_path:
            logger.error("Blender no está disponible.")
            return False
        
        # Crear script temporal
        script_content = self._generate_export_script(model_path, output_path, format)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(script_content)
            script_path = f.name
        
        try:
            # Ejecutar Blender en modo headless
            cmd = [self.blender_path, '--background', '--python', script_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Modelo exportado correctamente: {output_path}")
                return True
            else:
                logger.error(f"Error al exportar modelo: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error al exportar modelo: {e}")
            return False
        finally:
            # Limpiar script temporal
            os.unlink(script_path)
    
    def _generate_blender_script(
        self,
        pinata_type: str,
        materials: Dict,
        model_path: str,
        output_path: Optional[str]
    ) -> str:
        """
        Genera un script de Python para Blender.
        
        Args:
            pinata_type: Tipo de piñata.
            materials: Materiales seleccionados.
            model_path: Ruta al modelo.
            output_path: Ruta de salida.
            
        Returns:
            str: Contenido del script.
        """
        script = f"""
import bpy
import bmesh
import os
import sys

# Importar modelo
bpy.ops.import_scene.gltf(filepath='{model_path}')

# Seleccionar objeto importado
obj = bpy.context.selected_objects[0]
bpy.context.view_layer.objects.active = obj

# Aplicar materiales de piñata
exec(open('{self.scripts_dir / "pinata_materials.py"}').read())

# Aplicar tipo de piñata
pinata_type = '{pinata_type}'
exec(open('{self.scripts_dir / "pinata_types.py"}').read())

# Generar flecos
exec(open('{self.scripts_dir / "fringe_generator.py"}').read())

# Configurar para impresión 3D
exec(open('{self.scripts_dir / "export_utils.py"}').read())

# Configurar materiales específicos
body_material = '{materials.get("body", "crepe")}'
fringe_material = '{materials.get("fringe", "corto")}'
finish_material = '{materials.get("finish", "mate")}'

apply_pinata_materials(obj, body_material, fringe_material, finish_material)
apply_pinata_type(obj, pinata_type)
generate_fringes(obj, fringe_material)

# Configurar escala para impresión 3D
setup_for_3d_printing(obj)

# Guardar si se especificó ruta de salida
if '{output_path}':
    bpy.ops.wm.save_as_mainfile(filepath='{output_path}')

print("Piñata cargada correctamente en Blender.")
"""
        return script
    
    def _generate_export_script(
        self,
        model_path: str,
        output_path: str,
        format: str
    ) -> str:
        """
        Genera un script de Python para exportar un modelo.
        
        Args:
            model_path: Ruta al modelo de entrada.
            output_path: Ruta de salida.
            format: Formato de exportación.
            
        Returns:
            str: Contenido del script.
        """
        script = f"""
import bpy
import os

# Limpiar escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Importar modelo
if '{format}' == 'glb' or '{format}' == 'gltf':
    bpy.ops.import_scene.gltf(filepath='{model_path}')
elif '{format}' == 'obj':
    bpy.ops.import_scene.obj(filepath='{model_path}')

# Seleccionar objeto importado
obj = bpy.context.selected_objects[0]
bpy.context.view_layer.objects.active = obj

# Aplicar transformaciones
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Exportar según el formato
if '{format}' == 'glb':
    bpy.ops.export_scene.gltf(
        filepath='{output_path}',
        export_format='GLB',
        export_texcoords=True,
        export_normals=True,
        export_materials='EXPORT',
        export_colors=True,
        export_apply=True
    )
elif '{format}' == 'gltf':
    bpy.ops.export_scene.gltf(
        filepath='{output_path}',
        export_format='GLTF_SEPARATE',
        export_texcoords=True,
        export_normals=True,
        export_materials='EXPORT',
        export_colors=True,
        export_apply=True
    )
elif '{format}' == 'obj':
    bpy.ops.export_scene.obj(
        filepath='{output_path}',
        export_materials=True,
        export_normals=True,
        export_uv=True,
        export_triangulated_mesh=True
    )
elif '{format}' == 'stl':
    bpy.ops.export_mesh.stl(
        filepath='{output_path}',
        ascii=False,
        use_mesh_modifiers=True
    )
elif '{format}' == '3mf':
    bpy.ops.export_mesh.threemf(
        filepath='{output_path}',
        use_mesh_modifiers=True
    )
elif '{format}' == 'usdz':
    bpy.ops.export_scene.usdz(
        filepath='{output_path}'
    )

print(f"Modelo exportado: {output_path}")
"""
        return script
