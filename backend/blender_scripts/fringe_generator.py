import bpy
import bmesh
from mathutils import Vector, Matrix
import math
import random

def generate_fringes(obj, fringe_type='corto', density=0.5):
    """
    Genera flecos tridimensionales en la piñata.
    
    Args:
        obj: Objeto de Blender.
        fringe_type: Tipo de fleco.
        density: Densidad de flecos (0-1).
    """
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    # Determinar longitud del fleco según el tipo
    if fringe_type == 'corto':
        fringe_length = 0.05
    elif fringe_type == 'medio':
        fringe_length = 0.1
    elif fringe_type == 'largo':
        fringe_length = 0.2
    elif fringe_type == 'doble':
        fringe_length = 0.15
    else:
        fringe_length = 0.1
    
    # Crear flecos en las caras laterales
    fringe_count = 0
    max_fringes = int(len(bm.faces) * density)
    
    for face in bm.faces:
        if fringe_count >= max_fringes:
            break
        
        normal = face.normal
        # Solo generar flecos en caras laterales
        if abs(normal.z) < 0.7:
            center = face.calc_center_median()
            
            # Crear fleco
            fringe_obj = create_fringe(center, normal, fringe_length, fringe_type)
            fringe_obj.parent = obj
            
            fringe_count += 1
    
    bm.to_mesh(mesh)
    bm.free()
    
    print(f"Generados {fringe_count} flecos de tipo {fringe_type}.")

def create_fringe(location, normal, length, fringe_type):
    """
    Crea un fleco individual.
    
    Args:
        location: Posición del fleco.
        normal: Normal de la superficie.
        length: Longitud del fleco.
        fringe_type: Tipo de fleco.
        
    Returns:
        bpy.types.Object: Objeto del fleco.
    """
    # Crear plano para el fleco
    bpy.ops.mesh.primitive_plane_add(size=0.02, location=location)
    fringe = bpy.context.active_object
    
    # Orientar el fleco según la normal
    # Rotar para que cuelgue hacia abajo
    rotation_euler = (
        math.pi / 2 + normal.x * 0.3,  # Inclinación X
        normal.y * 0.3,  # Inclinación Y
        math.atan2(normal.y, normal.x)  # Rotación Z
    )
    fringe.rotation_euler = rotation_euler
    
    # Aplicar transformaciones
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    
    # Añadir modificador de subdivide para más detalle
    modifier = fringe.modifiers.new(name="Subdivide", type='SUBSURF')
    modifier.levels = 1
    modifier.render_levels = 2
    
    # Añadir modificador de deformación para simular papel
    if fringe_type == 'corto':
        # Fleco corto - poca deformación
        pass
    elif fringe_type == 'medio':
        # Fleco medio - deformación moderada
        add_wave_deformation(fringe, amplitude=0.01, frequency=5)
    elif fringe_type == 'largo':
        # Fleco largo - mucha deformación
        add_wave_deformation(fringe, amplitude=0.02, frequency=3)
    elif fringe_type == 'doble':
        # Fleco doble - dos capas
        add_wave_deformation(fringe, amplitude=0.015, frequency=4)
        # Crear segunda capa
        fringe2 = fringe.copy()
        fringe2.data = fringe.data.copy()
        fringe2.location.z -= 0.01
        bpy.context.collection.objects.link(fringe2)
    
    # Aplicar material de fleco
    if len(fringe.data.materials) == 0:
        fringe.data.materials.append(bpy.data.materials.get(f"Fleco_{fringe_type}_mate"))
    
    # Escalar el fleco según la longitud
    fringe.scale = (1, 1, length / 0.02)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Nombre del objeto
    fringe.name = f"Fleco_{fringe_type}_{random.randint(1000, 9999)}"
    
    return fringe

def add_wave_deformation(obj, amplitude=0.01, frequency=5):
    """Añade deformación de onda al objeto."""
    # Crear vacío para el modificador
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=obj.location)
    empty = bpy.context.active_object
    empty.name = f"Wave_Control_{random.randint(1000, 9999)}"
    
    # Añadir modificador de onda
    modifier = obj.modifiers.new(name="Wave", type='WAVE')
    modifier.height = amplitude
    modifier.width = 1 / frequency
    modifier.narrowness = 1.5
    modifier.time = random.uniform(0, 1)
    
    # Parentar vacío al objeto
    empty.parent = obj
