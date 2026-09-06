import bpy
import random
from mathutils import Vector
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

DOOR_WIDTH = 3.20
DOOR_HEIGHT = 4.20
DOOR_THICKNESS = 0.16

FRAME_WIDTH = 0.28
FRAME_DEPTH = 0.30

PLANK_COUNT_PER_DOOR = 6
PLANK_GAP = 0.018

CROSSBEAM_HEIGHT = 0.16
CROSSBEAM_DEPTH = 0.24

HINGE_RADIUS = 0.055
HINGE_DEPTH = 0.22

EDGE_BEVEL = 0.018
SEED = 202

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_FILE = (
    PROJECT_ROOT /
    "assets/generated/roman_double_doors.blend"
)

RENDER_FILE = (
    PROJECT_ROOT /
    "output/renders/roman_double_doors.png"
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


def add_bevel(obj, width=EDGE_BEVEL):
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

def create_wood_material():
    material = bpy.data.materials.new(
        name="Dark_Weathered_Wood"
    )

    principled = get_principled(material)

    principled.inputs["Base Color"].default_value = (
        0.075,
        0.025,
        0.008,
        1.0
    )

    principled.inputs["Roughness"].default_value = 0.84

    material.diffuse_color = (
        0.075,
        0.025,
        0.008,
        1.0
    )

    return material


def create_metal_material():
    material = bpy.data.materials.new(
        name="Aged_Iron"
    )

    principled = get_principled(material)

    principled.inputs["Base Color"].default_value = (
        0.055,
        0.050,
        0.045,
        1.0
    )

    principled.inputs["Metallic"].default_value = 0.78
    principled.inputs["Roughness"].default_value = 0.52

    material.diffuse_color = (
        0.055,
        0.050,
        0.045,
        1.0
    )

    return material


def create_ground_material():
    material = bpy.data.materials.new(
        name="Preview_Ground"
    )

    principled = get_principled(material)

    principled.inputs["Base Color"].default_value = (
        0.040,
        0.032,
        0.025,
        1.0
    )

    principled.inputs["Roughness"].default_value = 1.0

    return material


# ============================================================
# PORTE
# ============================================================

def create_door_leaf(
    name,
    center_x,
    wood,
    metal
):
    leaf_width = DOOR_WIDTH / 2

    plank_width = (
        leaf_width -
        PLANK_GAP *
        (PLANK_COUNT_PER_DOOR - 1)
    ) / PLANK_COUNT_PER_DOOR

    start_x = (
        center_x -
        leaf_width / 2 +
        plank_width / 2
    )

    for plank_index in range(
        PLANK_COUNT_PER_DOOR
    ):
        x = (
            start_x +
            plank_index *
            (plank_width + PLANK_GAP)
        )

        plank = add_cube(
            name=(
                f"{name}_Plank_"
                f"{plank_index + 1:02d}"
            ),
            location=(
                x,
                0,
                DOOR_HEIGHT / 2
            ),
            dimensions=(
                plank_width,
                DOOR_THICKNESS,
                DOOR_HEIGHT
            ),
            material=wood
        )

        plank.rotation_euler[1] = random.uniform(
            -0.006,
            0.006
        )

        plank.rotation_euler[2] = random.uniform(
            -0.004,
            0.004
        )

    for z in (
        DOOR_HEIGHT * 0.24,
        DOOR_HEIGHT * 0.52,
        DOOR_HEIGHT * 0.80
    ):
        crossbeam = add_cube(
            name=f"{name}_Crossbeam",
            location=(
                center_x,
                -DOOR_THICKNESS / 2,
                z
            ),
            dimensions=(
                leaf_width -
                0.10,
                CROSSBEAM_DEPTH,
                CROSSBEAM_HEIGHT
            ),
            material=wood
        )

    hinge_x = (
        center_x -
        leaf_width / 2 +
        0.12
    )

    if center_x < 0:
        hinge_x = (
            center_x +
            leaf_width / 2 -
            0.12
        )

    for z in (
        DOOR_HEIGHT * 0.22,
        DOOR_HEIGHT * 0.50,
        DOOR_HEIGHT * 0.78
    ):
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=HINGE_RADIUS,
            depth=HINGE_DEPTH,
            location=(
                hinge_x,
                -DOOR_THICKNESS / 2,
                z
            ),
            rotation=(1.5708, 0, 0)
        )

        hinge = bpy.context.active_object
        hinge.name = f"{name}_Iron_Hinge"
        hinge.data.materials.append(metal)


