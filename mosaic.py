import numpy as np
import cv2
from tqdm import tqdm

# _________________Fonctions___________________

def adjust_color(img_src: np.ndarray, target_color: list)-> np.ndarray:
    """
    Ajuste la couleur moyenne de l'image source pour correspondre à la couleur cible.

    Args:
        img_src (np.ndarray): L'image source.
        target_color (list): La couleur cible au format [B, G, R].

    Returns:
        np.ndarray: L'image avec la couleur ajustée.
    """
    b, g, r = cv2.split(img_src) 
    b_moy = np.mean(b)
    g_moy = np.mean(g)
    r_moy = np.mean(r)

    b_diff = target_color[0]-b_moy
    g_diff = target_color[1]-g_moy
    r_diff = target_color[2]-r_moy

    b_targ = np.clip(b+b_diff,0,255).astype(np.uint8)
    g_targ = np.clip(g+g_diff,0,255).astype(np.uint8)
    r_targ = np.clip(r+r_diff,0,255).astype(np.uint8)

    img_targ = cv2.merge([b_targ,g_targ,r_targ])
    return img_targ

def build_mosaic(img_src : np.ndarray, img_mini : np.ndarray, n : int)-> np.ndarray:
    """
    Construit une mosaïque en remplaçant les pixels noirs de l'image source par une image miniature avec la couleur ajustée.

    Args:
        img_src (np.ndarray): L'image source.
        img_mini (np.ndarray): L'image miniature.
        n (int): Le nombre de répétitions de l'image miniature.

    Returns:
        np.ndarray: L'image mosaïque résultante.
    """
    shape=img_src.shape[:2]
    b, g, r = cv2.split(img_src)
    img_dest=np.zeros((shape[0]*n,shape[1]*n,3),dtype=np.uint8)
    img_mini_resize=cv2.resize(img_mini,(n,n))

    for y in tqdm(range(0,shape[0])):
        for x in range(0,shape[1]):
            color=(b[y,x],g[y,x],r[y,x])
            img_mini_colo=adjust_color(img_mini_resize,color)
            img_dest[n*y:n*(y+1),n*x :n*(x+1)] = img_mini_colo[:,:]
    return img_dest
    
def mosaic_image(path_src : str, path_mini : str, n : int, path_output : str):
    """
    Crée une mosaïque à partir des images sources et miniatures, puis enregistre le résultat.

    Args:
        path_src (str): Chemin de l'image source.
        path_mini (str): Chemin de l'image miniature.
        n (int): Le nombre de répétitions de l'image miniature.
        path_output (str): Chemin de sortie pour l'image mosaïque.
    """
    img_dest=build_mosaic(cv2.imread(path_src),cv2.imread(path_mini),n)
    cv2.imwrite(path_output,img_dest)

def crop_and_resize(img_src : np.ndarray, crop_rect : tuple, w : int, h : int)-> np.ndarray:
    """
    Recadre et redimensionne une image source selon les dimensions spécifiées.

    Args:
        img_src (np.ndarray): L'image source.
        crop_rect (tuple): Coordonnées (y1, x1, y2, x2) du rectangle de recadrage.
        w (int): Largeur de l'image de sortie.
        h (int): Hauteur de l'image de sortie.

    Returns:
        np.ndarray: L'image recadrée et redimensionnée.
    """
    y1, x1, y2, x2 = crop_rect 
    cropped_img = img_src[y1:y2, x1:x2]
    resized_img = cv2.resize(cropped_img, (w, h))
    return resized_img

def mosaic_zoom(path_src: str, path_mini: str, path_prefix_output: str, nw: int, nh: int):
    """
    Crée une série d'images mosaïques zoomées à partir d'une image source et d'une image miniature.

    Args:
        path_src (str): Chemin de l'image source.
        path_mini (str): Chemin de l'image miniature.
        path_prefix_output (str): Préfixe pour les noms de fichier de sortie.
        nw (int): Nombre de niveaux de zoom en largeur.
        nh (int): Nombre de niveaux de zoom en hauteur.
    """
    img_src = cv2.imread(path_src)
    img_mini = cv2.imread(path_mini)
    img_resized = cv2.resize(img_src, (2 ** nw, 2 ** nh))
    cv2.imwrite(f"{path_prefix_output}_1.jpg", img_resized)
    h, w = img_resized.shape[:2]
    for i in range(2, 8): 
        h01=(h//2)-(h//(2**i)) 
        h02=(h//2)+(h//(2**i))
        w01=(w//2)-(w//(2**i))
        w02=(w//2)+(w//(2**i))
        img_resized_cropped = crop_and_resize(img_resized, (h01, w01, h02, w02), w//(2**i), h//(2**i))
        mini_resized = cv2.resize(img_mini, (2**i, 2**i))
        mosaic_img = build_mosaic(img_resized_cropped, mini_resized, 2**i) 
        cv2.imwrite(f"{path_prefix_output}_{i}.jpg", mosaic_img)



# ________________Tests____________________________
""""
adjusted_img = adjust_color(cv2.imread("baby.jpg"), [200,164,223])

cv2.imshow("Adjusted Color",adjusted_img)
cv2.waitKey(0) #pour ne pas que la fenetre se referme, on attends que la croix rouge soit pressée
cv2.destroyAllWindows()

mosaic=cv2.imwrite("build_mosaic.jpg",build_mosaic(cv2.imread("baby.jpg"),cv2.imread("baby.jpg"),20))
cv2.imshow("Build Mosaic",mosaic)
cv2.waitKey(0) 
cv2.destroyAllWindows()

mosaic_image("flip.jpg", "beauceron.jpg", 30, "flip2.jpg")

crop=crop_and_resize(cv2.imread("flip.jpg"), (330,160), 100, 300)
cv2.imshow("Crop",crop)
cv2.waitKey(0) 
cv2.destroyAllWindows()

mosaic_zoom("beauceron.jpg", "beau5.jpg", "beauceron", 9, 9)
"""
