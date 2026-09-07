import bpy
import random
from mathutils import Vector
from pathlib import Path

# ============================================================
# CONFIGURATION - MUR FORTERESSE V3 (RÉALISME FINAL)
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "output/scenes_3d/asset_roman_fortress_wall.blend"

WALL_WIDTH = 18.0
WALL_HEIGHT = 8.0
GAP = 0.04 

SEED = 101
random.seed(SEED)

def create_displacement_texture():
    if "Stone_Disp" not in bpy.data.textures:
        tex = bpy.data.textures.new("Stone_Disp", type='CLOUDS')
        tex.noise_scale = 1.5
        tex.noise_depth = 2
    return bpy.data.textures["Stone_Disp"]

# ============================================================
# MATÉRIAUX
# ============================================================
def create_realistic_stone_material():
    mat = bpy.data.materials.new(name="Realistic_Ancient_Stone")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs['Roughness'].default_value = 0.9 
    
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 8.0
    noise.inputs['Detail'].default_value = 15.0
    
    obj_info = nodes.new(type='ShaderNodeObjectInfo')
    
    # Amplifier la variation aléatoire
    math_node = nodes.new(type='ShaderNodeMath')
    math_node.operation = 'MULTIPLY'
    math_node.inputs[1].default_value = 1.5
    
    mix_color = nodes.new(type='ShaderNodeMix')
    mix_color.data_type = 'FLOAT'
    mix_color.blend_type = 'LINEAR_LIGHT'
    mix_color.inputs[0].default_value = 0.8
    
    # Couleurs beaucoup plus contrastées (Gris sombre, Beige, Ocre)
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.color_ramp.elements[0].position = 0.1
    color_ramp.color_ramp.elements[0].color = (0.15, 0.14, 0.13, 1.0) # Gris sombre
    color_ramp.color_ramp.elements[1].position = 0.4
    color_ramp.color_ramp.elements[1].color = (0.45, 0.40, 0.35, 1.0) # Sable moyen
    color_ramp.color_ramp.elements.new(0.8)
    color_ramp.color_ramp.elements[2].color = (0.70, 0.60, 0.50, 1.0) # Ocre clair
    
    bump = nodes.new(type='ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.8
    bump.inputs['Distance'].default_value = 0.2
    
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    links.new(obj_info.outputs['Random'], math_node.inputs[0])
    links.new(noise.outputs['Fac'], mix_color.inputs[1])
    links.new(math_node.outputs['Value'], mix_color.inputs[2]) 
    
    links.new(mix_color.outputs[0], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
    
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], principled.inputs['Normal'])
    
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_mortar_material():
    mat = bpy.data.materials.new(name="Mortar_Backing")
    mat.use_nodes = True
    principled = mat.node_tree.nodes.get("Principled BSDF")
    principled.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1.0) # Presque noir
    principled.inputs['Roughness'].default_value = 1.0
    return mat

# ============================================================
# CONSTRUCTION GÉOMÉTRIQUE
# ============================================================
def add_stone_block(x, y, z, width, height, depth, material, disp_tex):
    bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
    stone = bpy.context.active_object
    stone.name = "Stone_Block"
    
    stone.dimensions = (width - GAP, depth - GAP, height - GAP)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    stone.data.materials.append(material)
    
    bevel = stone.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = random.uniform(0.04, 0.08)
    bevel.segments = 4
    
    remesh = stone.modifiers.new(name="Subsurf", type='SUBSURF')
    remesh.render_levels = 3
    remesh.levels = 3
    
    displace = stone.modifiers.new(name="Displace", type='DISPLACE')
    displace.texture = disp_tex
    displace.strength = random.uniform(0.08, 0.15)
    displace.texture_coords = 'LOCAL'
    
    stone.rotation_euler[0] = random.uniform(-0.02, 0.02)
    stone.rotation_euler[1] = random.uniform(-0.02, 0.02)
    stone.rotation_euler[2] = random.uniform(-0.02, 0.02)

def build_fortress_wall():
    stone_mat = create_realistic_stone_material()
    disp_tex = create_displacement_texture()
    
    # 1. Ajouter le "fond" du mur pour boucher les trous
    bpy.ops.mesh.primitive_cube_add(location=(0, 0.2, WALL_HEIGHT/2))
    backdrop = bpy.context.active_object
    backdrop.name = "Wall_Backdrop"
    backdrop.dimensions = (WALL_WIDTH, 0.1, WALL_HEIGHT)
    backdrop.data.materials.append(create_mortar_material())

    # 2. Construire les pierres
    z = 0.0
    row_idx = 0
    while z < WALL_HEIGHT:
        base_height = random.uniform(0.8, 1.2) if z < 3.0 else random.uniform(0.5, 0.8)
        x = -WALL_WIDTH / 2
        if row_idx % 2 == 1: x -= random.uniform(0.5, 1.5)
            
        while x < WALL_WIDTH / 2:
            stone_width = random.uniform(1.2, 2.5)
            if x + stone_width > WALL_WIDTH / 2: stone_width = (WALL_WIDTH / 2) - x
            if stone_width > 0.4:
                add_stone_block(x + stone_width/2, 0, z + base_height/2, stone_width, base_height, random.uniform(0.5, 0.7), stone_mat, disp_tex)
            x += stone_width
            
        z += base_height
        row_idx += 1

# ============================================================
# MISE EN SCÈNE
# ============================================================
def setup_presentation():
    bpy.ops.object.camera_add(location=(0, -12.0, 2.0), rotation=(1.65, 0, 0))
    bpy.context.scene.camera = bpy.context.active_object
    bpy.context.active_object.data.lens = 28 
    
    bpy.ops.object.light_add(type='SUN', location=(-10, -10, 8))
    sun = bpy.context.active_object
    sun.data.energy = 8.0
    sun.rotation_euler = (1.2, 0.0, -0.8)
    sun.data.angle = 0.05 
    
    bpy.context.scene.world.use_nodes = True
    bg_node = bpy.context.scene.world.node_tree.nodes.get("Background")
    bg_node.inputs[0].default_value = (0.2, 0.22, 0.25, 1.0)
    bg_node.inputs[1].default_value = 1.5
    
    # On reste sur CYCLES car EEVEE gère mal le "Displacement" physique par défaut.
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.filepath = str(PROJECT_ROOT / "output/renders/asset_roman_fortress_wall_v3.png")

def main():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    build_fortress_wall()
    setup_presentation()
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT_FILE))
    bpy.ops.render.render(write_still=True)
    print("✅ Asset V3 généré avec succès.")

main()