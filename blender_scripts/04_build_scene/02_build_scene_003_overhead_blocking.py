import bpy
import random
from mathutils import Vector
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

SEED = 303

COURTYARD_WIDTH = 12.0
COURTYARD_DEPTH = 9.0

PAVED_WIDTH = 8.8
PAVED_DEPTH = 6.4

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_FILE = (
    PROJECT_ROOT /
    "output/scenes_3d/scene_003_overhead_blocking.blend"
)

RENDER_FILE = (
    PROJECT_ROOT /
    "output/renders/scene_003_overhead_blocking.png"
)


# ============================================================
# UTILITAIRES
# ============================================================

def look_at(obj, target):
    direction = Vector(target) - obj.location

    obj.rotation_euler = (
        direction.to_track_quat(
            "-Z",
            "Y"
        ).to_euler()
    )


def clear_scene():
    bpy.ops.object.select_all(
        action="SELECT"
    )

    bpy.ops.object.delete(
        use_global=False
    )


def get_principled(material):
    return material.node_tree.nodes.get(
        "Principled BSDF"
    )


def add_bevel(obj, width=0.02):
    bevel = obj.modifiers.new(
        name="Edge_Bevel",
        type="BEVEL"
    )

    bevel.width = width
    bevel.segments = 2

    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.modifier_apply(
        modifier=bevel.name
    )


def add_cube(name, location, dimensions, material):
    bpy.ops.mesh.primitive_cube_add(
        location=location
    )

    obj = bpy.context.active_object
    obj.name = name

    obj.dimensions = dimensions

    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True
    )

    obj.data.materials.append(
        material
    )

    add_bevel(obj)

    return obj


# ============================================================
# MATÉRIAUX
# ============================================================

def create_material(name, color, roughness=0.8):
    material = bpy.data.materials.new(
        name=name
    )

    principled = get_principled(material)

    principled.inputs["Base Color"].default_value = (
        *color,
        1.0
    )

    principled.inputs["Roughness"].default_value = roughness

    material.diffuse_color = (
        *color,
        1.0
    )

    return material


# ============================================================
# COUR : TERRE / GRAVIER ET DALLES
# ============================================================

def create_courtyard_base():
    gravel = create_material(
        "Gravel_Ground",
        (0.19, 0.16, 0.13),
        roughness=1.0
    )

    base = add_cube(
        name="Courtyard_Gravel_Base",
        location=(0, 0, -0.14),
        dimensions=(
            COURTYARD_WIDTH,
            COURTYARD_DEPTH,
            0.25
        ),
        material=gravel
    )

    return base


def create_paving():
    random.seed(SEED)

    stone_materials = [
        create_material(
            "Paving_Stone_Light",
            (0.43, 0.40, 0.35),
            roughness=0.92
        ),
        create_material(
            "Paving_Stone_Mid",
            (0.34, 0.32, 0.28),
            roughness=0.94
        ),
        create_material(
            "Paving_Stone_Warm",
            (0.38, 0.34, 0.29),
            roughness=0.93
        ),
    ]

    stone_height = 0.13
    gap = 0.035

    front = -PAVED_DEPTH / 2
    back = PAVED_DEPTH / 2
    left = -PAVED_WIDTH / 2
    right = PAVED_WIDTH / 2

    y = front
    row_number = 0

    while y < back:
        row_depth = random.uniform(
            0.62,
            0.90
        )

        remaining_depth = back - y

        if remaining_depth < 0.32:
            break

        if row_depth > remaining_depth:
            row_depth = remaining_depth

        offset = 0.0

        if row_number % 2 == 1:
            offset = random.uniform(
                0.25,
                0.65
            )

        x = left + offset

        while x < right:
            stone_width = random.uniform(
                0.70,
                1.45
            )

            remaining_width = right - x

            if remaining_width < 0.35:
                break

            if stone_width > remaining_width:
                stone_width = remaining_width

            center_x = x + stone_width / 2
            center_y = y + row_depth / 2

            stone = add_cube(
                name="Courtyard_Paving_Stone",
                location=(
                    center_x,
                    center_y,
                    stone_height / 2
                ),
                dimensions=(
                    stone_width,
                    row_depth,
                    stone_height
                ),
                material=random.choice(
                    stone_materials
                )
            )

            stone.rotation_euler[0] = random.uniform(
                -0.012,
                0.012
            )

            stone.rotation_euler[1] = random.uniform(
                -0.012,
                0.012
            )

            stone.rotation_euler[2] = random.uniform(
                -0.035,
                0.035
            )

            x += stone_width + gap

        y += row_depth + gap
        row_number += 1


