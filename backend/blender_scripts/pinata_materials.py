import bpy
import bmesh
from mathutils import Vector
import random

def apply_pinata_materials(obj, body_material='crepe', fringe_material='corto', finish_material='mate'):
    """
    Aplica materiales de piñata al objeto.
    
    Args:
        obj: Objeto de Blender.
        body_material: Material del cuerpo.
        fringe_material: Tipo de fleco.
        finish_material: Tipo de acabado.
    """
    # Limpiar materiales existentes
    obj.data.materials.clear()
    
    # Crear material del cuerpo
    body_mat = create_body_material(body_material, finish_material)
    obj.data.materials.append(body_mat)
    
    # Crear material de flecos
    fringe_mat = create_fringe_material(fringe_material, finish_material)
    obj.data.materials.append(fringe_mat)
    
    # Asignar materiales a las caras
    assign_materials_to_faces(obj, body_material, fringe_material)

def create_body_material(material_type, finish_type):
    """Crea un material para el cuerpo de la piñata."""
    mat = bpy.data.materials.new(name=f"Cuerpo_{material_type}_{finish_type}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Limpiar nodos existentes
    for node in nodes:
        nodes.remove(node)
    
    # Crear nodos
    output = nodes.new('ShaderNodeOutputMaterial')
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    noise = nodes.new('ShaderNodeTexNoise')
    bump = nodes.new('ShaderNodeBump')
    color_ramp = nodes.new('ShaderNodeValToRGB')
    
    # Configurar propiedades según el tipo de material
    if material_type == 'crepe':
        # Papel crepé - textura rugosa
        principled.inputs['Roughness'].default_value = 0.9
        principled.inputs['Specular'].default_value = 0.1
        noise.inputs['Scale'].default_value = 50.0
        noise.inputs['Detail'].default_value = 2.0
    elif material_type == 'cartulina':
        # Cartulina - más lisa
        principled.inputs['Roughness'].default_value = 0.7
        principled.inputs['Specular'].default_value = 0.2
        noise.inputs['Scale'].default_value = 20.0
        noise.inputs['Detail'].default_value = 1.0
    elif material_type == 'papel-seda':
        # Papel de seda - muy suave
        principled.inputs['Roughness'].default_value = 0.5
        principled.inputs['Specular'].default_value = 0.3
        noise.inputs['Scale'].default_value = 10.0
        noise.inputs['Detail'].default_value = 0.5
    elif material_type == 'papel-metalico':
        # Papel metálico - brillante
        principled.inputs['Roughness'].default_value = 0.2
        principled.inputs['Specular'].default_value = 0.8
        principled.inputs['Metallic'].default_value = 0.8
        noise.inputs['Scale'].default_value = 5.0
        noise.inputs['Detail'].default_value = 0.5
    
    # Configurar acabado
    if finish_type == 'mate':
        principled.inputs['Roughness'].default_value *= 1.2
    elif finish_type == 'brillante':
        principled.inputs['Roughness'].default_value *= 0.5
        principled.inputs['Clearcoat'].default_value = 0.5
    elif finish_type == 'metalico':
        principled.inputs['Metallic'].default_value = 0.8
    
    # Conectar nodos
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], principled.inputs['Normal'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Color base aleatorio vibrante
    colors = [
        (1.0, 0.2, 0.2, 1.0),  # Rojo
        (0.2, 0.8, 0.8, 1.0),  # Turquesa
        (1.0, 0.9, 0.2, 1.0),  # Amarillo
        (0.8, 0.2, 0.8, 1.0),  # Magenta
        (0.2, 0.8, 0.2, 1.0),  # Verde
    ]
    principled.inputs['Base Color'].default_value = random.choice(colors)
    
    return mat

def create_fringe_material(fringe_type, finish_type):
    """Crea un material para los flecos de la piñata."""
    mat = bpy.data.materials.new(name=f"Fleco_{fringe_type}_{finish_type}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Limpiar nodos existentes
    for node in nodes:
        nodes.remove(node)
    
    # Crear nodos
    output = nodes.new('ShaderNodeOutputMaterial')
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    wave = nodes.new('ShaderNodeTexWave')
    color_ramp = nodes.new('ShaderNodeValToRGB')
    
    # Configurar propiedades según el tipo de fleco
    if fringe_type == 'corto':
        wave.inputs['Scale'].default_value = 100.0
    elif fringe_type == 'medio':
        wave.inputs['Scale'].default_value = 50.0
    elif fringe_type == 'largo':
        wave.inputs['Scale'].default_value = 25.0
    elif fringe_type == 'doble':
        wave.inputs['Scale'].default_value = 75.0
    
    # Configurar color del fleco
    color_ramp.color_ramp.elements[0].color = (1.0, 0.3, 0.3, 1.0)  # Rojo
    color_ramp.color_ramp.elements[1].color = (1.0, 0.8, 0.2, 1.0)  # Amarillo
    
    # Conectar nodos
    links.new(wave.outputs['Color'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Configurar propiedades del material
    principled.inputs['Roughness'].default_value = 0.8
    principled.inputs['Specular'].default_value = 0.2
    
    return mat

def assign_materials_to_faces(obj, body_material, fringe_material):
    """Asigna materiales a las caras del objeto."""
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    # Asignar material del cuerpo a todas las caras
    for face in bm.faces:
        face.material_index = 0
    
    # Si hay flecos, asignar material de flecos a algunas caras
    if fringe_material:
        # Seleccionar caras para flecos (por ejemplo, las laterales)
        for face in bm.faces:
            normal = face.normal
            if abs(normal.x) > 0.5 or abs(normal.y) > 0.5:  # Caras laterales
                face.material_index = 1
    
    bm.to_mesh(mesh)
    bm.free()
