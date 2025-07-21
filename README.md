# Générateur de Mosaïques d'Images

Créez des mosaïques et animations visuelles à partir de vos collections de photos.

## 🚀 Fonctionnalités Principales

- 🖼️ Génération de mosaïques d'images (à partir d'une photo source et d'une collection de miniatures)
- 🎥 Création d'animations et effets vidéo (apparition, zoom, fondu…)
- ✨ Effets d'apparition pixelisée
- 🔍 Zoom précis sur points spécifiques
- 🖌️ Fusion et transitions d'images
- 🖥️ Interface graphique intuitive (Tkinter)

## Organisation des Fichiers

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

## ⚡ Utilisation Rapide

1. **Interface Graphique** : python interface.py

2. **Mosaïque simple** : python mosaic.py image_source.jpg miniature.jpg 20 sortie.jpg

3. **Animation zoom** : python make_movie.py image_source.jpg sortie.mp4 2 9


# ✅ Bonnes Pratiques
- Préparer un dossier de miniatures homogènes (carrées de préférence)
- Pour des vidéos fluides : 60 FPS recommandés
- Taille idéale des tuiles : 10 à 30 pixels
- Privilégier une bonne variation de couleurs dans les miniatures pour de meilleurs résultats

