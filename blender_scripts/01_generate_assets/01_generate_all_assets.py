import subprocess
import sys
from pathlib import Path


# ============================================================
# CHEMINS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BLENDER_EXECUTABLE = Path(
    "/Applications/Blender.app/Contents/MacOS/Blender"
)

ASSET_SCRIPTS = PROJECT_ROOT / "blender_scripts/01_generate_assets"

REPORT_FILE = (
    PROJECT_ROOT /
    "output/preproduction/generated_assets_report.txt"
)


# ============================================================
# RECETTES VALIDÉES
# ============================================================

ASSET_RECIPES = [
    {
        "name": "Mur romain V3",
        "script": (
            ASSET_SCRIPTS /
            "03_generate_stone_wall_v3.py"
        ),
        "output": (
            PROJECT_ROOT /
            "assets/generated/roman_stone_wall_v3.blend"
        ),
    },
    {
        "name": "Pavage romain",
        "script": (
            ASSET_SCRIPTS /
            "04_generate_roman_paving.py"
        ),
        "output": (
            PROJECT_ROOT /
            "assets/generated/roman_paving.blend"
        ),
    },
    {
        "name": "Table romaine en bois",
        "script": (
            ASSET_SCRIPTS /
            "05_generate_roman_wooden_table.py"
        ),
        "output": (
            PROJECT_ROOT /
            "assets/generated/roman_wooden_table.blend"
        ),
    },
        {
        "name": "Grandes portes romaines",
        "script": (
            ASSET_SCRIPTS /
            "06_generate_roman_double_doors.py"
        ),
        "output": (
            PROJECT_ROOT /
            "assets/generated/roman_double_doors.blend"
        ),
    }
]


# ============================================================
# GÉNÉRATION
# ============================================================

def generate_asset(recipe):
    name = recipe["name"]
    script = recipe["script"]
    output = recipe["output"]

    print()
    print("=" * 60)
    print(f"🏗️ GÉNÉRATION : {name}")
    print("=" * 60)

    if not script.exists():
        return (
            False,
            f"Script introuvable : {script}"
        )

    command = [
        str(BLENDER_EXECUTABLE),
        "--background",
        "--python",
        str(script),
    ]

    result = subprocess.run(
        command,
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        return (
            False,
            result.stdout +
            "\n" +
            result.stderr
        )

    if not output.exists():
        return (
            False,
            f"Le fichier attendu n'a pas été créé : {output}"
        )

    file_size_kb = output.stat().st_size // 1024

    return (
        True,
        f"Créé : {output.name} ({file_size_kb} Ko)"
    )


# ============================================================
# RAPPORT
# ============================================================

def save_report(results):
    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    lines = [
        "=" * 60,
        "RAPPORT DE GÉNÉRATION DES ASSETS",
        "=" * 60,
        "",
    ]

    success_count = 0

    for name, success, message in results:
        status = "✅ OK" if success else "❌ ERREUR"

        lines.append(
            f"{status} — {name}"
        )

        lines.append(
            f"   {message}"
        )

        lines.append("")

        if success:
            success_count += 1

    lines.extend([
        "=" * 60,
        (
            f"Résultat : {success_count}/"
            f"{len(results)} assets générés"
        ),
        "=" * 60,
    ])

    REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("🏛️ GÉNÉRATEUR D'ASSETS BLENDER")
    print("=" * 60)

    if not BLENDER_EXECUTABLE.exists():
        raise FileNotFoundError(
            "Exécutable Blender introuvable : "
            f"{BLENDER_EXECUTABLE}"
        )

    results = []

    for recipe in ASSET_RECIPES:
        success, message = generate_asset(
            recipe
        )

        status = "✅" if success else "❌"

        print(f"{status} {recipe['name']}")
        print(message)

        results.append(
            (
                recipe["name"],
                success,
                message,
            )
        )

    save_report(results)

    success_count = sum(
        success
        for _, success, _ in results
    )

    print()
    print("=" * 60)
    print(
        f"✅ {success_count}/"
        f"{len(results)} assets générés"
    )
    print(f"📄 Rapport : {REPORT_FILE}")
    print("=" * 60)

    if success_count != len(results):
        sys.exit(1)


main()