# ============================================================
# TABLE ET MOBILIER
# ============================================================

def create_wood_material():
    return create_material(
        "Weathered_Wood",
        (0.16, 0.075, 0.030),
        roughness=0.82
    )


def create_table(location, rotation_z=0):
    wood = create_wood_material()

    table_width = 2.45
    table_depth = 0.95
    table_height = 0.95
    top_thickness = 0.12

    tabletop = add_cube(
        name="Tabletop",
        location=(
            location[0],
            location[1],
            table_height - top_thickness / 2
        ),
        dimensions=(
            table_width,
            table_depth,
            top_thickness
        ),
        material=wood
    )

    tabletop.rotation_euler[2] = rotation_z

    leg_x = table_width / 2 - 0.16
    leg_y = table_depth / 2 - 0.14
    leg_height = table_height - top_thickness

    for x_sign in (-1, 1):
        for y_sign in (-1, 1):
            leg = add_cube(
                name="Table_Leg",
                location=(
                    location[0] +
                    x_sign * leg_x,
                    location[1] +
                    y_sign * leg_y,
                    leg_height / 2
                ),
                dimensions=(
                    0.13,
                    0.13,
                    leg_height
                ),
                material=wood
            )

            leg.rotation_euler[2] = rotation_z

    return tabletop


def create_small_table(location):
    wood = create_wood_material()

    top = add_cube(
        name="Small_Table_Top",
        location=(
            location[0],
            location[1],
            0.68
        ),
        dimensions=(1.15, 0.75, 0.10),
        material=wood
    )

    for x_sign in (-1, 1):
        for y_sign in (-1, 1):
            add_cube(
                name="Small_Table_Leg",
                location=(
                    location[0] +
                    x_sign * 0.44,
                    location[1] +
                    y_sign * 0.27,
                    0.33
                ),
                dimensions=(0.10, 0.10, 0.66),
                material=wood
            )

    return top


def create_stool(location):
    wood = create_wood_material()

    seat = add_cube(
        name="Stool_Seat",
        location=(
            location[0],
            location[1],
            0.48
        ),
        dimensions=(0.70, 0.45, 0.09),
        material=wood
    )

    for x_sign in (-1, 1):
        for y_sign in (-1, 1):
            add_cube(
                name="Stool_Leg",
                location=(
                    location[0] +
                    x_sign * 0.25,
                    location[1] +
                    y_sign * 0.14,
                    0.23
                ),
                dimensions=(0.08, 0.08, 0.46),
                material=wood
            )

    return seat


# ============================================================
# PROXIES DE PERSONNAGES
# ============================================================

def create_proxy_material(name, color):
    return create_material(
        name,
        color,
        roughness=0.72
    )


def create_standing_proxy(name, location, color, height=1.78):
    material = create_proxy_material(
        f"{name}_Material",
        color
    )

    body_height = height * 0.58
    body_radius = height * 0.13
    head_radius = height * 0.09

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=12,
        radius=body_radius,
        depth=body_height,
        location=(
            location[0],
            location[1],
            body_height / 2
        )
    )

    body = bpy.context.active_object
    body.name = f"{name}_Body"
    body.data.materials.append(material)

    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=12,
        ring_count=6,
        radius=head_radius,
        location=(
            location[0],
            location[1],
            body_height +
            head_radius
        )
    )

    head = bpy.context.active_object
    head.name = f"{name}_Head"
    head.data.materials.append(material)


