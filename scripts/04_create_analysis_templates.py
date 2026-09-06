import json
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

SCENES_FOLDER = Path("output/scenes")


# ============================================================
# TEMPLATE D'ANALYSE
# ============================================================

def create_empty_analysis(scene_number):

    return {
        "scene": scene_number,

        "characters": [],

        "environment": {
            "location": "",
            "interior_exterior": "",
            "architecture": "",
            "walls": "",
            "floor": "",
            "ceiling": "",
            "background": "",
            "depth": ""
        },

        "objects": [],

        "camera": {
            "shot_type": "",
            "angle": "",
            "height": "",
            "composition": "",
            "perspective": "",
            "movement": "",
            "estimated_focal_length": ""
        },

        "lighting": {
            "sources": [],
            "direction": "",
            "intensity": "",
            "softness": "",
            "color_temperature": "",
            "shadows": "",
            "mood": ""
        },

        "visual_style": "",

        "3d_reconstruction": {
            "important_assets": [],
            "materials": [],
            "geometry": [],
            "existing_assets": []
        }
    }


# ============================================================
# CRÉER LE TEMPLATE D'UNE SCÈNE
# ============================================================

def create_template(scene_folder):

    scene_number = int(
        scene_folder.name.split("_")[1]
    )

    analysis_file = (
        scene_folder / "analysis.json"
    )

    # --------------------------------------------------------
    # NE JAMAIS ÉCRASER UNE ANALYSE EXISTANTE
    # --------------------------------------------------------

    if analysis_file.exists():

        try:

            with open(
                analysis_file,
                "r",
                encoding="utf-8"
            ) as file:

                existing_data = json.load(file)

            # Vérifier qu'il s'agit bien d'un JSON
            if isinstance(existing_data, dict):

                print(
                    f"   ⏭️ Analyse existante conservée"
                )

                return "existing"

        except (
            json.JSONDecodeError,
            OSError
        ):

            print(
                f"   ⚠️ analysis.json invalide"
            )

            print(
                f"   → remplacement par un template"
            )

    # --------------------------------------------------------
    # CRÉER LE TEMPLATE
    # --------------------------------------------------------

    analysis = create_empty_analysis(
        scene_number
    )

    with open(
        analysis_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            analysis,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"   ✓ Template créé"
    )

    return "created"


# ============================================================
# TOUTES LES SCÈNES
# ============================================================

def create_all_templates():

    print()
    print("=" * 60)
    print("📝 PRÉPARATION DES ANALYSES")
    print("=" * 60)

    scene_folders = sorted(
        folder
        for folder in SCENES_FOLDER.glob("scene_*")
        if folder.is_dir()
    )

    print(
        f"\n🎬 {len(scene_folders)} scènes trouvées"
    )

    created = 0
    existing = 0
    errors = 0

    for scene_folder in scene_folders:

        print(
            f"\n🎬 {scene_folder.name}"
        )

        try:

            result = create_template(
                scene_folder
            )

            if result == "created":
                created += 1

            elif result == "existing":
                existing += 1

        except Exception as error:

            errors += 1

            print(
                f"   ❌ Erreur : {error}"
            )

    print()
    print("=" * 60)
    print("✅ PRÉPARATION TERMINÉE")
    print("=" * 60)

    print(
        f"📄 Templates créés : {created}"
    )

    print(
        f"📂 Analyses existantes conservées : "
        f"{existing}"
    )

    print(
        f"❌ Erreurs : {errors}"
    )

    print("=" * 60)


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

if __name__ == "__main__":

    create_all_templates()