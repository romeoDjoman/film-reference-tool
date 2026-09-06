import bpy
import random
from mathutils import Vector


# ============================================================
# CONFIGURATION
# ============================================================

RENDER_FILE = "output/renders/roman_stone_wall.png"

WALL_WIDTH = 6.0
WALL_HEIGHT = 3.0

BLOCK_WIDTH = 0.75
BLOCK_HEIGHT = 0.45
BLOCK_DEPTH = 0.35

GAP = 0.025

OUTPUT_FILE = "assets/generated/roman_stone_wall.blend"

SEED = 42


# ============================================================
# NETTOYAGE
# ============================================================

def clear_scene():

    bpy.ops.object.select_all(
        action="SELECT"
    )

    bpy.ops.object.delete(
        use_global=False
    )


# ============================================================
# MATÉRIAU
# ============================================================

def create_stone_material():

    material = bpy.data.materials.new(
        "Roman Stone"
    )

    principled = material.node_tree.nodes.get(
        "Principled BSDF"
    )

    principled.inputs["Base Color"].default_value = (
        0.32,
        0.28,
        0.22,
        1.0
    )

    principled.inputs["Roughness"].default_value = 0.85

    material.diffuse_color = (
        0.32,
        0.28,
        0.22,
        1.0
    )

    return material

# ============================================================
# CRÉER UN BLOC
# ============================================================

def create_block(
    location,
    scale,
    material
):

    bpy.ops.mesh.primitive_cube_add(
        location=location
    )

    block = bpy.context.object

    block.name = "Stone_Block"

    block.dimensions = scale

    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True
    )

    block.data.materials.append(
        material
    )

    return block


# ============================================================
# CONSTRUIRE LE MUR
# ============================================================

def generate_wall():

    random.seed(SEED)

    material = create_stone_material()

    blocks_x = int(
        WALL_WIDTH /
        (BLOCK_WIDTH + GAP)
    )

    blocks_y = int(
        WALL_HEIGHT /
        (BLOCK_HEIGHT + GAP)
    )

    for row in range(blocks_y):

        offset = 0

        # Décalage d'une rangée sur deux
        if row % 2 == 1:
            offset = BLOCK_WIDTH / 2

        for column in range(blocks_x + 1):

            x = (
                column *
                (BLOCK_WIDTH + GAP)
                + offset
                - WALL_WIDTH / 2
            )

            y = 0

            z = (
                row *
                (BLOCK_HEIGHT + GAP)
                + BLOCK_HEIGHT / 2
            )

            # Éviter les blocs trop éloignés
            if abs(x) > WALL_WIDTH / 2:
                continue

            # Variation légère
            width = BLOCK_WIDTH * random.uniform(
                0.90,
                1.10
            )

            height = BLOCK_HEIGHT * random.uniform(
                0.92,
                1.08
            )

            depth = BLOCK_DEPTH * random.uniform(
                0.95,
                1.05
            )

            block = create_block(
                (x, y, z),
                (width, depth, height),
                material
            )

            # Petite rotation réaliste
            block.rotation_euler[1] = random.uniform(
                -0.015,
                0.015
            )

            block.rotation_euler[2] = random.uniform(
                -0.015,
                0.015
            )


# ============================================================
# SOL
# ============================================================

def create_ground():

    bpy.ops.mesh.primitive_plane_add(
        size=20,
        location=(0, 0, 0)
    )

    ground = bpy.context.object

    ground.name = "Ground"

    material = bpy.data.materials.new(
        "Ground Stone"
    )


    principled = material.node_tree.nodes.get(
        "Principled BSDF"
    )

    principled.inputs["Base Color"].default_value = (
        0.18,
        0.16,
        0.13,
        1.0
    )

    principled.inputs["Roughness"].default_value = 0.9

    material.diffuse_color = (
        0.18,
        0.16,
        0.13,
        1.0
    )

    ground.data.materials.append(
        material
    )


# ============================================================
# CAMÉRA
# ============================================================

def create_camera():

    bpy.ops.object.camera_add(
        location=(7, -8, 4.5)
    )

    camera = bpy.context.object

    camera.name = "Camera_Main"

    direction = Vector(
        (0, 0, 1.4)
    ) - camera.location

    camera.rotation_euler = (
        direction.to_track_quat(
            "-Z",
            "Y"
        ).to_euler()
    )

    camera.data.lens = 50

    bpy.context.scene.camera = camera


# ============================================================
# LUMIÈRE
# ============================================================

def create_light():

    bpy.ops.object.light_add(
        type="AREA",
        location=(2, -4, 6)
    )

    light = bpy.context.object

    light.name = "Key_Light"

    light.data.energy = 1200

    light.data.shape = "DISK"

    light.data.size = 5

    direction = Vector(
        (0, 0, 1)
    ) - light.location

    light.rotation_euler = (
        direction.to_track_quat(
            "-Z",
            "Y"
        ).to_euler()
    )


# ============================================================
# SAUVEGARDE
# ============================================================

def save_file():

    bpy.ops.wm.save_as_mainfile(
        filepath=OUTPUT_FILE
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "========================================"
    )

    print(
        "🏛️ GÉNÉRATION DU MUR ROMAIN"
    )

    print(
        "========================================"
    )

    clear_scene()

    generate_wall()

    create_ground()

    create_camera()

    create_light()
    
    scene = bpy.context.scene

    scene.render.engine = "BLENDER_EEVEE"

    scene.render.resolution_x = 1000
    scene.render.resolution_y = 750
    scene.render.resolution_percentage = 100

    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = RENDER_FILE

    bpy.ops.render.render(
        write_still=True
    )

    save_file()

    print(
        "========================================"
    )

    print(
        "✅ MUR GÉNÉRÉ"
    )

    print(
        f"💾 {OUTPUT_FILE}"
    )

    print(
        "========================================"
    )


main()