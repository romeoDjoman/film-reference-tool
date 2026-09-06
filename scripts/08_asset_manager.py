import json
import re
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = Path(
    "output/preproduction/assets.json"
)

OUTPUT_FILE = Path(
    "output/preproduction/assets_manager.json"
)


# ============================================================
# NORMALISATION
# ============================================================

def normalize(text):

    if not text:
        return ""

    text = str(text).lower().strip()

    return re.sub(
        r"\s+",
        " ",
        text
    )


# ============================================================
# CLASSIFICATION
# ============================================================

def classify_asset(name):

    text = normalize(name)

    # --------------------------------------------------------
    # PERSONNAGES / ÉQUIPEMENTS
    # --------------------------------------------------------

    character_keywords = [
        "soldier",
        "roman soldier",
        "armor",
        "armour",
        "helmet",
        "guard",
        "warrior",
        "prisoner",
        "character",
        "person"
    ]

    for keyword in character_keywords:

        if keyword in text:

            return {
                "category": "CHARACTER",
                "strategy": "EXISTING_ASSET",
                "priority": "HIGH"
            }

    # --------------------------------------------------------
    # ENVIRONNEMENTS
    # --------------------------------------------------------

    environment_keywords = [
        "wall",
        "stone wall",
        "floor",
        "ground",
        "courtyard",
        "prison",
        "room",
        "building",
        "architecture",
        "stone",
        "column",
        "pillar"
    ]

    for keyword in environment_keywords:

        if keyword in text:

            return {
                "category": "ENVIRONMENT",
                "strategy": "PROCEDURAL_OR_EXISTING",
                "priority": "HIGH"
            }

    # --------------------------------------------------------
    # OBJETS / PROPS
    # --------------------------------------------------------

    prop_keywords = [
        "table",
        "chair",
        "jug",
        "cup",
        "scroll",
        "tablet",
        "quill",
        "chain",
        "chains",
        "rope",
        "weapon",
        "sword",
        "whip",
        "slab",
        "pottery",
        "clay",
        "crate",
        "wood"
    ]

    for keyword in prop_keywords:

        if keyword in text:

            return {
                "category": "PROP",
                "strategy": "EXISTING_ASSET",
                "priority": "MEDIUM"
            }

    # --------------------------------------------------------
    # MATÉRIAUX / SURFACES
    # --------------------------------------------------------

    material_keywords = [
        "leather",
        "metal",
        "bronze",
        "iron",
        "wood",
        "ceramic",
        "clay",
        "stone",
        "blood",
        "parchment",
        "paper",
        "fabric"
    ]

    for keyword in material_keywords:

        if keyword in text:

            return {
                "category": "MATERIAL",
                "strategy": "PROCEDURAL",
                "priority": "MEDIUM"
            }

    # --------------------------------------------------------
    # PAR DÉFAUT
    # --------------------------------------------------------

    return {
        "category": "OTHER",
        "strategy": "SEARCH_FIRST",
        "priority": "LOW"
    }


# ============================================================
# CHARGEMENT
# ============================================================

def load_assets():

    if not INPUT_FILE.exists():

        print(
            f"❌ Fichier introuvable : {INPUT_FILE}"
        )

        return None

    try:

        with open(
            INPUT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as error:

        print(
            f"❌ Erreur de lecture : {error}"
        )

        return None


# ============================================================
# CONSTRUCTION
# ============================================================

def build_asset_manager(assets):

    result = []

    for asset in assets:

        name = asset.get(
            "name",
            "unknown"
        )

        classification = classify_asset(
            name
        )

        managed_asset = {

            "id": asset.get(
                "id"
            ),

            "name": name,

            "category": classification[
                "category"
            ],

            "strategy": classification[
                "strategy"
            ],

            "priority": classification[
                "priority"
            ],

            "status": "TO_PROCESS",

            "blender_ready": False,

            "usage_scenes": asset.get(
                "usage_scenes",
                []
            ),

            "source": None,

            "local_file": None,

            "blender_object": None
        }

        result.append(
            managed_asset
        )

    return result


# ============================================================
# SAUVEGARDE
# ============================================================

def save_result(data):

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
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
# STATISTIQUES
# ============================================================

def print_statistics(assets):

    categories = {}

    strategies = {}

    for asset in assets:

        category = asset[
            "category"
        ]

        strategy = asset[
            "strategy"
        ]

        categories[category] = (
            categories.get(
                category,
                0
            ) + 1
        )

        strategies[strategy] = (
            strategies.get(
                strategy,
                0
            ) + 1
        )

    print("\n📊 CATÉGORIES")

    for category, count in sorted(
        categories.items()
    ):

        print(
            f"   {category}: {count}"
        )

    print("\n🛠️ STRATÉGIES")

    for strategy, count in sorted(
        strategies.items()
    ):

        print(
            f"   {strategy}: {count}"
        )


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

def main():

    print("\n" + "=" * 60)

    print(
        "🎬 ASSET MANAGER"
    )

    print("=" * 60)

    assets = load_assets()

    if assets is None:
        return

    print(
        f"\n📐 {len(assets)} assets chargés"
    )

    print(
        "\n🔄 Classification des assets..."
    )

    managed_assets = build_asset_manager(
        assets
    )

    save_result(
        managed_assets
    )

    print_statistics(
        managed_assets
    )

    print("\n" + "=" * 60)

    print(
        "✅ ASSET MANAGER CRÉÉ"
    )

    print("=" * 60)

    print(
        f"\n💾 Fichier : {OUTPUT_FILE}"
    )

    print("=" * 60)


# ============================================================
# LANCEMENT
# ============================================================

if __name__ == "__main__":

    main()