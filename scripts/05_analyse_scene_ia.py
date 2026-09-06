import json
from pathlib import Path

import ollama


# ============================================================
# CONFIGURATION
# ============================================================

MODEL = "qwen3.5:4b"

SCENES_FOLDER = Path("output/scenes")


# ============================================================
# ANALYSE D'UNE SCÈNE
# ============================================================

def analyse_scene(scene_folder):

    # --------------------------------------------------------
    # RÉCUPÉRER LES IMAGES
    # --------------------------------------------------------

    image_files = sorted(
        scene_folder.glob("frame_*.jpg")
    )

    if not image_files:
        print(
            f"⚠️ Aucune image dans {scene_folder}"
        )
        return False

    # --------------------------------------------------------
    # NUMÉRO DE LA SCÈNE
    # --------------------------------------------------------

    try:
        scene_number = int(
            scene_folder.name.split("_")[1]
        )

    except (IndexError, ValueError):

        print(
            f"❌ Nom de scène invalide : {scene_folder.name}"
        )

        return False

    # --------------------------------------------------------
    # FICHIER DE SORTIE
    # --------------------------------------------------------

    output_file = scene_folder / "analysis.json"

    # Si l'analyse existe déjà, on ne recommence pas
    if output_file.exists():

        print(
            f"   ⏭️ Analyse déjà existante : "
            f"{output_file}"
        )

        return True

    # --------------------------------------------------------
    # INFORMATIONS
    # --------------------------------------------------------

    print(
        f"\n🎬 Analyse de la scène {scene_number:03d}"
    )

    print(
        f"   {len(image_files)} images trouvées"
    )

    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are an expert cinematographer,
film analyst and 3D environment artist.

You are analyzing scene {scene_number}.

The provided images are five frames extracted
from the SAME cinematic shot.

Analyze all frames together.

Your goal is to extract information useful
for reconstructing the scene in Blender.

IMPORTANT RULES:

- Describe only what can reasonably be observed.
- Do not identify real people.
- Describe characters by their role, appearance,
  clothing and position.
- Do not invent details.
- If something cannot be determined, write "uncertain".
- Camera focal length is an estimate only.
- Distinguish visible facts from reasonable inference.
- Treat the five images as one cinematic shot.
- Be concise but sufficiently detailed for 3D reconstruction.

Analyze the following categories.

1. CHARACTERS

Identify:

- number of characters
- role
- appearance
- clothing
- position
- posture
- actions
- interactions

2. ENVIRONMENT

Identify:

- location
- interior or exterior
- architecture
- walls
- floor
- ceiling
- background
- depth

3. OBJECTS

Identify important objects.

For each object provide:

- name
- position
- apparent material
- importance for reconstruction

4. CAMERA

Estimate:

- shot type
- camera angle
- camera height
- composition
- perspective
- camera movement
- estimated focal length

5. LIGHTING

Analyze:

- light sources
- direction
- intensity
- softness
- color temperature
- shadows
- mood

6. VISUAL STYLE

Analyze:

- realism
- color palette
- contrast
- atmosphere
- cinematic characteristics

7. 3D RECONSTRUCTION

Determine:

- important assets
- materials
- geometry
- existing assets that could potentially be reused
  instead of modeling everything from scratch

Return ONLY valid JSON.

Use exactly this structure:

