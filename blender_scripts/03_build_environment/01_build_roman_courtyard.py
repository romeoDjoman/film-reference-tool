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

OUTPUT_FILE = (
    PROJECT_ROOT /
    "assets/blend/roman_courtyard_test.blend"
)

RENDER_FILE = (
    PROJECT_ROOT /
    "output/renders/roman_courtyard_test.png"
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
    """Importe tous les objets d'un fichier .blend dans la scène ouverte."""

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


def remove_cameras_and_lights(objects):
    """Supprime les caméras et lumières provenant des fichiers d'assets."""

    for obj in objects:
        if obj.type in {"CAMERA", "LIGHT"}:
            bpy.data.objects.remove(
                obj,
                do_unlink=True
            )


# ============================================================
# IMPORT DES ASSETS
# ============================================================

def import_paving():
    paving_objects = append_all_objects(
        PAVING_FILE
    )

    mesh_objects = [
        obj
        for obj in paving_objects
        if obj.type == "MESH"
    ]

    remove_cameras_and_lights(
        paving_objects
    )

    print(
        f"✓ Pavage importé : "
        f"{len(mesh_objects)} objets mesh"
    )
def import_wall():
    wall_objects = append_all_objects(
        WALL_FILE
    )

    mesh_objects = [
        obj
        for obj in wall_objects
        if obj.type == "MESH"
    ]

    remove_cameras_and_lights(
        wall_objects
    )

    for obj in mesh_objects:
        obj.location = (
            obj.location.x,
            3.15,
            obj.location.z
        )

    print(
        f"✓ Mur importé : "
        f"{len(mesh_objects)} objets mesh"
    )
    
    
# ============================================================
# DÉCOR COMPLÉMENTAIRE
# ============================================================

def create_backdrop():
    """Ajoute un fond discret derrière le mur pour le rendu de contrôle."""

    bpy.ops.mesh.primitive_plane_add(
        size=30,
        location=(0, 4.4, 7)
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
        0.025,
        0.020,
        0.015,
        1.0
    )

    principled.inputs["Roughness"].default_value = 1.0

    backdrop.data.materials.append(
        material
    )


# ============================================================
# CAMÉRA
# ============================================================

def create_camera():
    bpy.ops.object.camera_add(
        location=(9.5, -11.5, 7.0)
    )

    camera = bpy.context.active_object
    camera.name = "Camera_Courtyard"

    camera.data.lens = 46

    look_at(
        camera,
        (0, 1.0, 1.0)
    )

    bpy.context.scene.camera = camera


# ============================================================
# LUMIÈRES
# ============================================================

def create_lights():
    bpy.ops.object.light_add(
        type="AREA",
        location=(3.0, -4.0, 8.0)
    )

    key_light = bpy.context.active_object
    key_light.name = "Key_Light"

    key_light.data.energy = 1450
    key_light.data.shape = "DISK"
    key_light.data.size = 5.0

    look_at(
        key_light,
        (0, 1.5, 1.0)
    )

    bpy.ops.object.light_add(
        type="AREA",
        location=(-5.0, -1.0, 4.0)
    )

    fill_light = bpy.context.active_object
    fill_light.name = "Fill_Light"

    fill_light.data.energy = 280
    fill_light.data.size = 6.0

    look_at(
        fill_light,
        (0, 1.0, 1.0)
    )

    bpy.ops.object.light_add(
        type="AREA",
        location=(0, 4.0, 6.0)
    )

    rim_light = bpy.context.active_object
    rim_light.name = "Rim_Light"

    rim_light.data.energy = 500
    rim_light.data.size = 4.0

    look_at(
        rim_light,
        (0, 1.5, 1.0)
    )


# ============================================================
# RENDU ET SAUVEGARDE
# ============================================================

def configure_render():
    scene = bpy.context.scene

    scene.render.engine = "BLENDER_EEVEE"

    scene.render.resolution_x = 1200
    scene.render.resolution_y = 800
    scene.render.resolution_percentage = 100

    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(RENDER_FILE)

    scene.world.color = (
        0.01,
        0.01,
        0.01
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
    print("🏛️ CONSTRUCTION DE LA COUR ROMAINE")
    print("=" * 60)

    if not WALL_FILE.exists():
        raise FileNotFoundError(
            f"Mur introuvable : {WALL_FILE}"
        )

    if not PAVING_FILE.exists():
        raise FileNotFoundError(
            f"Pavage introuvable : {PAVING_FILE}"
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
    import_wall()

    create_backdrop()
    create_camera()
    create_lights()
    configure_render()

    bpy.ops.render.render(
        write_still=True
    )

    save_file()

    print("=" * 60)
    print("✅ COUR ROMAINE CRÉÉE")
    print(f"💾 Blender : {OUTPUT_FILE}")
    print(f"🖼️ Rendu   : {RENDER_FILE}")
    print("=" * 60)


main()