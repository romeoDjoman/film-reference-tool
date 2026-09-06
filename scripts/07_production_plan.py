import json
import re
from pathlib import Path
from collections import Counter


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = Path("output/film_analysis.json")
OUTPUT_FOLDER = Path("output/preproduction")


# ============================================================
# OUTILS
# ============================================================

def normalize_text(text):
    """
    Normalise un texte pour faciliter le regroupement.
    """

    if not text:
        return ""

    text = str(text).lower().strip()

    # Supprimer quelques caractères inutiles
    text = re.sub(r"[.,;:!?()\[\]{}]", "", text)

    # Espaces multiples
    text = re.sub(r"\s+", " ", text)

    return text


def load_json(file_path):

    if not file_path.exists():

        print(
            f"❌ Fichier introuvable : {file_path}"
        )

        return None

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as error:

        print(
            f"❌ Erreur de lecture : {error}"
        )

        return None


def save_json(data, file_path):

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# PERSONNAGES
# ============================================================

def build_characters(analyses):

    characters = {}

    for analysis in analyses:

        scene = analysis.get(
            "scene"
        )

        for character in analysis.get(
            "characters",
            []
        ):

            role = character.get(
                "role",
                "unknown"
            )

            key = normalize_text(
                role
            )

            if not key:
                continue

            if key not in characters:

                characters[key] = {
                    "id": f"CHAR_{len(characters) + 1:03d}",
                    "name": role,
                    "appearances": [],
                    "descriptions": [],
                    "clothing": [],
                    "actions": []
                }

            entry = characters[key]

            if scene not in entry["appearances"]:
                entry["appearances"].append(scene)

            appearance = character.get(
                "appearance"
            )

            if appearance:
                entry["descriptions"].append(
                    appearance
                )

            clothing = character.get(
                "clothing"
            )

            if clothing:
                entry["clothing"].append(
                    clothing
                )

            actions = character.get(
                "actions"
            )

            if actions:
                entry["actions"].append(
                    actions
                )

    # Dédupliquer
    for character in characters.values():

        character["appearances"] = sorted(
            set(character["appearances"])
        )

        character["descriptions"] = sorted(
            set(character["descriptions"])
        )

        character["clothing"] = sorted(
            set(character["clothing"])
        )

        character["actions"] = sorted(
            set(character["actions"])
        )

    return list(
        characters.values()
    )


# ============================================================
# ENVIRONNEMENTS
# ============================================================

def build_environments(analyses):

    environments = {}

    for analysis in analyses:

        scene = analysis.get(
            "scene"
        )

        environment = analysis.get(
            "environment",
            {}
        )

        location = environment.get(
            "location",
            "unknown"
        )

        key = normalize_text(
            location
        )

        if not key:
            continue

        if key not in environments:

            environments[key] = {
                "id": f"ENV_{len(environments) + 1:03d}",
                "name": location,
                "scenes": [],
                "architecture": [],
                "walls": [],
                "floor": [],
                "background": []
            }

        entry = environments[key]

        if scene not in entry["scenes"]:
            entry["scenes"].append(scene)

        for field in [
            "architecture",
            "walls",
            "floor",
            "background"
        ]:

            value = environment.get(field)

            if value:
                entry[field].append(value)

    # Dédupliquer
    for environment in environments.values():

        environment["scenes"] = sorted(
            set(environment["scenes"])
        )

        for field in [
            "architecture",
            "walls",
            "floor",
            "background"
        ]:

            environment[field] = sorted(
                set(environment[field])
            )

    return list(
        environments.values()
    )


# ============================================================
# OBJETS / PROPS
# ============================================================

