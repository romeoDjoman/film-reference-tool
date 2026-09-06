# FILM REFERENCE TOOL

# 📘 PROTOCOLE COMPLET — `FILM REFERENCE TOOL`

**Version : 1.0 — septembre 2026**

## 1. Objectif du projet

`film_reference_tool` est un pipeline automatisé permettant de transformer un film en **référentiel de production 3D**.

Le système doit progressivement être capable de :

```text
FILM
 │
 ▼
Extraction des plans
 │
 ▼
Extraction des images de référence
 │
 ▼
Contact sheets
 │
 ▼
Analyse IA des scènes
 │
 ▼
Analyse globale du film
 │
 ▼
Identification des :
 ├── personnages
 ├── environnements
 ├── architectures
 ├── props
 ├── équipements
 ├── matériaux
 ├── caméras
 └── lumières
 │
 ▼
Plan de production
 │
 ▼
Classification des assets
 │
 ▼
Bibliothèque d'assets
 │
 ▼
Génération / recherche / téléchargement d'assets
 │
 ▼
Blender
 │
 ▼
Assemblage des scènes 3D
 │
 ▼
Production d'une scène cinématographique
```

---

# 2. Architecture générale

Le dossier racine doit rester :

```text
film_reference_tool/
```

Structure recommandée :

```text
film_reference_tool/
│
├── videos/
│   └── passion_christ_flagellation.mp4
│
├── scripts/
│
├── blender_scripts/
│
├── output/
│
├── assets/
│
├── data/
│
├── config/
│
├── tests/
│
├── docs/
│
├── .venv/
│
├── requirements.txt
│
└── README.md
```

---

# 3. Nomenclature des dossiers

## `videos/`

Contient les films sources.

```text
videos/
└── passion_christ_flagellation.mp4
```

Règle :

```text
videos/
    ├── film_01.mp4
    ├── film_02.mp4
    └── ...
```

Ne jamais mettre les fichiers générés ici.

---

# 4. `data/`

Contient les données d'entrée statiques.

Exemple :

```text
data/
├── references/
├── metadata/
└── rosallind/
```

Pour ton projet bioinformatique, ce dossier peut également rester séparé si les projets sont indépendants.

Pour le projet cinéma, `data/` doit contenir les données qui ne sont pas directement produites par le pipeline.

---

# 5. `output/`

C'est le **laboratoire de production automatique**.

Structure :

```text
output/
│
├── scenes.csv
│
├── scenes/
│   ├── scene_001/
│   │   ├── frame_01.jpg
│   │   ├── frame_02.jpg
│   │   ├── frame_03.jpg
│   │   ├── frame_04.jpg
│   │   ├── frame_05.jpg
│   │   ├── contact_sheet.jpg
│   │   └── analysis.json
│   │
│   ├── scene_002/
│   ├── scene_003/
│   └── ...
│
├── film_analysis.json
│
└── preproduction/
    ├── assets.json
    ├── assets_manager.json
    ├── assets_classified.json
    ├── asset_library.json
    └── ...
```

---

# 6. Détection des plans

Première étape réelle du pipeline :

```text
film
 ↓
détection des changements de plans
```

Technologie utilisée :

**PySceneDetect + ContentDetector**

Nous avons obtenu :

```text
37 plans détectés
```

avec :

```text
FPS ≈ 23.976
```

Le programme identifie les limites :

```text
Scene 001
00:00 → 00:05

Scene 002
00:05 → 00:09

Scene 003
00:09 → ...
```

---

# 7. Extraction des frames

Pour chaque plan, nous avons décidé d'extraire :

```text
5 images
```

Exemple :

```text
output/scenes/scene_001/

frame_01.jpg
frame_02.jpg
frame_03.jpg
frame_04.jpg
frame_05.jpg
```

Pourquoi ?

Parce qu'une seule image peut être trompeuse.

Avec cinq images, l'IA dispose d'un aperçu plus représentatif du plan.

---

# 8. Contact sheet

Pour chaque scène, nous générons également une planche :

```text
contact_sheet.jpg
```

