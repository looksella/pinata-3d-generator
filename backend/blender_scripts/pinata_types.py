import bpy
import bmesh
from mathutils import Vector, Matrix
import math

def apply_pinata_type(obj, pinata_type):
    """
    Aplica el tipo de piñata seleccionado al modelo.
    
    Args:
        obj: Objeto de Blender.
        pinata_type: Tipo de piñata.
    """
    if pinata_type == 'tambor':
        apply_tambor_style(obj)
    elif pinata_type == 'tambor-alto-relieve':
        apply_tambor_alto_relieve_style(obj)
    elif pinata_type == 'escultura-3d':
        apply_escultura_3d_style(obj)
    elif pinata_type == 'rostro':
        apply_rostro_style(obj)
    elif pinata_type == 'tira-listones':
        apply_tira_listones_style(obj)
    elif pinata_type == 'globo-estallido':
        apply_globo_estallido_style(obj)

def apply_tambor_style(obj):
    """Aplica estilo de piñata de tambor (silueta plana)."""
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    # Aplanar el modelo
    for v in bm.verts:
        v.co.z *= 0.2
    
    bm.to_mesh(mesh)
    bm.free()
    
    # Añadir soporte para colgar
    add_hanging_support(obj)

def apply_tambor_alto_relieve_style(obj):
    """Aplica estilo de piñata de tambor con alto relieve."""
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    # Reducir profundidad base pero mantener relieve
    for v in bm.verts:
        if v.co.z > 0:
            v.co.z *= 0.5
        else:
            v.co.z *= 0.3
    
    bm.to_mesh(mesh)
    bm.free()
    
    # Añadir soporte para colgar
    add_hanging_support(obj)

def apply_escultura_3d_style(obj):
    """Aplica estilo de piñata escultura 3D completa."""
    # Mantener geometría original
    # Añadir soporte para colgar
    add_hanging_support(obj)

def apply_rostro_style(obj):
    """Aplica estilo de piñata de rostro (tipo espejo)."""
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    # Aplanar la parte trasera
    z_mean = sum(v.co.z for v in bm.verts) / len(bm.verts)
    
    for v in bm.verts:
        if v.co.z < z_mean:
            v.co.z = z_mean - 0.1
    
    bm.to_mesh(mesh)
    bm.free()
    
    # Añadir soporte para colgar
    add_hanging_support(obj)

def apply_tira_listones_style(obj):
    """Aplica estilo de piñata de tira o listones."""
    # Crear base con apertura para listones
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    # Dividir el modelo en la parte inferior
    z_min = min(v.co.z for v in bm.verts)
    z_max = max(v.co.z for v in bm.verts)
    z_threshold = z_min + (z_max - z_min) * 0.3
    
    # Crear listones virtuales
    for i in range(6):
        angle = (i / 6) * 2 * math.pi
        # Marcar caras para listones
        for face in bm.faces:
            center = face.calc_center_median()
            if center.z < z_threshold:
                # Verificar si la cara está en el sector del listón
                face_angle = math.atan2(center.y, center.x)
                if abs(face_angle - angle) < math.pi / 6:
                    face.material_index = 2  # Material de listón
    
    bm.to_mesh(mesh)
    bm.free()
    
    # Añadir soporte para colgar
    add_hanging_support(obj)

def apply_globo_estallido_style(obj):
    """Aplica estilo de piñata de globo (estallido)."""
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    # Inflar el modelo
    center = Vector((0, 0, 0))
    for v in bm.verts:
        direction = v.co - center
        distance = direction.length
        if distance > 0:
            v.co = center + direction * (1.2 * distance)
    
    # Crear líneas de estallido
    for i in range(8):
        angle = (i / 8) * 2 * math.pi
        # Marcar caras para líneas de estallido
        for face in bm.faces:
            center = face.calc_center_median()
            face_angle = math.atan2(center.y, center.x)
            if abs(face_angle - angle) < math.pi / 16:
                face.material_index = 3  # Material de estallido
    
    bm.to_mesh(mesh)
    bm.free()
    
    # Añadir soporte para colgar
    add_hanging_support(obj)

def add_hanging_support(obj):
    """Añade un soporte para colgar la piñata."""
    # Crear un pequeño cilindro en la parte superior
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.02,
        depth=0.1,
        location=(0, 0, max(v.co.z for v in obj.data.vertices) + 0.05)
    )
    support = bpy.context.active_object
    support.name = "Soporte_Colgar"
    
    # Parentar al objeto principal
    support.parent = obj
