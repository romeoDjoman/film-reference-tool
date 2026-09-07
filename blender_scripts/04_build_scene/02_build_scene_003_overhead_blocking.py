import bpy
import random
from mathutils import Vector
from pathlib import Path

# ============================================================
# CONFIGURATION V3 - FILM MATCH
# ============================================================
SEED = 303
COURTYARD_WIDTH = 12.0
COURTYARD_DEPTH = 10.0

PAVED_WIDTH = 8.0
PAVED_DEPTH = 6.5

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "output/scenes_3d/scene_003_overhead_blocking.blend"
RENDER_FILE = PROJECT_ROOT / "output/renders/scene_003_overhead_blocking.png"

# ============================================================
# UTILITAIRES
# ============================================================
def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

def get_principled(material):
    return material.node_tree.nodes.get("Principled BSDF")

def add_bevel(obj, width=0.02):
    bevel = obj.modifiers.new(name="Edge_Bevel", type="BEVEL")
    bevel.width = width
    bevel.segments = 2
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=bevel.name)

def add_cube(name, location, dimensions, material):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    add_bevel(obj)
    return obj

# ============================================================
# MATÉRIAUX
# ============================================================
def create_material(name, color, roughness=0.8):
    material = bpy.data.materials.new(name=name)
    principled = get_principled(material)
    principled.inputs["Base Color"].default_value = (*color, 1.0)
    principled.inputs["Roughness"].default_value = roughness
    material.diffuse_color = (*color, 1.0)
    return material

# ============================================================
# COUR ET PAVAGE
# ============================================================
def create_courtyard_base():
    gravel = create_material("Gravel_Ground", (0.19, 0.16, 0.13), roughness=1.0)
    return add_cube("Courtyard_Gravel_Base", (0, 0, -0.14), (COURTYARD_WIDTH, COURTYARD_DEPTH, 0.25), gravel)

def create_paving():
    random.seed(SEED)
    stone_materials = [
        create_material("Paving_Stone_Light", (0.43, 0.40, 0.35), 0.92),
        create_material("Paving_Stone_Mid", (0.34, 0.32, 0.28), 0.94),
        create_material("Paving_Stone_Warm", (0.38, 0.34, 0.29), 0.93),
    ]
    
    stone_height = 0.13
    gap_base = 0.04
    
    front, back = -PAVED_DEPTH / 2, PAVED_DEPTH / 2
    left, right = -PAVED_WIDTH / 2, PAVED_WIDTH / 2
    
    y = front
    row_number = 0
    
    while y < back:
        row_depth = random.uniform(0.5, 0.9)
        if back - y < 0.32: break
        if row_depth > back - y: row_depth = back - y
            
        offset = 0.0 if row_number % 2 == 0 else random.uniform(0.2, 0.6)
        x = left + offset
        
        while x < right:
            stone_width = random.uniform(0.60, 1.3)
            if right - x < 0.35: break
            if stone_width > right - x: stone_width = right - x
                
            # Écrêter les angles pour un effet "scène ronde" au centre
            dist_to_center = (x**2 + y**2)**0.5
            if dist_to_center < PAVED_WIDTH / 2.2 and random.random() > 0.05:
                stone = add_cube(
                    "Courtyard_Paving_Stone",
                    (x + stone_width / 2, y + row_depth / 2, stone_height / 2),
                    (stone_width - gap_base, row_depth - gap_base, stone_height),
                    random.choice(stone_materials)
                )
                stone.rotation_euler[2] = random.uniform(-0.04, 0.04)
            x += stone_width
        y += row_depth
        row_number += 1

# ============================================================
# ACCESSOIRES ET MOBILIER
# ============================================================
def create_pillar():
    mat = create_material("Stone_Pillar", (0.35, 0.35, 0.32), 0.9)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.35, depth=0.75, location=(-1.0, 0.0, 0.375))
    obj = bpy.context.active_object
    obj.name = "Whipping_Pillar"
    obj.data.materials.append(mat)
    add_bevel(obj, 0.03)

def create_wood_material():
    return create_material("Weathered_Wood", (0.16, 0.075, 0.030), 0.82)

def create_table_props(table_x, table_y, table_z):
    prop_mat = create_material("Clay_Props", (0.4, 0.3, 0.2))
    # Cruche
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.35, location=(table_x - 0.5, table_y + 0.1, table_z + 0.175))
    bpy.context.active_object.data.materials.append(prop_mat)
    # Gobelets / Parchemins
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.15, location=(table_x - 0.1, table_y - 0.2, table_z + 0.075))
    bpy.context.active_object.data.materials.append(prop_mat)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.4, location=(table_x + 0.6, table_y, table_z + 0.025))
    bpy.context.active_object.rotation_euler[1] = 1.57 # Couché
    bpy.context.active_object.data.materials.append(prop_mat)

