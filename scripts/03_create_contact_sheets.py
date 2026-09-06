from pathlib import Path

from PIL import Image


# ============================================================
# CONFIGURATION
# ============================================================

SCENES_FOLDER = Path(
    "output/scenes"
)

THUMBNAIL_WIDTH = 320
THUMBNAIL_HEIGHT = 180

MARGIN = 20

COLUMNS = 3
ROWS = 2


# ============================================================
# CONTACT SHEET
# ============================================================

def create_contact_sheet(scene_folder):

    image_files = sorted(
        scene_folder.glob(
            "frame_*.jpg"
        )
    )

    if not image_files:

        print(
            f"⚠️ Aucune image : "
            f"{scene_folder}"
        )

        return False

    images = []

    for image_file in image_files:

        try:

            image = Image.open(
                image_file
            )

            images.append(
                image.copy()
            )

            image.close()

        except Exception as error:

            print(
                f"⚠️ Erreur : "
                f"{image_file}"
            )

            print(
                f"   {error}"
            )

    if not images:

        return False

    sheet_width = (
        COLUMNS
        * THUMBNAIL_WIDTH
        + (COLUMNS + 1)
        * MARGIN
    )

    sheet_height = (
        ROWS
        * THUMBNAIL_HEIGHT
        + (ROWS + 1)
        * MARGIN
    )

    sheet = Image.new(
        "RGB",
        (
            sheet_width,
            sheet_height
        ),
        "white"
    )

    for index, image in enumerate(
        images
    ):

        if index >= COLUMNS * ROWS:

            break

        image.thumbnail(
            (
                THUMBNAIL_WIDTH,
                THUMBNAIL_HEIGHT
            )
        )

        column = index % COLUMNS
        row = index // COLUMNS

        x = (
            MARGIN
            + column
            * THUMBNAIL_WIDTH
        )

        y = (
            MARGIN
            + row
            * THUMBNAIL_HEIGHT
        )

        sheet.paste(
            image,
            (x, y)
        )

    output_file = (
        scene_folder
        / "contact_sheet.jpg"
    )

    sheet.save(
        output_file,
        quality=95
    )

    print(
        f"   ✓ {output_file}"
    )

    return True


# ============================================================
# TOUTES LES SCÈNES
# ============================================================

def create_all_contact_sheets():

    print()
    print("=" * 60)
    print("📋 CRÉATION DES PLANCHES CONTACT")
    print("=" * 60)

    scene_folders = sorted(
        folder
        for folder in SCENES_FOLDER.glob(
            "scene_*"
        )
        if folder.is_dir()
    )

    print(
        f"\n✓ {len(scene_folders)} scènes trouvées"
    )

    success = 0

    for scene_folder in scene_folders:

        print(
            f"\n🎬 {scene_folder.name}"
        )

        if create_contact_sheet(
            scene_folder
        ):

            success += 1

    print()
    print("=" * 60)

    print(
        f"✅ Planches créées : "
        f"{success}/{len(scene_folders)}"
    )

    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    create_all_contact_sheets()