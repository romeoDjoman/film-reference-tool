import json
from pathlib import Path
from collections import Counter


# ============================================================
# CONFIGURATION
# ============================================================

SCENES_FOLDER = Path("output/scenes")
OUTPUT_FILE = Path("output/film_analysis.json")


# ============================================================
# CHARGER UNE ANALYSE
# ============================================================

def load_analysis(file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as error:

        print(
            f"❌ Impossible de lire {file_path}: {error}"
        )

        return None


# ============================================================
# EXTRAIRE LES PERSONNAGES
# ============================================================

def collect_characters(analyses):

    characters = []

    for analysis in analyses:

        scene_number = analysis.get("scene")

        for character in analysis.get(
            "characters",
            []
        ):

            character_copy = character.copy()

            character_copy["scene"] = scene_number

            characters.append(
                character_copy
            )

    return characters


# ============================================================
# EXTRAIRE LES OBJETS
# ============================================================

def collect_objects(analyses):

    objects = []

    for analysis in analyses:

        scene_number = analysis.get("scene")

        for obj in analysis.get(
            "objects",
            []
        ):

            object_copy = obj.copy()

            object_copy["scene"] = scene_number

            objects.append(
                object_copy
            )

    return objects


# ============================================================
# EXTRAIRE LES ASSETS 3D
# ============================================================

def collect_3d_assets(analyses):

    important_assets = []
    materials = []
    geometry = []
    existing_assets = []

    for analysis in analyses:

        reconstruction = analysis.get(
            "3d_reconstruction",
            {}
        )

        important_assets.extend(
            reconstruction.get(
                "important_assets",
                []
            )
        )

        materials.extend(
            reconstruction.get(
                "materials",
                []
            )
        )

        geometry.extend(
            reconstruction.get(
                "geometry",
                []
            )
        )

        existing_assets.extend(
            reconstruction.get(
                "existing_assets",
                []
            )
        )

    return {
        "important_assets": sorted(
            set(important_assets)
        ),

        "materials": sorted(
            set(materials)
        ),

        "geometry": sorted(
            set(geometry)
        ),

        "existing_assets": sorted(
            set(existing_assets)
        )
    }


# ============================================================
# ENVIRONNEMENTS
# ============================================================

def collect_environments(analyses):

    environments = []

    for analysis in analyses:

        environment = analysis.get(
            "environment",
            {}
        )

        environment_copy = environment.copy()

        environment_copy["scene"] = analysis.get(
            "scene"
        )

        environments.append(
            environment_copy
        )

    return environments


# ============================================================
# CAMÉRAS
# ============================================================

def collect_cameras(analyses):

    cameras = []

    for analysis in analyses:

        camera = analysis.get(
            "camera",
            {}
        )

        camera_copy = camera.copy()

        camera_copy["scene"] = analysis.get(
            "scene"
        )

        cameras.append(
            camera_copy
        )

    return cameras


# ============================================================
# ÉCLAIRAGES
# ============================================================

def collect_lighting(analyses):

    lighting = []

    for analysis in analyses:

        light = analysis.get(
            "lighting",
            {}
        )

        light_copy = light.copy()

        light_copy["scene"] = analysis.get(
            "scene"
        )

        lighting.append(
            light_copy
        )

    return lighting


# ============================================================
# STYLES VISUELS
# ============================================================

def collect_visual_styles(analyses):

    styles = []

    for analysis in analyses:

        style = analysis.get(
            "visual_style"
        )

        if style:

            styles.append({
                "scene": analysis.get("scene"),
                "style": style
            })

    return styles


# ============================================================
# CALCULER LES STATISTIQUES
# ============================================================

def calculate_statistics(analyses):

    scene_count = len(analyses)

    character_count = sum(
        len(
            analysis.get(
                "characters",
                []
            )
        )
        for analysis in analyses
    )

    object_count = sum(
        len(
            analysis.get(
                "objects",
                []
            )
        )
        for analysis in analyses
    )

    locations = []

    for analysis in analyses:

        environment = analysis.get(
            "environment",
            {}
        )

        location = environment.get(
            "location"
        )

        if location:

            locations.append(location)

    location_counts = Counter(
        locations
    )

    return {
        "scenes_analyzed": scene_count,

        "character_instances": character_count,

        "object_instances": object_count,

        "locations": dict(
            location_counts
        )
    }


# ============================================================
# CONSTRUIRE L'ANALYSE GLOBALE
# ============================================================

def build_film_analysis(analyses):

    return {

        "project": {
            "name": "Passion Christ Flagellation",
            "analysis_type": "Cinematic 3D reconstruction",
            "model": "qwen3.5:4b",
            "source_scenes": len(analyses)
        },

        "statistics": calculate_statistics(
            analyses
        ),

        "scenes": analyses,

        "characters": collect_characters(
            analyses
        ),

        "environments": collect_environments(
            analyses
        ),

        "objects": collect_objects(
            analyses
        ),

        "cameras": collect_cameras(
            analyses
        ),

        "lighting": collect_lighting(
            analyses
        ),

        "visual_styles": collect_visual_styles(
            analyses
        ),

        "3d_assets": collect_3d_assets(
            analyses
        )
    }


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

def main():

    print("\n" + "=" * 60)

    print(
        "🎬 FUSION DES ANALYSES DU FILM"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # VÉRIFIER LE DOSSIER
    # --------------------------------------------------------

    if not SCENES_FOLDER.exists():

        print(
            f"❌ Dossier introuvable : {SCENES_FOLDER}"
        )

        return

    # --------------------------------------------------------
    # RÉCUPÉRER UNIQUEMENT LES DOSSIERS
    # --------------------------------------------------------

    scene_folders = sorted(

        folder

        for folder in SCENES_FOLDER.glob("scene_*")

        if folder.is_dir()
    )

    print(
        f"\n📁 {len(scene_folders)} dossiers de scènes trouvés"
    )

    # --------------------------------------------------------
    # CHARGER LES ANALYSES
    # --------------------------------------------------------

    analyses = []

    errors = 0

    for scene_folder in scene_folders:

        analysis_file = (
            scene_folder /
            "analysis.json"
        )

        if not analysis_file.exists():

            print(
                f"⚠️ Analyse manquante : "
                f"{scene_folder.name}"
            )

            errors += 1

            continue

        analysis = load_analysis(
            analysis_file
        )

        if analysis is None:

            errors += 1

            continue

        analyses.append(
            analysis
        )

        print(
            f"✓ {scene_folder.name}"
        )

    # --------------------------------------------------------
    # VÉRIFICATION
    # --------------------------------------------------------

    if not analyses:

        print(
            "\n❌ Aucune analyse valide trouvée."
        )

        return

    # --------------------------------------------------------
    # CONSTRUIRE L'ANALYSE GLOBALE
    # --------------------------------------------------------

    film_analysis = build_film_analysis(
        analyses
    )

    # --------------------------------------------------------
    # CRÉER LE DOSSIER OUTPUT
    # --------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # SAUVEGARDER
    # --------------------------------------------------------

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            film_analysis,
            file,
            indent=4,
            ensure_ascii=False
        )

    # --------------------------------------------------------
    # RÉSUMÉ
    # --------------------------------------------------------

    print("\n" + "=" * 60)

    print(
        "✅ FUSION TERMINÉE"
    )

    print("=" * 60)

    print(
        f"🎬 Scènes analysées : "
        f"{len(analyses)}"
    )

    print(
        f"👤 Instances de personnages : "
        f"{film_analysis['statistics']['character_instances']}"
    )

    print(
        f"📦 Instances d'objets : "
        f"{film_analysis['statistics']['object_instances']}"
    )

    print(
        f"🏛️ Lieux détectés : "
        f"{len(film_analysis['statistics']['locations'])}"
    )

    print(
        f"📐 Assets 3D : "
        f"{len(film_analysis['3d_assets']['important_assets'])}"
    )

    print(
        f"🧱 Matériaux : "
        f"{len(film_analysis['3d_assets']['materials'])}"
    )

    print(
        f"📦 Assets existants potentiels : "
        f"{len(film_analysis['3d_assets']['existing_assets'])}"
    )

    print(
        f"\n💾 Fichier créé : "
        f"{OUTPUT_FILE}"
    )

    if errors > 0:

        print(
            f"\n⚠️ Analyses problématiques : {errors}"
        )

    print("=" * 60)


# ============================================================
# LANCEMENT
# ============================================================

if __name__ == "__main__":

    main()
