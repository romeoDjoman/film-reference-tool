import json
import re
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = Path(
    "output/preproduction/assets_classified.json"
)

OUTPUT_FILE = Path(
    "output/preproduction/asset_library.json"
)


# ============================================================
# NORMALISATION
# ============================================================

def normalize_name(name):
    """
    Transforme le nom en identifiant exploitable.
    """

    name = str(name).lower().strip()

    # Remplacer les caractères spéciaux
    name = re.sub(
        r"[^a-z0-9]+",
        "_",
        name
    )

    # Supprimer les _ multiples
    name = re.sub(
        r"_+",
        "_",
        name
    )

    return name.strip("_")


# ============================================================
# REQUÊTE DE RECHERCHE
# ============================================================

def create_search_query(asset):
    """
    Crée automatiquement une requête utilisable
    pour rechercher un asset 3D.
    """

    name = asset.get(
        "name",
        ""
    )

    category = asset.get(
        "category",
        ""
    )

    name_normalized = name.replace(
        "_",
        " "
    )

    category_normalized = category.replace(
        "_",
        " "
    ).lower()

    # Requête générale
    query = (
        f"{name_normalized} "
        f"{category_normalized} "
        f"3D model Blender"
    )

    return query


# ============================================================
# FORMAT
# ============================================================

def determine_format(asset):

    category = asset.get(
        "category",
        ""
    )

    if category == "MATERIAL":

        return [
            "BLEND",
            "PNG",
            "JPG",
            "EXR"
        ]

    return [
        "BLEND",
        "FBX",
        "OBJ",
        "GLB",
        "GLTF"
    ]


# ============================================================
# CONSTRUIRE UN ASSET
# ============================================================

def create_library_asset(
    asset,
    index
):

    asset_id = asset.get(
        "id",
        f"ASSET_{index:04d}"
    )

    name = asset.get(
        "name",
        "unknown"
    )

    category = asset.get(
        "category",
        "OTHER"
    )

    method = asset.get(
        "production_method",
        "SEARCH"
    )

    priority = asset.get(
        "priority",
        "MEDIUM"
    )

    usage_scenes = asset.get(
        "usage_scenes",
        []
    )

    library_asset = {

        "asset_id": asset_id,

        "name": name,

        "slug": normalize_name(
            name
        ),

        "category": category,

        "production_method": method,

        "priority": priority,

        "status": "MISSING",

        "blender_ready": False,

        "usage_scenes": usage_scenes,

        "search": {

            "query": create_search_query(
                asset
            ),

            "formats": determine_format(
                asset
            )
        },

        "source": {

            "provider": None,

            "url": None,

            "license": None
        },

        "files": {

            "local_file": None,

            "blend_file": None,

            "texture_files": []
        },

        "blender": {

            "collection": None,

            "object": None,

            "material": None
        },

        "production": {

            "needs_modeling": False,

            "needs_texturing": False,

            "needs_rigging": False,

            "needs_animation": False
        }
    }

    # --------------------------------------------------------
    # Déterminer les besoins de production
    # --------------------------------------------------------

    if method in [
        "PROCEDURAL",
        "PROCEDURAL_OR_EXISTING"
    ]:

        library_asset[
            "production"
        ][
            "needs_modeling"
        ] = True

    if category in [
        "CHARACTER",
        "CHARACTER_EQUIPMENT"
    ]:

        library_asset[
            "production"
        ][
            "needs_texturing"
        ] = True

    if category == "CHARACTER":

        library_asset[
            "production"
        ][
            "needs_rigging"
        ] = True

        library_asset[
            "production"
        ][
            "needs_animation"
        ] = True

    return library_asset


# ============================================================
# CHARGEMENT
# ============================================================

def load_assets():

    if not INPUT_FILE.exists():

        print(
            f"❌ Fichier introuvable : "
            f"{INPUT_FILE}"
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
            f"❌ Erreur de lecture : "
            f"{error}"
        )

        return None


# ============================================================
# CONSTRUCTION DE LA BIBLIOTHÈQUE
# ============================================================

def build_library(assets):

    library = []

    for index, asset in enumerate(
        assets,
        start=1
    ):

        library_asset = create_library_asset(
            asset,
            index
        )

        library.append(
            library_asset
        )

    return library


# ============================================================
# STATISTIQUES
# ============================================================

def show_statistics(library):

    categories = {}

    statuses = {}

    methods = {}

    for asset in library:

        category = asset[
            "category"
        ]

        status = asset[
            "status"
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

        statuses[status] = (
            statuses.get(
                status,
                0
            ) + 1
        )

        methods[method] = (
            methods.get(
                method,
                0
            ) + 1
        )

    print(
        "\n📊 CATÉGORIES"
    )

    for key, value in sorted(
        categories.items()
    ):

        print(
            f"   {key}: {value}"
        )

    print(
        "\n🛠️ MÉTHODES"
    )

    for key, value in sorted(
        methods.items()
    ):

        print(
            f"   {key}: {value}"
        )

    print(
        "\n📦 STATUTS"
    )

    for key, value in sorted(
        statuses.items()
    ):

        print(
            f"   {key}: {value}"
        )


# ============================================================
# SAUVEGARDE
# ============================================================

def save_library(library):

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
            library,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

def main():

    print(
        "\n" + "=" * 60
    )

    print(
        "📚 ASSET LIBRARY MANAGER"
    )

    print(
        "=" * 60
    )

    assets = load_assets()

    if assets is None:
        return

    print(
        f"\n📐 {len(assets)} assets chargés"
    )

    print(
        "\n🔄 Construction de la bibliothèque..."
    )

    library = build_library(
        assets
    )

    show_statistics(
        library
    )

    save_library(
        library
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "✅ BIBLIOTHÈQUE D'ASSETS CRÉÉE"
    )

    print(
        "=" * 60
    )

    print(
        f"\n📚 Assets enregistrés : "
        f"{len(library)}"
    )

    print(
        f"💾 Fichier : "
        f"{OUTPUT_FILE}"
    )

    print(
        "\n" + "=" * 60
    )


# ============================================================
# LANCEMENT
# ============================================================

if __name__ == "__main__":

    main()