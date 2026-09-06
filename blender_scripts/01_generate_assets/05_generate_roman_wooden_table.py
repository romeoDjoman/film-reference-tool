import bpy
import random
from mathutils import Vector
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

TABLE_WIDTH = 2.8
TABLE_DEPTH = 1.15
TABLE_HEIGHT = 1.02

TOP_THICKNESS = 0.12
LEG_THICKNESS = 0.14
LEG_INSET = 0.18

EDGE_BEVEL = 0.025
SEED = 101

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_FILE = (
    PROJECT_ROOT /
    "assets/generated/roman_wooden_table.blend"
)

RENDER_FILE = (
    PROJECT_ROOT /
    "output/renders/roman_wooden_table.png"
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
        name="Weathered_Wood"
    )

    principled = get_principled(material)

    principled.inputs["Base Color"].default_value = (
        0.16,
        0.07,
        0.025,
        1.0
    )

    principled.inputs["Roughness"].default_value = 0.78

    material.diffuse_color = (
        0.16,
        0.07,
        0.025,
        1.0
    )

    return material


def create_ground_material():
    material = bpy.data.materials.new(
        name="Preview_Ground"
    )

    principled = get_principled(material)

    principled.inputs["Base Color"].default_value = (
        0.045,
        0.035,
        0.025,
        1.0
    )

    principled.inputs["Roughness"].default_value = 1.0

    return material


# ============================================================
# TABLE
# ============================================================

def create_table():
    random.seed(SEED)

    wood = create_wood_material()

    tabletop_z = (
        TABLE_HEIGHT -
        TOP_THICKNESS / 2
    )

    tabletop = add_cube(
        name="Tabletop",
        location=(0, 0, tabletop_z),
        dimensions=(
            TABLE_WIDTH,
            TABLE_DEPTH,
            TOP_THICKNESS
        ),
        material=wood
    )

    tabletop.rotation_euler[2] = random.uniform(
        -0.008,
        0.008
    )

    leg_height = (
        TABLE_HEIGHT -
        TOP_THICKNESS
    )

    leg_z = leg_height / 2

    leg_x = (
        TABLE_WIDTH / 2 -
        LEG_INSET
    )

    leg_y = (
        TABLE_DEPTH / 2 -
        LEG_INSET
    )

    for x in (-leg_x, leg_x):
        for y in (-leg_y, leg_y):
            leg = add_cube(
                name="Table_Leg",
                location=(x, y, leg_z),
                dimensions=(
                    LEG_THICKNESS,
                    LEG_THICKNESS,
                    leg_height
                ),
                material=wood
            )

            leg.rotation_euler[0] = random.uniform(
                -0.012,
                0.012
            )

            leg.rotation_euler[1] = random.uniform(
                -0.012,
                0.012
            )

    support_height = 0.13

    add_cube(
        name="Long_Support_Left",
        location=(
            -leg_x,
            0,
            support_height
        ),
        dimensions=(
            LEG_THICKNESS,
            TABLE_DEPTH -
            LEG_INSET,
            LEG_THICKNESS
        ),
        material=wood
    )

    add_cube(
        name="Long_Support_Right",
        location=(
            leg_x,
            0,
            support_height
        ),
        dimensions=(
            LEG_THICKNESS,
            TABLE_DEPTH -
            LEG_INSET,
            LEG_THICKNESS
        ),
        material=wood
    )

    add_cube(
        name="Center_Support",
        location=(0, 0, 0.33),
        dimensions=(
            TABLE_WIDTH -
            LEG_INSET * 2,
            LEG_THICKNESS,
            LEG_THICKNESS
        ),
        material=wood
    )


# ============================================================
# SOL, CAMÉRA, LUMIÈRES
# ============================================================

def create_ground():
    bpy.ops.mesh.primitive_plane_add(
        size=12,
        location=(0, 0, 0)
    )

    ground = bpy.context.active_object
    ground.name = "Ground"

    ground.data.materials.append(
        create_ground_material()
    )


def create_camera():
    bpy.ops.object.camera_add(
        location=(4.2, -5.2, 3.2)
    )

    camera = bpy.context.active_object
    camera.name = "Camera_Main"

    camera.data.lens = 50

    look_at(
        camera,
        (0, 0, 0.55)
    )

    bpy.context.scene.camera = camera


def create_lights():
    bpy.ops.object.light_add(
        type="AREA",
        location=(2.5, -3.5, 5.5)
    )

    key_light = bpy.context.active_object
    key_light.name = "Key_Light"

    key_light.data.energy = 900
    key_light.data.size = 4

    look_at(
        key_light,
        (0, 0, 0.7)
    )

    bpy.ops.object.light_add(
        type="AREA",
        location=(-3, 1.5, 3)
    )

    fill_light = bpy.context.active_object
    fill_light.name = "Fill_Light"

    fill_light.data.energy = 180
    fill_light.data.size = 4

    look_at(
        fill_light,
        (0, 0, 0.7)
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
    print("🪵 GÉNÉRATION DE LA TABLE ROMAINE")
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
    create_table()
    create_ground()
    create_camera()
    create_lights()
    configure_render()

    bpy.ops.render.render(
        write_still=True
    )

    save_file()

    print("=" * 60)
    print("✅ TABLE ROMAINE GÉNÉRÉE")
    print(f"💾 Blender : {OUTPUT_FILE}")
    print(f"🖼️ Rendu   : {RENDER_FILE}")
    print("=" * 60)


main()