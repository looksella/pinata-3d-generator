import bpy
import bmesh
from mathutils import Vector
import os

def setup_for_3d_printing(obj):
    """
    Configura el modelo para impresión 3D.
    
    Args:
        obj: Objeto de Blender.
    """
    # Seleccionar el objeto
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    # Aplicar transformaciones
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
    # Añadir modificador de remesh para asegurar malla manifold
    remesh_modifier = obj.modifiers.new(name="Remesh", type='REMESH')
    remesh_modifier.voxel_size = 0.01
    remesh_modifier.adaptivity = 0.001
    
    # Aplicar modificador
    bpy.ops.object.modifier_apply(modifier="Remesh")
    
    # Reparar geometría
    repair_mesh(obj)
    
    # Centrar el pivote en la base
    center_pivot_at_base(obj)
    
    # Escalar a tamaño real (en cm)
    scale_to_real_size(obj, target_height_cm=30)
    
    print("Modelo configurado para impresión 3D.")

def repair_mesh(obj):
    """Repara la malla para asegurar que es manifold."""
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    # Eliminar caras duplicadas
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
    
    # Rellenar agujeros
    bmesh.ops.holes_fill(bm, edges=bm.edges)
    
    # Recalcular normales
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    
    # Hacer manifold
    bmesh.ops.make_manifold(bm, faces=bm.faces)
    
    bm.to_mesh(mesh)
    bm.free()

def center_pivot_at_base(obj):
    """Centra el pivote en la base del modelo."""
    mesh = obj.data
    
    # Encontrar el punto más bajo
    min_z = min(v.co.z for v in mesh.vertices)
    
    # Mover el origen a la base
    bpy.context.scene.cursor.location = (0, 0, min_z)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    
    # Mover el objeto al origen
    obj.location = (0, 0, 0)

def scale_to_real_size(obj, target_height_cm=30):
    """Escala el modelo a un tamaño real en centímetros."""
    mesh = obj.data
    
    # Calcular altura actual
    min_z = min(v.co.z for v in mesh.vertices)
    max_z = max(v.co.z for v in mesh.vertices)
    current_height = max_z - min_z
    
    # Calcular factor de escala
    scale_factor = (target_height_cm / 100) / current_height  # Convertir cm a metros
    
    # Aplicar escala
    obj.scale = (scale_factor, scale_factor, scale_factor)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

def export_model(obj, output_path, format='glb'):
    """
    Exporta el modelo en el formato especificado.
    
    Args:
        obj: Objeto de Blender.
        output_path: Ruta de salida.
        format: Formato de exportación.
    """
    # Seleccionar el objeto
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    # Exportar según el formato
    if format == 'glb':
        bpy.ops.export_scene.gltf(
            filepath=output_path,
            export_format='GLB',
            export_texcoords=True,
            export_normals=True,
            export_materials='EXPORT',
            export_colors=True,
            export_cameras=False,
            export_lights=False,
            export_apply=True
        )
    elif format == 'gltf':
        bpy.ops.export_scene.gltf(
            filepath=output_path,
            export_format='GLTF_SEPARATE',
            export_texcoords=True,
            export_normals=True,
            export_materials='EXPORT',
            export_colors=True,
            export_cameras=False,
            export_lights=False,
            export_apply=True
        )
    elif format == 'obj':
        bpy.ops.export_scene.obj(
            filepath=output_path,
            export_materials=True,
            export_normals=True,
            export_uv=True,
            export_triangulated_mesh=True
        )
    elif format == 'stl':
        bpy.ops.export_mesh.stl(
            filepath=output_path,
            ascii=False,
            use_mesh_modifiers=True
        )
    elif format == '3mf':
        bpy.ops.export_mesh.threemf(
            filepath=output_path,
            use_mesh_modifiers=True
        )
    elif format == 'usdz':
        bpy.ops.export_scene.usdz(
            filepath=output_path
        )
    
    print(f"Modelo exportado como {format.upper()}: {output_path}")
