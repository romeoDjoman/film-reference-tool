import bpy
from mathutils import Vector
from pathlib import Path


# ============================================================
# CHEMINS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

WALL_FILE = (
    PROJECT_ROOT /
    "assets/generated/roman_stone_wall_v3.blend"
)

PAVING_FILE = (
    PROJECT_ROOT /
    "assets/generated/roman_paving.blend"
)

TABLE_FILE = (
    PROJECT_ROOT /
    "assets/generated/roman_wooden_table.blend"
)

DOORS_FILE = (
    PROJECT_ROOT /
    "assets/generated/roman_double_doors.blend"
)

OUTPUT_FILE = (
    PROJECT_ROOT /
    "output/scenes_3d/scene_001_blocking.blend"
)

RENDER_FILE = (
    PROJECT_ROOT /
    "output/renders/scene_001_blocking.png"
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


def append_all_objects(blend_file):
    with bpy.data.libraries.load(
        str(blend_file),
        link=False
    ) as (data_from, data_to):
        data_to.objects = data_from.objects

    imported_objects = []

    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)
            imported_objects.append(obj)

    return imported_objects


def get_mesh_objects(objects):
    return [
        obj
        for obj in objects
        if obj.type == "MESH"
    ]


def remove_cameras_and_lights(objects):
    objects_to_remove = [
        obj
        for obj in objects
        if obj.type in {"CAMERA", "LIGHT"}
    ]

    for obj in objects_to_remove:
        bpy.data.objects.remove(
            obj,
            do_unlink=True
        )


def move_objects(objects, location):
    for obj in objects:
        obj.location = (
            obj.location.x + location[0],
            obj.location.y + location[1],
            obj.location.z + location[2]
        )


def rotate_objects_z(objects, degrees):
    radians = degrees * 0.01745329252

    for obj in objects:
        obj.rotation_euler[2] += radians


# ============================================================
# IMPORT DES ASSETS
# ============================================================

def import_paving():
    objects = append_all_objects(
        PAVING_FILE
    )

    mesh_objects = get_mesh_objects(
        objects
    )

    remove_cameras_and_lights(
        objects
    )

    print(
        f"✓ Pavage : "
        f"{len(mesh_objects)} objets"
    )

    return mesh_objects


def import_back_wall():
    objects = append_all_objects(
        WALL_FILE
    )

    mesh_objects = get_mesh_objects(
        objects
    )

    remove_cameras_and_lights(
        objects
    )

    move_objects(
        mesh_objects,
        (0, 3.65, 0)
    )

    print(
        f"✓ Mur arrière : "
        f"{len(mesh_objects)} objets"
    )

    return mesh_objects


def import_doors():
    objects = append_all_objects(
        DOORS_FILE
    )

    mesh_objects = get_mesh_objects(
        objects
    )

    remove_cameras_and_lights(
        objects
    )

    move_objects(
        mesh_objects,
        (0, 3.42, 0)
    )

    print(
        f"✓ Portes : "
        f"{len(mesh_objects)} objets"
    )

    return mesh_objects


def import_table():
    objects = append_all_objects(
        TABLE_FILE
    )

    mesh_objects = get_mesh_objects(
        objects
    )

    remove_cameras_and_lights(
        objects
    )

    move_objects(
        mesh_objects,
        (0, 0.35, 0)
    )

    print(
        f"✓ Table : "
        f"{len(mesh_objects)} objets"
    )

    return mesh_objects


# ============================================================
# MARQUEURS DE PERSONNAGES
# ============================================================

def create_placeholder_material(
    name,
    color
):
    material = bpy.data.materials.new(
        name=name
    )

    principled = material.node_tree.nodes.get(
        "Principled BSDF"
    )

    principled.inputs["Base Color"].default_value = (
        *color,
        1.0
    )

    principled.inputs["Roughness"].default_value = 0.72

    return material


def create_character_placeholder(
    name,
    location,
    color,
    height=1.75
):
    material = create_placeholder_material(
        f"{name}_Material",
        color
    )

    body_height = height * 0.62
    head_radius = height * 0.10

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=height * 0.14,
        depth=body_height,
        location=(
            location[0],
            location[1],
            location[2] +
            body_height / 2
        )
    )

    body = bpy.context.active_object
    body.name = f"{name}_Body"
    body.data.materials.append(material)

    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=16,
        ring_count=8,
        radius=head_radius,
        location=(
            location[0],
            location[1],
            location[2] +
            body_height +
            head_radius
        )
    )

    head = bpy.context.active_object
    head.name = f"{name}_Head"
    head.data.materials.append(material)

    return body, head


