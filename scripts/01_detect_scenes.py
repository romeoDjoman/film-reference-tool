import csv
from pathlib import Path

from scenedetect import detect, ContentDetector


# ============================================================
# CONFIGURATION
# ============================================================

VIDEO = Path(
    "videos/passion_christ_flagellation.mp4"
)

OUTPUT_CSV = Path(
    "output/scenes.csv"
)


# ============================================================
# UTILITAIRE
# ============================================================

def seconds_to_timecode(seconds):

    hours = int(seconds // 3600)

    minutes = int(
        (seconds % 3600) // 60
    )

    secs = seconds % 60

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{secs:06.3f}"
    )


# ============================================================
# DETECTION
# ============================================================

def detect_scenes():

    print()
    print("=" * 60)
    print("🎬 DÉTECTION DES PLANS")
    print("=" * 60)

    if not VIDEO.exists():

        print(
            f"❌ Vidéo introuvable : {VIDEO}"
        )

        return False

    print(
        f"\n🎥 Vidéo : {VIDEO}"
    )

    scenes = detect(
        str(VIDEO),
        ContentDetector()
    )

    print(
        f"\n✓ {len(scenes)} plans détectés"
    )

    # Créer le dossier output
    OUTPUT_CSV.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Créer le CSV
    with open(
        OUTPUT_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow([
            "scene",
            "start",
            "end",
            "duration"
        ])

        for scene_number, (start, end) in enumerate(
            scenes,
            start=1
        ):

            start_seconds = start.seconds
            end_seconds = end.seconds

            duration = (
                end_seconds
                - start_seconds
            )

            writer.writerow([
                scene_number,
                seconds_to_timecode(
                    start_seconds
                ),
                seconds_to_timecode(
                    end_seconds
                ),
                round(duration, 3)
            ])

    print(
        f"\n✓ Fichier créé : {OUTPUT_CSV}"
    )

    return True


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

if __name__ == "__main__":

    detect_scenes()