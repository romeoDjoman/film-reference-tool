from pathlib import Path
import shutil
import ast
import re
from datetime import datetime


# ============================================================
# CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parent

DRY_RUN = True
# True  = montre ce qui va être fait sans modifier
# False = effectue réellement la migration


# ============================================================
# FICHIERS À DÉPLACER
# ============================================================

SCRIPT_MOVES = {

    "analyse_film.py":
        "scripts/analyse_film.py",

    "analyse_scene_ia.py":
        "scripts/analyse_scene_ia.py",

    "asset_library.py":
        "scripts/asset_library.py",

    "asset_manager.py":
        "scripts/asset_manager.py",

    "classify_assets.py":
        "scripts/classify_assets.py",

    "fusionner_analyses.py":
        "scripts/fusionner_analyses.py",

    "production_plan.py":
        "scripts/production_plan.py",

    "setup_assets.py":
        "scripts/setup_assets.py",
}


# ============================================================
# TESTS
# ============================================================

TEST_MOVES = {

    "test_vision.py":
        "tests/test_vision.py",
}


# ============================================================
# AUTRES FICHIERS
# ============================================================

OTHER_MOVES = {

    "image_test.jpg":
        "tests/data/image_test.jpg",

    "my-script.rtf":
        "docs/archive/my-script.rtf",
}


# ============================================================
# DOSSIERS À CRÉER
# ============================================================

DIRECTORIES = [

    "scripts",

    "tests",
    "tests/data",

    "docs",
    "docs/archive",

    "blender_scripts",
    "blender_scripts/01_generate_assets",
    "blender_scripts/02_import_assets",
    "blender_scripts/03_build_environment",
    "blender_scripts/04_build_scene",
    "blender_scripts/05_camera",
    "blender_scripts/06_lighting",
    "blender_scripts/07_render",
]


# ============================================================
# BACKUP
# ============================================================

def create_backup():

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup = ROOT / f"_backup_before_reorganization_{timestamp}"

    print()
    print("=" * 60)
    print("💾 CRÉATION DU BACKUP")
    print("=" * 60)

    if DRY_RUN:

        print(
            f"[DRY RUN] Backup prévu : {backup}"
        )

        return backup

    shutil.copytree(
        ROOT,
        backup,
        ignore=shutil.ignore_patterns(
            ".venv",
            "__pycache__",
            "_backup_*"
        )
    )

    print(
        f"✓ Backup créé : {backup}"
    )

    return backup


# ============================================================
# CRÉATION DES DOSSIERS
# ============================================================

def create_directories():

    print()
    print("=" * 60)
    print("📁 CRÉATION DES DOSSIERS")
    print("=" * 60)

    for directory in DIRECTORIES:

        path = ROOT / directory

        if path.exists():

            print(
                f"✓ Existe déjà : {directory}"
            )

        else:

            print(
                f"+ Création : {directory}"
            )

            if not DRY_RUN:
                path.mkdir(
                    parents=True,
                    exist_ok=True
                )


# ============================================================
# ANALYSE DES IMPORTS
# ============================================================

def analyse_imports():

    print()
    print("=" * 60)
    print("🔍 ANALYSE DES IMPORTS")
    print("=" * 60)

    python_files = list(
        ROOT.glob("*.py")
    )

    for file in python_files:

        if file.name == Path(__file__).name:
            continue

        print()
        print(f"📄 {file.name}")

        try:

            source = file.read_text(
                encoding="utf-8"
            )

            tree = ast.parse(source)

        except Exception as error:

            print(
                f"⚠️ Impossible d'analyser : {error}"
            )

            continue

        imports = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:

                    imports.append(
                        alias.name
                    )

            elif isinstance(
                node,
                ast.ImportFrom
            ):

                if node.module:

                    imports.append(
                        node.module
                    )

        if imports:

            for item in sorted(set(imports)):

                print(
                    f"   import → {item}"
                )

        else:

            print(
                "   Aucun import local détecté"
            )


# ============================================================
# RECHERCHE DES CHEMINS
# ============================================================

