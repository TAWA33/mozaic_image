# Générateur de Mosaïques d'Images

Créez des mosaïques et animations visuelles à partir de vos collections de photos.

## Fonctionnalités Principales

- 🖼️ Génération de mosaïques d'images
- 🎥 Création d'animations et effets vidéo
- ✨ Effets d'apparition pixelisée
- 🔍 Zoom précis sur points spécifiques
- 🖌️ Fusion et transitions d'images
- 🖥️ Interface graphique intuitive

## Fichiers Clés

📂 projet/

├── 📄 apparition.py             # Animation d'apparition pixel par pixel

├── 📄 concat_opac.py            # Fondu entre images et effets de transition

├── 📄 interface.py              # Interface utilisateur graphique (Tkinter)

├── 📄 mosaic.py                 # Cœur de génération des mosaïques

├── 📄 mosaic_rep.py             # Mosaïques à partir de répertoires d'images

├── 📄 zoom_precis.py            # Effets de zoom avancés et ciblés

└── 📄 make_video.py             # Fonctions vidéo de base

## Prérequis

- Python 3.8+
- Bibliothèques requises :
pip install opencv-python numpy tqdm Pillow

## Utilisation Rapide

1. **Interface Graphique** : python interface.py

2. **Ligne de commande** :
# Mosaïque simple
python mosaic.py image_source.jpg miniature.jpg 20 sortie.jpg

# Animation zoom
python make_movie.py image_source.jpg sortie.mp4 2 9


Bonnes Pratiques
Préparer un dossier d'images miniatures homogènes

Pour les vidéos : 60 FPS donne des résultats fluides

Taille recommandée des tuiles : 10-30 pixels