def build_props(analyses):

    props = {}

    for analysis in analyses:

        scene = analysis.get(
            "scene"
        )

        for obj in analysis.get(
            "objects",
            []
        ):

            name = obj.get(
                "name",
                "unknown"
            )

            key = normalize_text(
                name
            )

            if not key:
                continue

            if key not in props:

                props[key] = {
                    "id": f"PROP_{len(props) + 1:03d}",
                    "name": name,
                    "scenes": [],
                    "materials": [],
                    "positions": [],
                    "importance": []
                }

            entry = props[key]

            if scene not in entry["scenes"]:
                entry["scenes"].append(scene)

            material = obj.get(
                "material"
            )

            if material:
                entry["materials"].append(
                    material
                )

            position = obj.get(
                "position"
            )

            if position:
                entry["positions"].append(
                    position
                )

            importance = obj.get(
                "importance"
            )

            if importance:
                entry["importance"].append(
                    importance
                )

    # Dédupliquer
    for prop in props.values():

        prop["scenes"] = sorted(
            set(prop["scenes"])
        )

        prop["materials"] = sorted(
            set(prop["materials"])
        )

        prop["positions"] = sorted(
            set(prop["positions"])
        )

        prop["importance"] = sorted(
            set(prop["importance"])
        )

    return list(
        props.values()
    )


# ============================================================
# ASSETS 3D
# ============================================================

def build_assets(analyses):

    assets = {}

    for analysis in analyses:

        reconstruction = analysis.get(
            "3d_reconstruction",
            {}
        )

        for asset in reconstruction.get(
            "important_assets",
            []
        ):

            key = normalize_text(
                asset
            )

            if not key:
                continue

            if key not in assets:

                assets[key] = {
                    "id": f"ASSET_{len(assets) + 1:03d}",
                    "name": asset,
                    "usage_scenes": [],
                    "type": "3D asset",
                    "status": "TO_FIND"
                }

            scene = analysis.get(
                "scene"
            )

            if scene not in assets[key]["usage_scenes"]:
                assets[key]["usage_scenes"].append(
                    scene
                )

    for asset in assets.values():

        asset["usage_scenes"] = sorted(
            set(asset["usage_scenes"])
        )

    return list(
        assets.values()
    )


# ============================================================
# MATÉRIAUX
# ============================================================

def build_materials(analyses):

    materials = {}

    for analysis in analyses:

        reconstruction = analysis.get(
            "3d_reconstruction",
            {}
        )

        for material in reconstruction.get(
            "materials",
            []
        ):

            key = normalize_text(
                material
            )

            if not key:
                continue

            if key not in materials:

                materials[key] = {
                    "id": f"MAT_{len(materials) + 1:03d}",
                    "name": material,
                    "usage_scenes": []
                }

            scene = analysis.get(
                "scene"
            )

            if scene not in materials[key]["usage_scenes"]:
                materials[key]["usage_scenes"].append(
                    scene
                )

    for material in materials.values():

        material["usage_scenes"] = sorted(
            set(material["usage_scenes"])
        )

    return list(
        materials.values()
    )


# ============================================================
# CAMÉRAS
# ============================================================

def build_cameras(analyses):

    cameras = []

    for analysis in analyses:

        camera = analysis.get(
            "camera",
            {}
        )

        cameras.append({

            "scene": analysis.get(
                "scene"
            ),

            "shot_type": camera.get(
                "shot_type"
            ),

            "angle": camera.get(
                "angle"
            ),

            "height": camera.get(
                "height"
            ),

            "composition": camera.get(
                "composition"
            ),

            "perspective": camera.get(
                "perspective"
            ),

            "movement": camera.get(
                "movement"
            ),

            "estimated_focal_length": camera.get(
                "estimated_focal_length"
            )
        })

    return cameras


# ============================================================
# LIGHTING
# ============================================================

def build_lighting(analyses):

    lighting = []

    for analysis in analyses:

        light = analysis.get(
            "lighting",
            {}
        )

        lighting.append({

            "scene": analysis.get(
                "scene"
            ),

            "sources": light.get(
                "sources",
                []
            ),

            "direction": light.get(
                "direction"
            ),

            "intensity": light.get(
                "intensity"
            ),

            "softness": light.get(
                "softness"
            ),

            "color_temperature": light.get(
                "color_temperature"
            ),

            "shadows": light.get(
                "shadows"
            ),

            "mood": light.get(
                "mood"
            )
        })

    return lighting


# ============================================================
# PLAN DE PRODUCTION
# ============================================================

