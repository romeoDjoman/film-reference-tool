import bpy
import random
from mathutils import Vector
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

WALL_WIDTH = 6.0
WALL_HEIGHT = 3.0

BLOCK_WIDTH = 0.78
BLOCK_HEIGHT = 0.42
BLOCK_DEPTH = 0.35

GAP = 0.035
EDGE_BEVEL = 0.025

SEED = 42

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_FILE = (
    PROJECT_ROOT /
    "assets/generated/roman_stone_wall_v3.blend"
)

RENDER_FILE = (
    PROJECT_ROOT /
    "output/renders/roman_stone_wall_v3.png"
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

def create_stone_material():
    material = bpy.data.materials.new(
        name="Roman_Stone"
    )

    principled = get_principled(material)

    principled.inputs["Base Color"].default_value = (
        0.22,
        0.17,
        0.12,
        1.0
    )

    principled.inputs["Roughness"].default_value = 0.9

    material.diffuse_color = (
        0.22,
        0.17,
        0.12,
        1.0
    )

    return material


def create_ground_material():
    material = bpy.data.materials.new(
        name="Ground_Stone"
    )

    principled = get_principled(material)

    principled.inputs["Base Color"].default_value = (
        0.08,
        0.065,
        0.05,
        1.0
    )

    principled.inputs["Roughness"].default_value = 0.95

    material.diffuse_color = (
        0.08,
        0.065,
        0.05,
        1.0
    )

    return material


# ============================================================
# PIERRES
# ============================================================

def add_bevel(block):
    bevel = block.modifiers.new(
        name="Stone_Edge_Bevel",
        type="BEVEL"
    )

    bevel.width = EDGE_BEVEL
    bevel.segments = 2

    bpy.context.view_layer.objects.active = block

    bpy.ops.object.modifier_apply(
        modifier=bevel.name
    )


def create_block(location, dimensions, material):
    bpy.ops.mesh.primitive_cube_add(
        location=location
    )

    block = bpy.context.active_object
    block.name = "Stone_Block"

    block.dimensions = dimensions

    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True
    )

    block.data.materials.append(
        material
    )

    add_bevel(block)

    return block


def generate_wall():
    random.seed(SEED)

    material = create_stone_material()

    blocks_y = int(
        WALL_HEIGHT /
        (BLOCK_HEIGHT + GAP)
    )

    wall_left = -WALL_WIDTH / 2
    wall_right = WALL_WIDTH / 2

    for row in range(blocks_y):
        row_z = (
            row *
            (BLOCK_HEIGHT + GAP)
            + BLOCK_HEIGHT / 2
        )

        offset = 0.0

        if row % 2 == 1:
            offset = BLOCK_WIDTH / 2

        x = wall_left + offset

        while x < wall_right:
            width = BLOCK_WIDTH * random.uniform(
                0.84,
                1.16
            )

            remaining_width = wall_right - x

            # Ne jamais produire une dernière pierre trop petite.
            # Si l'espace restant est inférieur à 45 % d'une pierre,
            # on ajoute cet espace à la pierre précédente en pratique
            # en utilisant la dernière pierre comme bloc de bord.
            if remaining_width < BLOCK_WIDTH * 0.45:
                break

            # La dernière pierre occupe proprement la largeur restante.
            if width > remaining_width:
                width = remaining_width

            # Les blocs de bord doivent rester visuellement cohérents.
            if x == wall_left + offset:
                width = min(
                    width,
                    BLOCK_WIDTH * 1.05
                )

            height = BLOCK_HEIGHT * random.uniform(
                0.90,
                1.10
            )

            depth = BLOCK_DEPTH * random.uniform(
                0.94,
                1.06
            )

            center_x = x + width / 2

            jitter_x = random.uniform(
                -0.010,
                0.010
            )

            jitter_y = random.uniform(
                -0.010,
                0.010
            )

            jitter_z = random.uniform(
                -0.008,
                0.008
            )

            # On bloque les variations à proximité des bords
            # afin de conserver une silhouette de mur propre.
            if center_x - width / 2 <= wall_left + 0.05:
                jitter_x = 0.0

            if center_x + width / 2 >= wall_right - 0.05:
                jitter_x = 0.0

            block = create_block(
                location=(
                    center_x + jitter_x,
                    jitter_y,
                    row_z + jitter_z
                ),
                dimensions=(
                    width,
                    depth,
                    height
                ),
                material=material
            )

            block.rotation_euler[0] = random.uniform(
                -0.008,
                0.008
            )

            block.rotation_euler[1] = random.uniform(
                -0.015,
                0.015
            )

            block.rotation_euler[2] = random.uniform(
                -0.010,
                0.010
            )

            x += width + GAP


# ============================================================
# SOL
# ============================================================

def create_ground():
    bpy.ops.mesh.primitive_plane_add(
        size=20,
        location=(0, 0, 0)
    )

    ground = bpy.context.active_object
    ground.name = "Ground"

    ground.data.materials.append(
        create_ground_material()
    )


# ============================================================
# CAMÉRA ET LUMIÈRE
# ============================================================

def create_camera():
    bpy.ops.object.camera_add(
        location=(7, -8, 4.2)
    )

    camera = bpy.context.active_object
    camera.name = "Camera_Main"

    camera.data.lens = 52

    look_at(
        camera,
        (0, 0, WALL_HEIGHT * 0.45)
    )

    bpy.context.scene.camera = camera


def create_lights():
    bpy.ops.object.light_add(
        type="AREA",
        location=(3.5, -4.5, 6)
    )

    key_light = bpy.context.active_object
    key_light.name = "Key_Light"

    key_light.data.energy = 1000
    key_light.data.shape = "DISK"
    key_light.data.size = 4

    look_at(
        key_light,
        (0, 0, 1.2)
    )

    bpy.ops.object.light_add(
        type="AREA",
        location=(-4, -1.5, 3)
    )

    fill_light = bpy.context.active_object
    fill_light.name = "Fill_Light"

    fill_light.data.energy = 180
    fill_light.data.size = 5

    look_at(
        fill_light,
        (0, 0, 1.2)
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
        0.015,
        0.015,
        0.015
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
    print("🏛️ GÉNÉRATION DU MUR ROMAIN — V3")
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
    generate_wall()
    create_ground()
    create_camera()
    create_lights()
    configure_render()

    bpy.ops.render.render(
        write_still=True
    )

    save_file()

    print("=" * 60)
    print("✅ MUR ROMAIN V3 GÉNÉRÉ")
    print(f"💾 Blender : {OUTPUT_FILE}")
    print(f"🖼️ Rendu   : {RENDER_FILE}")
    print("=" * 60)


main()