Disposition :

```text
┌──────────┬──────────┬──────────┐
│ frame 01 │ frame 02 │ frame 03 │
├──────────┼──────────┼──────────┤
│ frame 04 │ frame 05 │          │
└──────────┴──────────┴──────────┘
```

Cette image permet :

* inspection humaine ;
* comparaison rapide ;
* visualisation de la scène ;
* référence pour l'analyse.

---

# 9. `scenes.csv`

Le pipeline crée également :

```text
output/scenes.csv
```

Structure :

```text
scene
start
end
duration
frame_01
frame_02
frame_03
frame_04
frame_05
```

Exemple conceptuel :

```csv
scene,start,end,duration,frame_01,frame_02,...
1,00:00,00:05,5.0,...
2,00:05,00:09,4.0,...
```

Ce fichier est le **registre temporel des scènes**.

---

# 10. Analyse IA des scènes

Nous avons ensuite intégré :

```text
Ollama
```

avec :

```text
qwen3.5:4b
```

Version Ollama utilisée :

```text
0.33.3
```

Le modèle analyse les images de chaque scène.

---

# 11. Pourquoi Ollama ?

L'avantage est que l'analyse peut être effectuée localement.

Architecture :

```text
Image
  ↓
Python
  ↓
Ollama
  ↓
Qwen
  ↓
JSON
```

Cela évite de dépendre obligatoirement d'une API cloud.

---

# 12. Problème rencontré : contexte IA

Au début, nous avons rencontré :

```text
request (5208 tokens)
exceeds the available context size (4096 tokens)
```

Correction :

```python
options={
    "num_ctx": 16384,
    "num_predict": 4096,
    "temperature": 0
}
```

et :

```python
think=False
```

Cette configuration permet d'obtenir une sortie structurée plus stable.

---

# 13. Format d'analyse

Chaque scène produit :

```text
output/scenes/scene_001/analysis.json
```

Puis :

```text
scene_002/analysis.json
scene_003/analysis.json
...
```

L'IA identifie notamment :

```text
characters
objects
locations
assets_3d
materials
camera
lighting
```

---

# 14. Fusion des analyses

Une fois les 37 scènes analysées, nous avons créé :

```text
output/film_analysis.json
```

Ce fichier représente **la vision globale du film**.

Résultat obtenu :

```text
37 scènes
120 instances de personnages
122 instances d'objets
30 lieux
147 assets 3D
150 matériaux
125 assets existants potentiels
```

Important :

**instance ≠ asset unique.**

Par exemple :

```text
Scène 01 → soldat
Scène 02 → soldat
Scène 03 → soldat
```

peut correspondre à :

```text
1 personnage réutilisable
```

C'est précisément pourquoi l'étape suivante est nécessaire.

---

# 15. Production Plan

Script :

```text
production_plan.py
```

Entrée :

```text
output/film_analysis.json
```

Sorties dans :

```text
output/preproduction/
```

Le système produit :

```text
72 personnages uniques
30 environnements uniques
86 props uniques
145 assets 3D uniques
144 matériaux uniques
37 configurations caméra
37 configurations lumière
477 tâches de production
```

---

# 16. Pourquoi le Production Plan ?

Il transforme :

```text
ANALYSE
```

en :

```text
PLAN DE FABRICATION
```

Exemple :

```text
Asset :
Roman Stone Wall

Catégorie :
Architecture

Production :
Procedural

Priorité :
High
```

Cela commence à ressembler à un véritable pipeline de production.

---

# 17. Asset Manager

Script :

```text
asset_manager.py
```

Entrée :

```text
output/preproduction/assets.json
```

Sortie :

```text
output/preproduction/assets_manager.json
```

Il détermine comment obtenir chaque asset.

Résultat :

```text
EXISTING_ASSET       54
PROCEDURAL           23
PROCEDURAL_OR_EXISTING 33
SEARCH_FIRST         35
```

---

# 18. Classification avancée

Script :

```text
classify_assets.py
```

Entrée :

```text
assets_manager.json
```