def create_character_blocking():
    create_character_placeholder(
        name="Authority_Figure",
        location=(0, 1.15, 0),
        color=(0.32, 0.10, 0.06),
        height=1.30
    )

    create_character_placeholder(
        name="Guard_Left",
        location=(-1.55, 1.85, 0),
        color=(0.18, 0.20, 0.24),
        height=1.82
    )

    create_character_placeholder(
        name="Guard_Right",
        location=(1.55, 1.85, 0),
        color=(0.18, 0.20, 0.24),
        height=1.82
    )

    create_character_placeholder(
        name="Prisoner",
        location=(0, -0.85, 0),
        color=(0.30, 0.22, 0.16),
        height=0.35
    )

    print("✓ Marqueurs personnages : 4")


# ============================================================
# FOND ET AMBIANCE
# ============================================================

def create_backdrop():
    bpy.ops.mesh.primitive_plane_add(
        size=30,
        location=(0, 5.25, 7)
    )

    backdrop = bpy.context.active_object
    backdrop.name = "Backdrop"

    backdrop.rotation_euler = (
        1.5708,
        0,
        0
    )

    material = bpy.data.materials.new(
        name="Backdrop_Material"
    )

    principled = material.node_tree.nodes.get(
        "Principled BSDF"
    )

    principled.inputs["Base Color"].default_value = (
        0.018,
        0.016,
        0.014,
        1.0
    )

    principled.inputs["Roughness"].default_value = 1.0

    backdrop.data.materials.append(
        material
    )


# ============================================================
# CAMÉRA ET LUMIÈRES
# ============================================================

def create_camera():
    bpy.ops.object.camera_add(
        location=(5.8, -8.8, 3.15)
    )

    camera = bpy.context.active_object
    camera.name = "Scene_001_Camera"

    camera.data.lens = 45

    look_at(
        camera,
        (0, 1.15, 1.05)
    )

    bpy.context.scene.camera = camera


def create_lights():
    bpy.ops.object.light_add(
        type="AREA",
        location=(-2.5, -2.5, 8.0)
    )

    sky_light = bpy.context.active_object
    sky_light.name = "Soft_Daylight"

    sky_light.data.energy = 1250
    sky_light.data.shape = "DISK"
    sky_light.data.size = 7.0

    look_at(
        sky_light,
        (0, 1.2, 0.8)
    )

    bpy.ops.object.light_add(
        type="AREA",
        location=(4.0, 1.5, 5.0)
    )

    fill_light = bpy.context.active_object
    fill_light.name = "Soft_Fill"

    fill_light.data.energy = 360
    fill_light.data.size = 6.0

    look_at(
        fill_light,
        (0, 1.3, 1.0)
    )

    bpy.ops.object.light_add(
        type="AREA",
        location=(0, 4.0, 6.5)
    )

    back_light = bpy.context.active_object
    back_light.name = "Back_Light"

    back_light.data.energy = 450
    back_light.data.size = 5.0

    look_at(
        back_light,
        (0, 1.5, 1.0)
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
    print("🎬 CONSTRUCTION — SCÈNE 001 / BLOCKING")
    print("=" * 60)

    required_files = [
        WALL_FILE,
        PAVING_FILE,
        TABLE_FILE,
        DOORS_FILE,
    ]

    for file_path in required_files:
        if not file_path.exists():
            raise FileNotFoundError(
                f"Asset introuvable : {file_path}"
            )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    RENDER_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    clear_scene()

    import_paving()
    import_back_wall()
    import_doors()
    import_table()

    create_character_blocking()
    create_backdrop()

    create_camera()
    create_lights()
    configure_render()

    bpy.ops.render.render(
        write_still=True
    )

    save_file()

    print("=" * 60)
    print("✅ SCÈNE 001 — BLOCKING CRÉÉ")
    print(f"💾 Blender : {OUTPUT_FILE}")
    print(f"🖼️ Rendu   : {RENDER_FILE}")
    print("=" * 60)


main()