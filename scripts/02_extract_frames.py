import csv
from pathlib import Path

import cv2


# ============================================================
# CONFIGURATION
# ============================================================

VIDEO = Path(
    "videos/passion_christ_flagellation.mp4"
)

SCENES_CSV = Path(
    "output/scenes.csv"
)

OUTPUT_FOLDER = Path(
    "output/scenes"
)

IMAGES_PER_SCENE = 5


# ============================================================
# TIME
# ============================================================

def timecode_to_seconds(timecode):

    hours, minutes, seconds = timecode.split(":")

    return (
        int(hours) * 3600
        + int(minutes) * 60
        + float(seconds)
    )


# ============================================================
# EXTRACTION
# ============================================================

def extract_frames():

    print()
    print("=" * 60)
    print("🖼️ EXTRACTION DES IMAGES")
    print("=" * 60)

    if not VIDEO.exists():

        print(
            f"❌ Vidéo introuvable : {VIDEO}"
        )

        return False

    if not SCENES_CSV.exists():

        print(
            f"❌ CSV introuvable : {SCENES_CSV}"
        )

        print(
            "Lance d'abord :"
        )

        print(
            "python scripts/01_detect_scenes.py"
        )

        return False

    video = cv2.VideoCapture(
        str(VIDEO)
    )

    if not video.isOpened():

        print(
            "❌ Impossible d'ouvrir la vidéo"
        )

        return False

    fps = video.get(
        cv2.CAP_PROP_FPS
    )

    print(
        f"\nFPS : {fps}"
    )

    with open(
        SCENES_CSV,
        "r",
        encoding="utf-8"
    ) as csv_file:

        reader = csv.DictReader(
            csv_file
        )

        scenes = list(reader)

    print(
        f"✓ {len(scenes)} scènes à traiter"
    )

    for scene in scenes:

        scene_number = int(
            scene["scene"]
        )

        start_time = timecode_to_seconds(
            scene["start"]
        )

        end_time = timecode_to_seconds(
            scene["end"]
        )

        duration = (
            end_time
            - start_time
        )

        scene_folder = (
            OUTPUT_FOLDER
            / f"scene_{scene_number:03d}"
        )

        scene_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        print(
            f"\n🎬 Scène {scene_number:03d}"
        )

        for image_number in range(
            IMAGES_PER_SCENE
        ):

            if IMAGES_PER_SCENE == 1:

                position = 0

            else:

                position = (
                    image_number
                    / (IMAGES_PER_SCENE - 1)
                )

            time_seconds = (
                start_time
                + position * duration
            )

            video.set(
                cv2.CAP_PROP_POS_MSEC,
                time_seconds * 1000
            )

            success, frame = video.read()

            if not success:

                print(
                    f"   ❌ Impossible "
                    f"d'extraire l'image "
                    f"{image_number + 1}"
                )

                continue

            filename = (
                f"frame_"
                f"{image_number + 1:02d}.jpg"
            )

            filepath = (
                scene_folder
                / filename
            )

            cv2.imwrite(
                str(filepath),
                frame
            )

            print(
                f"   ✓ {filename}"
            )

    video.release()

    print()
    print("=" * 60)
    print("✅ EXTRACTION TERMINÉE")
    print("=" * 60)

    return True


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    extract_frames()