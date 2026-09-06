import bpy
import random
from mathutils import Vector
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

PAVING_WIDTH = 8.0
PAVING_DEPTH = 8.0

STONE_WIDTH = 0.85
STONE_DEPTH = 0.60
STONE_HEIGHT = 0.16

GAP = 0.035
EDGE_BEVEL = 0.025

SEED = 84

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_FILE = (
    PROJECT_ROOT /
    "assets/generated/roman_paving.blend"
)

RENDER_FILE = (
    PROJECT_ROOT /
    "output/renders/roman_paving.png"
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


# ============================================================
# MATÉRIAUX
# ============================================================

def create_paving_material():
    material = bpy.data.materials.new(
        name="Roman_Paving_Stone"
    )

    principled = get_principled(material)

    principled.inputs["Base Color"].default_value = (
        0.19,
        0.15,
        0.11,
        1.0
    )

    principled.inputs["Roughness"].default_value = 0.92

    material.diffuse_color = (
        0.19,
        0.15,
        0.11,
        1.0
    )

    return material


def create_base_material():
    material = bpy.data.materials.new(
        name="Ground_Base"
    )

    principled = get_principled(material)

    principled.inputs["Base Color"].default_value = (
        0.045,
        0.035,
        0.025,
        1.0
    )

    principled.inputs["Roughness"].default_value = 1.0

    material.diffuse_color = (
        0.045,
        0.035,
        0.025,
        1.0
    )

    return material


# ============================================================
# PIERRES DU PAVAGE
# ============================================================

def add_bevel(stone):
    bevel = stone.modifiers.new(
        name="Paving_Edge_Bevel",
        type="BEVEL"
    )

    bevel.width = EDGE_BEVEL
    bevel.segments = 2

    bpy.context.view_layer.objects.active = stone

    bpy.ops.object.modifier_apply(
        modifier=bevel.name
    )


def create_paving_stone(location, dimensions, material):
    bpy.ops.mesh.primitive_cube_add(
        location=location
    )

    stone = bpy.context.active_object
    stone.name = "Paving_Stone"

    stone.dimensions = dimensions

    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True
    )

    stone.data.materials.append(
        material
    )

    add_bevel(stone)

    return stone


def generate_paving():
    random.seed(SEED)

    material = create_paving_material()

    front = -PAVING_DEPTH / 2
    back = PAVING_DEPTH / 2
    left = -PAVING_WIDTH / 2
    right = PAVING_WIDTH / 2

    y = front

    row_number = 0

    while y < back:
        row_depth = STONE_DEPTH * random.uniform(
            0.84,
            1.16
        )

        remaining_depth = back - y

        if remaining_depth < STONE_DEPTH * 0.45:
            break

        if row_depth > remaining_depth:
            row_depth = remaining_depth

        offset = 0.0

        if row_number % 2 == 1:
            offset = STONE_WIDTH * 0.5

        x = left + offset

        while x < right:
            stone_width = STONE_WIDTH * random.uniform(
                0.80,
                1.20
            )

            remaining_width = right - x

            if remaining_width < STONE_WIDTH * 0.45:
                break

            if stone_width > remaining_width:
                stone_width = remaining_width

            stone_height = STONE_HEIGHT * random.uniform(
                0.82,
                1.18
            )

            jitter_x = random.uniform(
                -0.012,
                0.012
            )

            jitter_y = random.uniform(
                -0.012,
                0.012
            )

            jitter_z = random.uniform(
                -0.008,
                0.008
            )

            center_x = x + stone_width / 2
            center_y = y + row_depth / 2

            # Évite les débordements du contour.
            if center_x - stone_width / 2 <= left + 0.05:
                jitter_x = 0.0

            if center_x + stone_width / 2 >= right - 0.05:
                jitter_x = 0.0

            if center_y - row_depth / 2 <= front + 0.05:
                jitter_y = 0.0

            if center_y + row_depth / 2 >= back - 0.05:
                jitter_y = 0.0

            stone = create_paving_stone(
                location=(
                    center_x + jitter_x,
                    center_y + jitter_y,
                    stone_height / 2 + jitter_z
                ),
                dimensions=(
                    stone_width,
                    row_depth,
                    stone_height
                ),
                material=material
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
                -0.020,
                0.020
            )

            x += stone_width + GAP

        y += row_depth + GAP
        row_number += 1


# ============================================================
# BASE SOUS LE PAVAGE
# ============================================================

def create_ground_base():
    bpy.ops.mesh.primitive_cube_add(
        location=(0, 0, -0.10)
    )

    base = bpy.context.active_object
    base.name = "Ground_Base"

    base.dimensions = (
        PAVING_WIDTH + 0.3,
        PAVING_DEPTH + 0.3,
        0.20
    )

    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True
    )

    base.data.materials.append(
        create_base_material()
    )


# ============================================================
# CAMÉRA ET LUMIÈRES
# ============================================================

def create_camera():
    bpy.ops.object.camera_add(
        location=(8.5, -9.5, 8.5)
    )

    camera = bpy.context.active_object
    camera.name = "Camera_Main"

    camera.data.lens = 48

    look_at(
        camera,
        (0, 0, 0)
    )

    bpy.context.scene.camera = camera


def create_lights():
    bpy.ops.object.light_add(
        type="AREA",
        location=(3, -5, 8)
    )

    key_light = bpy.context.active_object
    key_light.name = "Key_Light"

    key_light.data.energy = 1200
    key_light.data.shape = "DISK"
    key_light.data.size = 5

    look_at(
        key_light,
        (0, 0, 0)
    )

    bpy.ops.object.light_add(
        type="AREA",
        location=(-4, 2, 4)
    )

    fill_light = bpy.context.active_object
    fill_light.name = "Fill_Light"

    fill_light.data.energy = 250
    fill_light.data.size = 5

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

    scene.render.resolution_x = 1000
    scene.render.resolution_y = 750
    scene.render.resolution_percentage = 100

    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(RENDER_FILE)

    scene.world.color = (
        0.012,
        0.012,
        0.012
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
    print("🏛️ GÉNÉRATION DU PAVAGE ROMAIN")
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
    create_ground_base()
    generate_paving()
    create_camera()
    create_lights()
    configure_render()

    bpy.ops.render.render(
        write_still=True
    )

    save_file()

    print("=" * 60)
    print("✅ PAVAGE ROMAIN GÉNÉRÉ")
    print(f"💾 Blender : {OUTPUT_FILE}")
    print(f"🖼️ Rendu   : {RENDER_FILE}")
    print("=" * 60)


main()