import json
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = Path(
    "output/preproduction/assets_manager.json"
)

OUTPUT_FILE = Path(
    "output/preproduction/assets_classified.json"
)


# ============================================================
# CLASSIFICATION
# ============================================================

def classify_asset(asset):

    name = asset.get("name", "").lower()

    # --------------------------------------------------------
    # CHARACTER EQUIPMENT
    # --------------------------------------------------------

    equipment_keywords = [
        "armor",
        "armour",
        "helmet",
        "shield",
        "sword",
        "spear",
        "weapon",
        "leather armor",
        "roman armor"
    ]

    if any(
        keyword in name
        for keyword in equipment_keywords
    ):

        return {
            "category": "CHARACTER_EQUIPMENT",
            "production_method": "EXISTING_ASSET",
            "priority": "HIGH"
        }

    # --------------------------------------------------------
    # CHARACTER
    # --------------------------------------------------------

    character_keywords = [
        "soldier",
        "guard",
        "warrior",
        "prisoner",
        "executioner",
        "torturer",
        "roman",
        "victim",
        "character",
        "man",
        "woman",
        "person"
    ]

    if any(
        keyword in name
        for keyword in character_keywords
    ):

        return {
            "category": "CHARACTER",
            "production_method": "EXISTING_OR_GENERATED",
            "priority": "HIGH"
        }

    # --------------------------------------------------------
    # ARCHITECTURE
    # --------------------------------------------------------

    architecture_keywords = [
        "wall",
        "stone wall",
        "pillar",
        "column",
        "arch",
        "door",
        "window",
        "building",
        "fortification",
        "architecture"
    ]

    if any(
        keyword in name
        for keyword in architecture_keywords
    ):

        return {
            "category": "ARCHITECTURE",
            "production_method": "PROCEDURAL_OR_EXISTING",
            "priority": "HIGH"
        }

    # --------------------------------------------------------
    # ENVIRONMENT
    # --------------------------------------------------------

    environment_keywords = [
        "courtyard",
        "prison",
        "room",
        "cell",
        "street",
        "interior",
        "exterior",
        "environment",
        "ground",
        "floor"
    ]

    if any(
        keyword in name
        for keyword in environment_keywords
    ):

        return {
            "category": "ENVIRONMENT",
            "production_method": "PROCEDURAL_OR_EXISTING",
            "priority": "HIGH"
        }

    # --------------------------------------------------------
    # MATERIAL
    # --------------------------------------------------------

    material_keywords = [
        "stone",
        "wood",
        "leather",
        "metal",
        "iron",
        "bronze",
        "clay",
        "ceramic",
        "fabric",
        "blood",
        "parchment",
        "paper",
        "material",
        "texture"
    ]

    if any(
        keyword in name
        for keyword in material_keywords
    ):

        return {
            "category": "MATERIAL",
            "production_method": "PROCEDURAL",
            "priority": "MEDIUM"
        }

    # --------------------------------------------------------
    # VFX
    # --------------------------------------------------------

    vfx_keywords = [
        "blood",
        "smoke",
        "fire",
        "dust",
        "fog",
        "particle",
        "vfx"
    ]

    if any(
        keyword in name
        for keyword in vfx_keywords
    ):

        return {
            "category": "VFX",
            "production_method": "PROCEDURAL_OR_SHADER",
            "priority": "MEDIUM"
        }

    # --------------------------------------------------------
    # PROP
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
        "whip",
        "slab",
        "pot",
        "crate",
        "box",
        "bowl",
        "torch",
        "lamp"
    ]

    if any(
        keyword in name
        for keyword in prop_keywords
    ):

        return {
            "category": "PROP",
            "production_method": "EXISTING_OR_PROCEDURAL",
            "priority": "MEDIUM"
        }

    # --------------------------------------------------------
    # OTHER
    # --------------------------------------------------------

    return {
        "category": "OTHER",
        "production_method": "SEARCH",
        "priority": "LOW"
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n" + "=" * 60)

    print(
        "🧠 CLASSIFICATION INTELLIGENTE DES ASSETS"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # CHARGER
    # --------------------------------------------------------

    if not INPUT_FILE.exists():

        print(
            f"\n❌ Fichier introuvable : {INPUT_FILE}"
        )

        return

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        assets = json.load(file)

    print(
        f"\n📐 {len(assets)} assets chargés"
    )

    # --------------------------------------------------------
    # CLASSIFIER
    # --------------------------------------------------------

    classified_assets = []

    for asset in assets:

        classification = classify_asset(
            asset
        )

        classified_asset = {
            **asset,
            **classification,

            "status": "TO_PROCESS",

            "blender_ready": False,

            "source": None,

            "local_file": None,

            "blender_object": None
        }

        classified_assets.append(
            classified_asset
        )

    # --------------------------------------------------------
    # STATISTIQUES
    # --------------------------------------------------------

    categories = {}

    methods = {}

    for asset in classified_assets:

        category = asset[
            "category"
        ]

        method = asset[
            "production_method"
        ]

        categories[category] = (
            categories.get(
                category,
                0
            ) + 1
        )

        methods[method] = (
            methods.get(
                method,
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

    print("\n🛠️ MÉTHODES DE PRODUCTION")

    for method, count in sorted(
        methods.items()
    ):

        print(
            f"   {method}: {count}"
        )

    # --------------------------------------------------------
    # SAUVEGARDER
    # --------------------------------------------------------

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
            classified_assets,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n" + "=" * 60)

    print(
        "✅ CLASSIFICATION TERMINÉE"
    )

    print("=" * 60)

    print(
        f"\n💾 Fichier créé :"
    )

    print(
        f"   {OUTPUT_FILE}"
    )

    print("=" * 60)


# ============================================================
# LANCEMENT
# ============================================================

if __name__ == "__main__":

    main()