Sortie :

```text
assets_classified.json
```

Catégories :

```text
ARCHITECTURE
CHARACTER
CHARACTER_EQUIPMENT
ENVIRONMENT
MATERIAL
OTHER
PROP
```

Résultat :

```text
ARCHITECTURE          21
CHARACTER             26
CHARACTER_EQUIPMENT   31
ENVIRONMENT           11
MATERIAL              31
OTHER                 14
PROP                  11
```

---

# 19. Méthodes de production

Le système distingue :

```text
EXISTING_ASSET
EXISTING_OR_GENERATED
EXISTING_OR_PROCEDURAL
PROCEDURAL
PROCEDURAL_OR_EXISTING
SEARCH
```

Cela permet de prendre une décision rationnelle.

Exemple :

### Mur

```text
Architecture
↓
Procedural
↓
Blender Python
```

### Personnage historique complexe

```text
Character
↓
Existing / Generated
↓
Recherche d'un modèle existant
```

### Sol en pierre

```text
Material
↓
Procedural
↓
Shader / texture
```

---

# 20. Asset Library

Script :

```text
asset_library.py
```

Entrée :

```text
assets_classified.json
```

Sortie :

```text
asset_library.json
```

Cette étape crée le **catalogue central des assets**.

Pour l'instant :

```text
145 assets
145 MISSING
```

C'est normal.

Nous avons créé **le registre**, pas encore les fichiers 3D correspondants.

---

# 21. Arborescence des assets

Nous avons ensuite créé :

```text
assets/
│
├── downloaded/
│
├── generated/
│
├── blend/
│
├── textures/
│
├── materials/
│
├── characters/
│
├── environments/
│
├── props/
│
└── architecture/
```

### Rôle précis

`downloaded/`

Assets récupérés depuis une source externe.

```text
assets/downloaded/
```

---

`generated/`

Assets générés automatiquement.

C'est ici que nous avons placé :

```text
roman_stone_wall.blend
```

---

`blend/`

Fichiers `.blend` de production ou assemblage.

---

`textures/`

Textures :

```text
.jpg
.png
.exr
...
```

---

`materials/`

Matériaux réutilisables.

---

`characters/`

Personnages.

---

`environments/`

Environnements.

---

`props/`

Objets.

---

`architecture/`

Éléments architecturaux :

```text
walls
columns
doors
arches
stairs
...
```

---

# 22. Premier générateur Blender

Nous avons créé :

```text
blender_scripts/
└── generate_stone_wall.py
```

Technologie :

```text
Python
+
Blender Python API
+
bpy
```

Important :

`bpy` fonctionne **dans Blender**.

Donc :

❌

```bash
python generate_stone_wall.py
```

mais :

✅

```bash
/Applications/Blender.app/Contents/MacOS/Blender \
--background \
--python blender_scripts/generate_stone_wall.py
```

---

# 23. Premier asset généré

Le script construit :

```text
Mur
├── blocs de pierre
├── variations de taille
├── variations de rotation
├── matériau
├── sol
├── caméra
└── lumière
```

Puis sauvegarde :

```text
assets/generated/roman_stone_wall.blend
```

Résultat confirmé :

```text
117 KB
```

Donc notre première chaîne complète fonctionne réellement :

```text
Python
 ↓
Blender
 ↓
bpy
 ↓
Géométrie
 ↓
.blend
```

---

# 24. Règle fondamentale du projet

À partir de maintenant, il faut respecter cette séparation :

```text
Python classique
    ↓
analyse / données / IA / orchestration

Blender Python
    ↓
géométrie / matériaux / scènes / caméra / lumière
```

Ne mélangeons pas les deux environnements inutilement.

---

# 25. Nomenclature des scripts

Je recommande désormais cette organisation :

```text
scripts/
│
├── 01_detect_scenes.py
├── 02_extract_frames.py
├── 03_create_contact_sheets.py
├── 04_analyse_scene_ia.py
├── 05_merge_analysis.py
├── 06_production_plan.py
├── 07_asset_manager.py
├── 08_classify_assets.py
└── 09_asset_library.py
```