def create_door_frame(wood):
    left_x = -DOOR_WIDTH / 2 - FRAME_WIDTH / 2
    right_x = DOOR_WIDTH / 2 + FRAME_WIDTH / 2

    add_cube(
        name="Door_Frame_Left",
        location=(
            left_x,
            0,
            DOOR_HEIGHT / 2
        ),
        dimensions=(
            FRAME_WIDTH,
            FRAME_DEPTH,
            DOOR_HEIGHT +
            FRAME_WIDTH
        ),
        material=wood
    )

    add_cube(
        name="Door_Frame_Right",
        location=(
            right_x,
            0,
            DOOR_HEIGHT / 2
        ),
        dimensions=(
            FRAME_WIDTH,
            FRAME_DEPTH,
            DOOR_HEIGHT +
            FRAME_WIDTH
        ),
        material=wood
    )

    add_cube(
        name="Door_Frame_Top",
        location=(
            0,
            0,
            DOOR_HEIGHT +
            FRAME_WIDTH / 2
        ),
        dimensions=(
            DOOR_WIDTH +
            FRAME_WIDTH * 2,
            FRAME_DEPTH,
            FRAME_WIDTH
        ),
        material=wood
    )


def create_double_doors():
    random.seed(SEED)

    wood = create_wood_material()
    metal = create_metal_material()

    left_center = -DOOR_WIDTH / 4
    right_center = DOOR_WIDTH / 4

    create_door_leaf(
        "Door_Left",
        left_center,
        wood,
        metal
    )

    create_door_leaf(
        "Door_Right",
        right_center,
        wood,
        metal
    )

    create_door_frame(wood)


# ============================================================
# SOL, CAMÉRA, LUMIÈRES
# ============================================================

def create_ground():
    bpy.ops.mesh.primitive_plane_add(
        size=14,
        location=(0, 0, 0)
    )

    ground = bpy.context.active_object
    ground.name = "Ground"

    ground.data.materials.append(
        create_ground_material()
    )


def create_camera():
    bpy.ops.object.camera_add(
        location=(6.8, -8.5, 4.3)
    )

    camera = bpy.context.active_object
    camera.name = "Camera_Main"

    camera.data.lens = 52

    look_at(
        camera,
        (0, 0, DOOR_HEIGHT * 0.48)
    )

    bpy.context.scene.camera = camera


def create_lights():
    bpy.ops.object.light_add(
        type="AREA",
        location=(2.8, -4.0, 6.5)
    )

    key_light = bpy.context.active_object
    key_light.name = "Key_Light"

    key_light.data.energy = 1100
    key_light.data.size = 4.5

    look_at(
        key_light,
        (0, 0, DOOR_HEIGHT * 0.45)
    )

    bpy.ops.object.light_add(
        type="AREA",
        location=(-3.0, -1.0, 3.5)
    )

    fill_light = bpy.context.active_object
    fill_light.name = "Fill_Light"

    fill_light.data.energy = 200
    fill_light.data.size = 5

    look_at(
        fill_light,
        (0, 0, DOOR_HEIGHT * 0.45)
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
    print("🚪 GÉNÉRATION DES PORTES ROMAINES")
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
    create_double_doors()
    create_ground()
    create_camera()
    create_lights()
    configure_render()

    bpy.ops.render.render(
        write_still=True
    )

    save_file()

    print("=" * 60)
    print("✅ PORTES ROMAINES GÉNÉRÉES")
    print(f"💾 Blender : {OUTPUT_FILE}")
    print(f"🖼️ Rendu   : {RENDER_FILE}")
    print("=" * 60)


main()