def build_production_plan(
    characters,
    environments,
    props,
    assets,
    materials
):

    tasks = []

    # Personnages
    for character in characters:

        tasks.append({

            "category": "CHARACTER",

            "id": character["id"],

            "name": character["name"],

            "action": "CREATE_OR_FIND",

            "priority": "HIGH"
        })

    # Environnements
    for environment in environments:

        tasks.append({

            "category": "ENVIRONMENT",

            "id": environment["id"],

            "name": environment["name"],

            "action": "CREATE",

            "priority": "HIGH"
        })

    # Props
    for prop in props:

        tasks.append({

            "category": "PROP",

            "id": prop["id"],

            "name": prop["name"],

            "action": "CREATE_OR_FIND",

            "priority": "MEDIUM"
        })

    # Assets
    for asset in assets:

        tasks.append({

            "category": "ASSET",

            "id": asset["id"],

            "name": asset["name"],

            "action": "SEARCH_ASSET_LIBRARY",

            "priority": "HIGH"
        })

    # Matériaux
    for material in materials:

        tasks.append({

            "category": "MATERIAL",

            "id": material["id"],

            "name": material["name"],

            "action": "CREATE_MATERIAL",

            "priority": "MEDIUM"
        })

    return tasks


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

def main():

    print("\n" + "=" * 60)

    print(
        "🎬 PLAN DE PRODUCTION 3D"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # CHARGER LE FILM
    # --------------------------------------------------------

    film = load_json(
        INPUT_FILE
    )

    if film is None:
        return

    analyses = film.get(
        "scenes",
        []
    )

    if not analyses:

        print(
            "❌ Aucune scène trouvée dans film_analysis.json"
        )

        return

    print(
        f"\n🎬 {len(analyses)} scènes chargées"
    )

    # --------------------------------------------------------
    # CONSTRUIRE LES DONNÉES
    # --------------------------------------------------------

    print(
        "\n🔄 Construction du catalogue..."
    )

    characters = build_characters(
        analyses
    )

    environments = build_environments(
        analyses
    )

    props = build_props(
        analyses
    )

    assets = build_assets(
        analyses
    )

    materials = build_materials(
        analyses
    )

    cameras = build_cameras(
        analyses
    )

    lighting = build_lighting(
        analyses
    )

    production_tasks = build_production_plan(
        characters,
        environments,
        props,
        assets,
        materials
    )

    # --------------------------------------------------------
    # CRÉER LE DOSSIER
    # --------------------------------------------------------

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # SAUVEGARDER CHAQUE CATÉGORIE
    # --------------------------------------------------------

    save_json(
        characters,
        OUTPUT_FOLDER / "characters.json"
    )

    save_json(
        environments,
        OUTPUT_FOLDER / "environments.json"
    )

    save_json(
        props,
        OUTPUT_FOLDER / "props.json"
    )

    save_json(
        assets,
        OUTPUT_FOLDER / "assets.json"
    )

    save_json(
        materials,
        OUTPUT_FOLDER / "materials.json"
    )

    save_json(
        cameras,
        OUTPUT_FOLDER / "cameras.json"
    )

    save_json(
        lighting,
        OUTPUT_FOLDER / "lighting.json"
    )

    save_json(
        production_tasks,
        OUTPUT_FOLDER / "production_plan.json"
    )

    # --------------------------------------------------------
    # RÉSUMÉ
    # --------------------------------------------------------

    print("\n" + "=" * 60)

    print(
        "✅ PLAN DE PRODUCTION CRÉÉ"
    )

    print("=" * 60)

    print(
        f"👤 Personnages uniques : "
        f"{len(characters)}"
    )

    print(
        f"🏛️ Environnements uniques : "
        f"{len(environments)}"
    )

    print(
        f"📦 Props uniques : "
        f"{len(props)}"
    )

    print(
        f"📐 Assets 3D uniques : "
        f"{len(assets)}"
    )

    print(
        f"🧱 Matériaux uniques : "
        f"{len(materials)}"
    )

    print(
        f"🎥 Configurations caméra : "
        f"{len(cameras)}"
    )

    print(
        f"💡 Configurations lumière : "
        f"{len(lighting)}"
    )

    print(
        f"📋 Tâches de production : "
        f"{len(production_tasks)}"
    )

    print(
        f"\n📁 Dossier créé : "
        f"{OUTPUT_FOLDER}"
    )

    print("=" * 60)


# ============================================================
# LANCEMENT
# ============================================================

if __name__ == "__main__":

    main()