Et :

```text
blender_scripts/
│
├── 01_generate_assets.py
├── 02_import_assets.py
├── 03_build_environment.py
├── 04_build_scene.py
├── 05_setup_camera.py
├── 06_setup_lighting.py
└── 07_render_scene.py
```

**Mais ne renomme pas maintenant tes scripts existants sans nécessité.** Ils fonctionnent déjà. Cette nomenclature est surtout la cible d'organisation future.

---

# 26. Convention de nommage des fichiers 3D

Utiliser :

```text
snake_case
```

Exemples :

```text
roman_stone_wall.blend
roman_column.blend
wooden_door.blend
roman_soldier.blend
stone_floor.blend
```

Pas :

```text
MurFinal2.blend
Mur_final_OK.blend
nouveau_mur.blend
test123.blend
```

---

# 27. Convention pour les scènes

Toujours :

```text
scene_001
scene_002
scene_003
```

Jamais :

```text
scene1
scene2
scene_final
scene_final2
```

---

# 28. Documentation

Je recommande fortement de créer :

```text
docs/
│
├── PROTOCOL.md
├── ARCHITECTURE.md
├── PIPELINE.md
├── BLENDER.md
├── ASSETS.md
└── TROUBLESHOOTING.md
```

Et à la racine :

```text
README.md
```

---

# 29. Contenu de `README.md`

Le README doit être le **point d'entrée**.

Il doit expliquer :

```text
1. Qu'est-ce que le projet ?
2. Installation
3. Environnement
4. Structure
5. Pipeline
6. Comment lancer le pipeline
7. Comment utiliser Blender
8. Où sont les résultats
9. Problèmes connus
```

---

# 30. Environnement Python

Créer/retrouver :

```text
.venv/
```

Puis :

```bash
source .venv/bin/activate
```

Vérifier :

```bash
python --version
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Puis générer éventuellement :

```bash
pip freeze > requirements.txt
```

---

# 31. Ollama

Ollama est indépendant du `.venv`.

Vérification :

```bash
ollama --version
```

Puis :

```bash
ollama list
```

Nous avons actuellement utilisé :

```text
qwen3.5:4b
```

---

# 32. Blender

Blender est également indépendant du `.venv`.

Chez toi :

```text
/Applications/Blender.app/
```

Version :

```text
Blender 5.2.1 LTS
```

Test :

```bash
/Applications/Blender.app/Contents/MacOS/Blender --version
```

---

# 33. Commande de génération Blender

Toujours depuis :

```text
film_reference_tool/
```

utiliser :

```bash
/Applications/Blender.app/Contents/MacOS/Blender \
--background \
--python blender_scripts/generate_stone_wall.py
```

---

# 34. Workflow complet à retenir

Quand tu reviendras dans 6 mois, pense simplement à cette séquence :

```text
① FILM
   ↓
② DÉTECTION DES PLANS
   ↓
③ FRAMES
   ↓
④ CONTACT SHEETS
   ↓
⑤ ANALYSE IA
   ↓
⑥ FUSION
   ↓
⑦ PRODUCTION PLAN
   ↓
⑧ ASSET MANAGER
   ↓
⑨ CLASSIFICATION
   ↓
⑩ ASSET LIBRARY
   ↓
⑪ GÉNÉRATION / RECHERCHE DES ASSETS
   ↓
⑫ BLENDER
   ↓
⑬ ASSEMBLAGE DES SCÈNES
   ↓
⑭ CAMÉRA + LUMIÈRE
   ↓
⑮ RENDU
```

---

# 35. État actuel du projet

Nous sommes actuellement ici :

```text
                TERMINÉ
                   ↓
Film ──────────────┐
                   ↓
Détection plans    ✓
                   ↓
Frames             ✓
                   ↓
Contact sheets     ✓
                   ↓
Analyse IA         ✓
                   ↓
Fusion             ✓
                   ↓
Production Plan    ✓
                   ↓
Asset Manager      ✓
                   ↓