def analyse_paths():

    print()
    print("=" * 60)
    print("🔍 RECHERCHE DES CHEMINS")
    print("=" * 60)

    python_files = list(
        ROOT.glob("*.py")
    )

    patterns = [

        r'["\']([^"\']*output/[^"\']*)["\']',

        r'["\']([^"\']*assets/[^"\']*)["\']',

        r'["\']([^"\']*videos/[^"\']*)["\']',

        r'["\']([^"\']*blender_scripts/[^"\']*)["\']',

        r'["\']([^"\']*docs/[^"\']*)["\']',

    ]

    for file in python_files:

        if file.name == Path(__file__).name:
            continue

        try:

            source = file.read_text(
                encoding="utf-8"
            )

        except Exception:
            continue

        found = []

        for pattern in patterns:

            matches = re.findall(
                pattern,
                source
            )

            found.extend(matches)

        if found:

            print()
            print(f"📄 {file.name}")

            for path in sorted(set(found)):

                print(
                    f"   → {path}"
                )


# ============================================================
# DÉPLACEMENT D'UN FICHIER
# ============================================================

def move_file(source_relative, destination_relative):

    source = ROOT / source_relative
    destination = ROOT / destination_relative

    if not source.exists():

        print(
            f"⚠️ Source absente : {source_relative}"
        )

        return False

    if destination.exists():

        print(
            f"⚠️ Destination existe déjà : "
            f"{destination_relative}"
        )

        return False

    print()
    print(
        f"📦 {source_relative}"
    )

    print(
        f"   ↓"
    )

    print(
        f"   {destination_relative}"
    )

    if not DRY_RUN:

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.move(
            str(source),
            str(destination)
        )

    return True


# ============================================================
# MIGRATION
# ============================================================

def migrate():

    print()
    print("=" * 60)
    print("🚚 MIGRATION DES FICHIERS")
    print("=" * 60)

    all_moves = {}

    all_moves.update(
        SCRIPT_MOVES
    )

    all_moves.update(
        TEST_MOVES
    )

    all_moves.update(
        OTHER_MOVES
    )

    success = 0
    errors = 0

    for source, destination in all_moves.items():

        result = move_file(
            source,
            destination
        )

        if result:

            success += 1

        else:

            errors += 1

    print()
    print(
        f"✓ Fichiers préparés : {success}"
    )

    print(
        f"❌ Problèmes : {errors}"
    )


# ============================================================
# VÉRIFICATION FINALE
# ============================================================

def verify():

    print()
    print("=" * 60)
    print("🔎 VÉRIFICATION")
    print("=" * 60)

    expected_files = {

        "scripts/analyse_film.py",
        "scripts/analyse_scene_ia.py",
        "scripts/asset_library.py",
        "scripts/asset_manager.py",
        "scripts/classify_assets.py",
        "scripts/fusionner_analyses.py",
        "scripts/production_plan.py",
        "scripts/setup_assets.py",

        "tests/test_vision.py",

    }

    missing = []

    for file in expected_files:

        path = ROOT / file

        if path.exists():

            print(
                f"✓ {file}"
            )

        else:

            print(
                f"❌ MANQUANT : {file}"
            )

            missing.append(file)

    print()

    if missing:

        print(
            f"❌ {len(missing)} fichier(s) manquant(s)"
        )

    else:

        print(
            "✅ Tous les scripts principaux sont présents"
        )


# ============================================================
# RAPPORT
# ============================================================

def print_final_report():

    print()
    print("=" * 60)
    print("📊 RAPPORT")
    print("=" * 60)

    print()

    if DRY_RUN:

        print(
            "⚠️ MODE DRY RUN"
        )

        print(
            "Aucun fichier n'a été déplacé."
        )

        print()

        print(
            "Si le résultat te convient :"
        )

        print(
            "DRY_RUN = False"
        )

        print(
            "puis relance le programme."
        )

    else:

        print(
            "✅ RÉORGANISATION TERMINÉE"
        )

        print()
        print(
            "Les fichiers ont été déplacés."
        )

        print(
            "Le backup peut être utilisé pour revenir en arrière."
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("🎬 FILM REFERENCE TOOL")
    print("RÉORGANISATION DU PROJET")
    print("=" * 60)

    print()

    if DRY_RUN:

        print(
            "⚠️ MODE SIMULATION ACTIVÉ"
        )

    else:

        print(
            "🚨 MODE MODIFICATION ACTIVÉ"
        )

    analyse_imports()

    analyse_paths()

    create_backup()

    create_directories()

    migrate()

    verify()

    print_final_report()


if __name__ == "__main__":

    main()