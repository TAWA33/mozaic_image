from tqdm import tqdm
import numpy as np
import cv2
import random

def ordre_apparition(w: int, h: int) -> list: 
    """
    Renvoie un ordre d'apparition des pixels d'une image de dimensions w x h
    
    Args:
        w (int): Largeur de l'image.
        h (int): Hauteur de l'image.
        
    Returns:
        list: Liste des coordonnées des pixels dans l'ordre d'apparition.
    """
    list_pix = [(x, y) for x in range(w) for y in range(h)] 
    random.shuffle(list_pix)
    return list_pix

def ajout(img_src: str, output_filename: str, steps: int, fps: int):
    """
    Créée la vidéo d'apparition d'une image pixel par pixel

    Args:
        img_src (str): Chemin de l'image source.
        output_filename (str): Nom du fichier vidéo de sortie.
        steps (int): Nombre de nouveaux pixels qui apparaissent par frame.
        fps (int): Nombre d'images par seconde de la vidéo.
    """
    img_src = cv2.imread(img_src)
    h, w = img_src.shape[:2]
    img_black = np.zeros((h, w, 3), dtype=np.uint8) 
    images = []
    ordre = ordre_apparition(w, h)
    images.append(img_black.copy())
    for i in tqdm(range(0, len(ordre), steps)):
        for j in range(steps): 
            if i + j < len(ordre): 
                x, y = ordre[i + j]
                img_black[y, x] = img_src[y, x]
        images.append(img_black.copy())
    
    video_writer = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h)) 
    for im in images:
        video_writer.write(im)
    video_writer.release()
    cv2.destroyAllWindows()


#ajout("beau5.jpg", "beau_apparition.mp4", 80, 100)