Classification     ✓
                   ↓
Asset Library      ✓
                   ↓
Dossiers assets    ✓
                   ↓
Premier asset 3D   ✓
                   ↓
              >>> NOUS SOMMES ICI <<<
                   ↓
Générateur 3D
générique
                   ↓
Import automatique
                   ↓
Construction
des scènes
                   ↓
Caméra / lumière
                   ↓
Rendu
```

---

# 36. La philosophie du projet

Le principe fondamental à conserver est :

> **L'IA ne doit pas directement fabriquer toute la scène. Elle doit d'abord comprendre le film et produire des données structurées. Python orchestre. Blender fabrique et assemble.**

Donc :

```text
IA
=
COMPRENDRE

Python
=
ORCHESTRER

Asset Library
=
STOCKER / RÉUTILISER

Blender
=
FABRIQUER / ASSEMBLER / RENDRE
```

C'est beaucoup plus robuste qu'un système où l'on demande simplement :

> « IA, crée-moi cette scène. »

---

# 37. Structure finale recommandée

À terme, ton projet devrait ressembler à ceci :

```text
film_reference_tool/
│
├── README.md
├── requirements.txt
│
├── videos/
│   └── source_video.mp4
│
├── data/
│
├── scripts/
│   ├── 01_detect_scenes.py
│   ├── 02_extract_frames.py
│   ├── 03_create_contact_sheets.py
│   ├── 04_analyse_scene_ia.py
│   ├── 05_merge_analysis.py
│   ├── 06_production_plan.py
│   ├── 07_asset_manager.py
│   ├── 08_classify_assets.py
│   └── 09_asset_library.py
│
├── blender_scripts/
│   ├── generate_stone_wall.py
│   ├── generate_architecture.py
│   ├── generate_props.py
│   ├── generate_environment.py
│   ├── import_assets.py
│   ├── build_scene.py
│   └── render_scene.py
│
├── assets/
│   ├── downloaded/
│   ├── generated/
│   ├── blend/
│   ├── textures/
│   ├── materials/
│   ├── characters/
│   ├── environments/
│   ├── props/
│   └── architecture/
│
├── output/
│   ├── scenes.csv
│   ├── film_analysis.json
│   │
│   ├── scenes/
│   │   ├── scene_001/
│   │   ├── scene_002/
│   │   └── ...
│   │
│   └── preproduction/
│       ├── assets.json
│       ├── assets_manager.json
│       ├── assets_classified.json
│       └── asset_library.json
│
├── docs/
│   ├── PROTOCOL.md
│   ├── ARCHITECTURE.md
│   ├── PIPELINE.md
│   ├── BLENDER.md
│   ├── ASSETS.md
│   └── TROUBLESHOOTING.md
│
├── tests/
│
└── .venv/
```

## ⭐ Et surtout : faisons-en un vrai document maintenant

Je te recommande de **ne pas simplement garder cette réponse dans le chat**.

Le mieux est de créer dans ton projet :

```text
docs/PROTOCOL.md
```

et d'y mettre cette documentation.

Puis, à chaque grosse étape du projet, on ajoute une section :

```text
PROTOCOL.md
       │
       ├── Phase 1 — Analyse vidéo
       ├── Phase 2 — Analyse IA
       ├── Phase 3 — Préproduction
       ├── Phase 4 — Asset Library
       ├── Phase 5 — Génération 3D
       ├── Phase 6 — Assemblage Blender
       ├── Phase 7 — Caméra / lumière
       ├── Phase 8 — Rendu
       └── Phase 9 — Automatisation complète
```

Ainsi, **dans six mois, tu n'auras pas besoin de retrouver cette conversation** : tu ouvriras `docs/PROTOCOL.md`, tu verras immédiatement où nous en étions et tu pourras reprendre le pipeline.

Et notre prochaine phase logique est maintenant **Phase 5 — Génération 3D automatisée**, où l'on va faire évoluer `generate_stone_wall.py` en un véritable **Asset Generator** capable de lire `assets_classified.json` et de décider automatiquement quel asset générer.