def create_table(location, rotation_z=0):
    wood = create_wood_material()
    table_width, table_depth, table_height, top_thickness = 2.45, 0.95, 0.95, 0.12
    tabletop = add_cube("Tabletop", (location[0], location[1], table_height - top_thickness / 2), (table_width, table_depth, top_thickness), wood)
    tabletop.rotation_euler[2] = rotation_z
    leg_x, leg_y = table_width / 2 - 0.16, table_depth / 2 - 0.14
    leg_height = table_height - top_thickness
    for x_sign in (-1, 1):
        for y_sign in (-1, 1):
            leg = add_cube("Table_Leg", (location[0] + x_sign * leg_x, location[1] + y_sign * leg_y, leg_height / 2), (0.13, 0.13, leg_height), wood)
            leg.rotation_euler[2] = rotation_z
    
    # Ajouter les accessoires sur la table
    create_table_props(location[0], location[1], table_height)

# ============================================================
# PROXIES PERSONNAGES (BASÉS SUR LE FILM)
# ============================================================
def create_proxy_material(name, color):
    return create_material(name, color, roughness=0.72)

def create_standing_proxy(name, location, color, height=1.78):
    material = create_proxy_material(f"{name}_Material", color)
    body_height, body_radius, head_radius = height * 0.58, height * 0.13, height * 0.09
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=body_radius, depth=body_height, location=(location[0], location[1], body_height / 2))
    body = bpy.context.active_object
    body.name = f"{name}_Body"
    body.data.materials.append(material)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=head_radius, location=(location[0], location[1], body_height + head_radius))
    bpy.context.active_object.data.materials.append(material)

def create_ground_proxy(name, location, color):
    material = create_proxy_material(f"{name}_Material", color)
    add_cube(f"{name}_Body", (location[0], location[1], 0.15), (1.55, 0.48, 0.22), material)
    add_cube(f"{name}_Head", (location[0] - 0.72, location[1], 0.18), (0.34, 0.34, 0.24), material)

def create_character_layout():
    guard_color = (0.35, 0.20, 0.20) # Manteaux rouges romains
    torturer_color = (0.50, 0.40, 0.30)
    jesus_color = (0.80, 0.70, 0.60) # Pâle/Nu
    officer_color = (0.2, 0.2, 0.25)
    
    # Centre : Le Prisonnier attaché au pilier (-1.0, 0.0)
    create_ground_proxy("Prisoner", (-1.8, 0.0), jesus_color) # Couché à gauche du pilier
    
    # Centre : Les deux bourreaux
    create_standing_proxy("Torturer_1", (-0.2, 0.8), torturer_color)
    create_standing_proxy("Torturer_2", (-0.3, -1.0), torturer_color)
    
    # Droite : Officier près de la table
    create_standing_proxy("Officer_Abenader", (2.8, 0.5), officer_color)
    
    # Arrière-plan : Arc de cercle des gardes romains
    create_standing_proxy("Guard_1", (-3.5, 2.8), guard_color)
    create_standing_proxy("Guard_2", (-1.5, 3.2), guard_color)
    create_standing_proxy("Guard_3", (0.5, 3.4), guard_color)
    create_standing_proxy("Guard_4", (2.5, 3.0), guard_color)

# ============================================================
# CAMÉRA ET LUMIÈRES
# ============================================================
def create_camera():
    # Placée en hauteur, légèrement inclinée pour voir toute la cour
    bpy.ops.object.camera_add(location=(0.0, -3.5, 15.0))
    camera = bpy.context.active_object
    camera.name = "Scene_003_Overhead_Camera"
    camera.data.lens = 35 # Focale large
    look_at(camera, (0, 0, 0)) # Regarde le centre de la scène
    bpy.context.scene.camera = camera

def create_lights():
    bpy.ops.object.light_add(type="AREA", location=(-5.0, -5.0, 12.0))
    key_light = bpy.context.active_object
    key_light.data.energy = 2500
    key_light.data.size = 15.0
    look_at(key_light, (0, 0, 0))
    
    bpy.ops.object.light_add(type="AREA", location=(5.0, 5.0, 10.0))
    fill_light = bpy.context.active_object
    fill_light.data.energy = 1000
    fill_light.data.size = 20.0
    look_at(fill_light, (0, 0, 0))

# ============================================================
# RENDU ET MAIN
# ============================================================
def main():
    print("=" * 60)
    print(" 🎬 CONSTRUCTION — SCÈNE 003 / PLONGÉE / BLOCKING V3 (FILM MATCH)")
    print("=" * 60)
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    clear_scene()
    
    create_courtyard_base()
    create_paving()
    create_pillar() # Le fameux pilier !
    
    create_table(location=(3.8, -0.5, 0), rotation_z=-0.1)
    create_character_layout()
    create_camera()
    create_lights()
    
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x, scene.render.resolution_y = 1280, 720
    scene.render.filepath = str(RENDER_FILE)
    scene.world.color = (0.04, 0.04, 0.04) # Ciel nuageux gris
    
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT_FILE))
    bpy.ops.render.render(write_still=True)
    print("✅ V3 MATCH TERMINÉE")

main()