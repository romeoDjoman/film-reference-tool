from pathlib import Path


BASE_DIR = Path("assets")

FOLDERS = [
    "downloaded",
    "generated",
    "blend",
    "textures",
    "materials",
    "characters",
    "environments",
    "props",
    "architecture",
]


def create_folders():
    print("\n" + "=" * 60)
    print("📁 PRÉPARATION DE LA BIBLIOTHÈQUE 3D")
    print("=" * 60)

    for folder in FOLDERS:
        path = BASE_DIR / folder
        path.mkdir(parents=True, exist_ok=True)
        print(f"✓ {path}")

    print("\n" + "=" * 60)
    print("✅ STRUCTURE DES ASSETS CRÉÉE")
    print("=" * 60)


def main():
    create_folders()


if __name__ == "__main__":
    main()