def create_ground_proxy(name, location, color):
    material = create_proxy_material(
        f"{name}_Material",
        color
    )

    body = add_cube(
        name=f"{name}_Body",
        location=(
            location[0],
            location[1],
            0.18
        ),
        dimensions=(0.48, 1.55, 0.22),
        material=material
    )

    head = add_cube(
        name=f"{name}_Head",
        location=(
            location[0],
            location[1] + 0.72,
            0.25
        ),
        dimensions=(0.34, 0.34, 0.24),
        material=material
    )

    return body, head


def create_character_layout():
    guard_color = (0.18, 0.20, 0.24)
    observer_color = (0.24, 0.16, 0.10)
    central_color = (0.32, 0.18, 0.12)

    create_ground_proxy(
        "Central_Ground_Figure",
        (-0.7, -0.15),
        central_color
    )

    create_standing_proxy(
        "Guard_Left_01",
        (-2.00, 0.20),
        guard_color
    )

    create_standing_proxy(
        "Guard_Left_02",
        (-2.55, 1.65),
        guard_color
    )

    create_standing_proxy(
        "Guard_Top_01",
        (-0.35, 2.45),
        guard_color
    )

    create_standing_proxy(
        "Guard_Top_02",
        (1.30, 2.45),
        guard_color
    )

    create_standing_proxy(
        "Observer_Right_01",
        (2.75, 1.45),
        observer_color
    )

    create_standing_proxy(
        "Observer_Right_02",
        (3.35, 0.10),
        observer_color
    )

    print("✓ Proxies personnages : 7")


# ============================================================
# CAMÉRA ET LUMIÈRES
# ============================================================

def create_camera():
    bpy.ops.object.camera_add(
        location=(0.3, -1.3, 14.5)
    )

    camera = bpy.context.active_object
    camera.name = "Scene_003_Overhead_Camera"

    camera.data.lens = 52

    look_at(
        camera,
        (0, 0.25, 0)
    )

    bpy.context.scene.camera = camera


def create_lights():
    bpy.ops.object.light_add(
        type="AREA",
        location=(-3.0, -4.0, 10.0)
    )

    key_light = bpy.context.active_object
    key_light.name = "Diffuse_Daylight_Key"

    key_light.data.energy = 1800
    key_light.data.size = 8.0

    look_at(
        key_light,
        (0, 0, 0)
    )

    bpy.ops.object.light_add(
        type="AREA",
        location=(4.0, 3.0, 8.0)
    )

    fill_light = bpy.context.active_object
    fill_light.name = "Diffuse_Daylight_Fill"

    fill_light.data.energy = 700
    fill_light.data.size = 9.0

    look_at(
        fill_light,
        (0, 0, 0)
    )


# ============================================================
# RENDU ET SAUVEGARDE
# ============================================================

def configure_render():
    scene = bpy.context.scene

    scene.render.engine = "BLENDER_EEVEE"

    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100

    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(RENDER_FILE)

    scene.world.color = (
        0.025,
        0.022,
        0.020
    )


def save_file():
    bpy.ops.wm.save_as_mainfile(
        filepath=str(OUTPUT_FILE)
    )


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("🎬 CONSTRUCTION — SCÈNE 003 / PLONGÉE / BLOCKING")
    print("=" * 60)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    RENDER_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    clear_scene()

    create_courtyard_base()
    create_paving()

    create_table(
        location=(3.45, -0.35, 0),
        rotation_z=-0.12
    )

    create_small_table(
        location=(4.30, -1.35, 0)
    )

    create_stool(
        location=(4.20, -2.25, 0)
    )

    create_character_layout()

    create_camera()
    create_lights()
    configure_render()

    bpy.ops.render.render(
        write_still=True
    )

    save_file()

    print("=" * 60)
    print("✅ SCÈNE 003 — BLOCKING CRÉÉ")
    print(f"💾 Blender : {OUTPUT_FILE}")
    print(f"🖼️ Rendu   : {RENDER_FILE}")
    print("=" * 60)


main()