{{
    "scene": {scene_number},

    "characters": [],

    "environment": {{
        "location": "",
        "interior_exterior": "",
        "architecture": "",
        "walls": "",
        "floor": "",
        "ceiling": "",
        "background": "",
        "depth": ""
    }},

    "objects": [],

    "camera": {{
        "shot_type": "",
        "angle": "",
        "height": "",
        "composition": "",
        "perspective": "",
        "movement": "",
        "estimated_focal_length": ""
    }},

    "lighting": {{
        "sources": [],
        "direction": "",
        "intensity": "",
        "softness": "",
        "color_temperature": "",
        "shadows": "",
        "mood": ""
    }},

    "visual_style": "",

    "3d_reconstruction": {{
        "important_assets": [],
        "materials": [],
        "geometry": [],
        "existing_assets": []
    }}
}}
"""

    # --------------------------------------------------------
    # APPEL À OLLAMA
    # --------------------------------------------------------

    try:

        response = ollama.chat(

            model=MODEL,

            messages=[
                {
                    "role": "user",

                    "content": prompt,

                    "images": [
                        str(image_file)
                        for image_file in image_files
                    ]
                }
            ],

            # Demande explicitement du JSON
            format="json",

            # Désactive le raisonnement visible
            think=False,

            options={
                # Contexte suffisamment grand
                "num_ctx": 16384,

                # Marge pour terminer le JSON
                "num_predict": 6144,

                # Résultats reproductibles
                "temperature": 0
            }
        )

    except Exception as error:

        print(
            f"   ❌ Erreur Ollama : {error}"
        )

        return False

    # --------------------------------------------------------
    # RÉCUPÉRER LA RÉPONSE
    # --------------------------------------------------------

    try:

        result_text = response["message"]["content"]

    except (KeyError, TypeError):

        print(
            "   ❌ Impossible de récupérer "
            "la réponse du modèle"
        )

        print(response)

        return False

    # --------------------------------------------------------
    # VÉRIFIER SI LA RÉPONSE EST VIDE
    # --------------------------------------------------------

    if not result_text.strip():

        print(
            "   ❌ Réponse vide du modèle"
        )

        return False

    # --------------------------------------------------------
    # CONVERSION JSON
    # --------------------------------------------------------

    try:

        analysis = json.loads(
            result_text
        )

    except json.JSONDecodeError:

        print(
            "   ❌ Réponse du modèle "
            "non valide en JSON"
        )

        print("\n--- RÉPONSE DU MODÈLE ---")
        print(result_text)
        print("--- FIN RÉPONSE ---\n")

        return False

    # --------------------------------------------------------
    # VÉRIFICATION MINIMALE DE LA STRUCTURE
    # --------------------------------------------------------

    if not isinstance(analysis, dict):

        print(
            "   ❌ Le résultat JSON n'est pas un objet"
        )

        return False

    # --------------------------------------------------------
    # FORCER LE BON NUMÉRO DE SCÈNE
    # --------------------------------------------------------

    analysis["scene"] = scene_number

    # --------------------------------------------------------
    # SAUVEGARDER
    # --------------------------------------------------------

    try:

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                analysis,
                file,
                indent=4,
                ensure_ascii=False
            )

    except Exception as error:

        print(
            f"   ❌ Erreur lors de la sauvegarde : {error}"
        )

        return False

    # --------------------------------------------------------
    # SUCCÈS
    # --------------------------------------------------------

    print(
        f"   ✓ Analyse enregistrée : "
        f"{output_file}"
    )

    return True


# ============================================================
# ANALYSER TOUTES LES SCÈNES
# ============================================================

def analyse_all_scenes():

    # --------------------------------------------------------
    # IMPORTANT :
    # récupérer uniquement les DOSSIERS scene_XXX
    # et ignorer les fichiers scene_XXX_frame_XX.jpg
    # --------------------------------------------------------

    scene_folders = sorted(

        folder

        for folder in SCENES_FOLDER.glob("scene_*")

        if folder.is_dir()
    )

    # --------------------------------------------------------
    # AUCUNE SCÈNE
    # --------------------------------------------------------

    if not scene_folders:

        print(
            "❌ Aucune scène trouvée."
        )

        return

    # --------------------------------------------------------
    # NOMBRE DE SCÈNES
    # --------------------------------------------------------

    print(
        f"\n🎬 {len(scene_folders)} scènes trouvées"
    )

    print(
        f"📁 Dossier : {SCENES_FOLDER}"
    )

    print(
        f"🤖 Modèle : {MODEL}"
    )

    # --------------------------------------------------------
    # COMPTEURS
    # --------------------------------------------------------

    success_count = 0
    error_count = 0

    # --------------------------------------------------------
    # ANALYSE DES SCÈNES
    # --------------------------------------------------------

    for index, scene_folder in enumerate(
        scene_folders,
        start=1
    ):

        print(
            f"\n[{index}/{len(scene_folders)}]"
        )

        success = analyse_scene(
            scene_folder
        )

        if success:

            success_count += 1

        else:

            error_count += 1

    # --------------------------------------------------------
    # RÉSUMÉ FINAL
    # --------------------------------------------------------

    print(
        "\n" + "=" * 50
    )

    print(
        "ANALYSE TERMINÉE"
    )

    print(
        f"✓ Réussites : {success_count}"
    )

    print(
        f"❌ Erreurs : {error_count}"
    )

    print(
        "=" * 50
    )


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

if __name__ == "__main__":

    analyse_all_scenes()