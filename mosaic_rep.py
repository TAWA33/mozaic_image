from tqdm import tqdm
import numpy as np
import cv2
import os
import csv
import mosaic
import json


""""
def list_fichiers(path_dir : str)-> dict:
    for e in (os.listdir(path_dir)):
        print (e)
list_fichiers("../Imgaes rendu Prof")
"""

def mean_color_dir_csv(path_dir: str, color_file: str):
    """
    Calcule les couleurs moyennes de chaque image dans un répertoire et les enregistre dans un fichier CSV.

    Args:
    - path_dir (str): Le chemin du répertoire contenant les images.
    - color_file (str): Le nom du fichier CSV dans lequel enregistrer les couleurs moyennes.
    """
    colors = {}
    list_img = os.listdir(path_dir)
    for e in list_img:
        img = cv2.imread(os.path.join(path_dir, e))
        b, g, r = cv2.split(img)
        b_moy = round(np.mean(b))
        g_moy = round(np.mean(g))
        r_moy = round(np.mean(r))
        colors[e] = (b_moy, g_moy, r_moy)
    with open(color_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Image', 'Blue Mean', 'Green Mean', 'Red Mean'])
        
        for img_name, (blue_mean, green_mean, red_mean) in colors.items():
            writer.writerow([img_name, blue_mean, green_mean, red_mean])
        
def mean_color_dir_json(path_dir: str, color_file: str):
    """
    Calcule les couleurs moyennes de chaque image dans un répertoire et les enregistre dans un fichier JSON.

    Args:
    - path_dir (str): Le chemin du répertoire contenant les images.
    - color_file (str): Le nom du fichier JSON dans lequel enregistrer les couleurs moyennes.
    """
    colors = {}
    list_img = os.listdir(path_dir)
    for e in list_img:
        img = cv2.imread(os.path.join(path_dir, e))
        b, g, r = cv2.split(img)
        b_moy = round(np.mean(b))
        g_moy = round(np.mean(g))
        r_moy = round(np.mean(r))
        colors[e] = (b_moy, g_moy, r_moy)
    with open(color_file, 'w') as f:
        json.dump(colors,f)

def distance(color1: tuple, color2: tuple) -> float:
    """
    Calcule la distance euclidienne entre deux couleurs.

    Args:
    - color1 (tuple): Les composantes de la première couleur.
    - color2 (tuple): Les composantes de la deuxième couleur.

    Returns:
    - float: La distance euclidienne entre les deux couleurs.
    """
    return np.sqrt(np.sum((np.array(color1) - np.array(color2)) ** 2))

def find_img_color_csv(target_color: tuple, color_file: str) -> str:
    """
    Trouve l'image avec la couleur moyenne la plus proche de la couleur cible.

    Args:
    - target_color (tuple): La couleur cible à rechercher.
    - color_file (str): Le nom du fichier CSV contenant les couleurs moyennes des images.

    Returns:
    - str: Le nom de l'image avec la couleur moyenne la plus proche de la couleur cible.
    """
    closest_img = ''
    min_distance = float('inf')
    with open(color_file, 'r', newline='') as f: 
        reader = csv.DictReader(f)
        for row in reader: 
            img_color = (int(row['Blue Mean']), int(row['Green Mean']), int(row['Red Mean']))
            dis = distance(img_color, target_color)
            if dis < min_distance:
                min_distance = dis
                closest_img = row['Image']
    return closest_img


def find_img_color_json(target_color: tuple, color_file: str) -> str:
    """
    Trouve l'image avec la couleur moyenne la plus proche de la couleur cible.

    Args:
    - target_color (tuple): La couleur cible à rechercher.
    - color_file (str): Le nom du fichier JSON contenant les couleurs moyennes des images.

    Returns:
    - str: Le nom de l'image avec la couleur moyenne la plus proche de la couleur cible.
    """
    closest_img = ''
    min_distance = float('inf')
    with open(color_file, 'r') as f: 
        reader = json.load(f)
        for chemin in reader: 
            img_color = (int(reader[chemin][0]),int(reader[chemin][1]) ,int(reader[chemin][2]))
            dis = distance(img_color, target_color)
            if dis < min_distance:
                min_distance = dis
                closest_img = chemin
    return closest_img 

def build_mosaic(img_src: np.ndarray, path_dir: str, n: int, color_file: str) -> np.ndarray:
    """
    Construit une mosaïque à partir d'une image source et d'un ensemble d'images miniatures.

    Args:
    - img_src (np.ndarray): L'image source à utiliser comme base de la mosaïque.
    - path_dir (str): Le chemin du répertoire contenant les images miniatures.
    - n (int): La taille des images miniatures à utiliser dans la mosaïque.
    - color_file (str): Le nom du fichier CSV/JSON contenant les couleurs moyennes des images miniatures. 
    Attention en fonction du type de fichier à utiliser, il faut changer certaines lignes (mises en commentaires)

    Returns:
    - np.ndarray: L'image de la mosaïque générée.
    """
    mean_color_dir_csv(path_dir, color_file) #CSV
    #mean_color_dir_csv(path_dir, color_file) #JSON
    shape = img_src.shape[:2]

    #img_resized = cv2.resize(img_src, (shape[0]//4,shape[1]//4)) #on redimensionne l image pour pas que les calculs soient trop longs.
    img_resized = cv2.resize(img_src, (shape[1],shape[0]))

    shape = img_resized.shape[:2]
    b, g, r = cv2.split(img_resized)
    img_dest = np.zeros((shape[0]*n, shape[1]*n, 3), dtype=np.uint8) 
    for y in tqdm(range(0, shape[0])):
        for x in (range(0, shape[1])):
            color = (b[y, x], g[y, x], r[y, x])
            closest_img = find_img_color_csv(color, color_file) #CSV
            #closest_img=find_img_color_json(color, color_file) #JSON
            img_mini_colo1 = cv2.resize(cv2.imread(os.path.join(path_dir,closest_img)), (n, n)) #CSV
            img_mini_colo2=mosaic.adjust_color(img_mini_colo1,color)
            #img_mini_colo = cv2.resize(cv2.imread(os.path.join(closest_img)), (n, n)) #JSON
            img_dest[n*y:n*(y+1), n*x:n*(x+1)] = img_mini_colo2[:,:]
    return img_dest

def mosaic_zoom(path_src: str, path_dir: str, path_prefix_output: str, nw: int, nh: int):
    """
    Crée une série d'images mosaïques zoomées à partir d'une image source et d'un ensemble d'images miniatures.

    Args:
        path_src (str): Chemin de l'image source.
        path_dir (str): Chemin du répertoire contenant les images miniatures.
        path_prefix_output (str): Préfixe pour les noms de fichier de sortie.
        nw (int): Nombre de niveaux de zoom en largeur.
        nh (int): Nombre de niveaux de zoom en hauteur.
    """
    img_src = cv2.imread(path_src)
    img_resized = cv2.resize(img_src, (2 ** nw, 2 ** nh))

    #cv2.imwrite(f"{path_prefix_output}_1.jpg",cv2.resize(img_resized, (2 ** (nw-2), 2 ** (nh-2)))) # On sauve directement l'image en diminuant ses dimensions 
    #pour que lors de la vidéo, toutes les images soient de la meme taille

    cv2.imwrite(f"{path_prefix_output}_1.jpg",cv2.resize(img_resized, (2**nw, 2**nh)))
    h, w = img_resized.shape[:2]
    for i in range(2, 8): 
        h01=(h//2)-(h//(2**i))
        h02=(h//2)+(h//(2**i))
        w01=(w//2)-(w//(2**i))
        w02=(w//2)+(w//(2**i))
        img_resized_cropped = mosaic.crop_and_resize(img_resized, (h01, w01, h02, w02), w//(2**i), h//(2**i))

        mosaic_img = build_mosaic(img_resized_cropped, path_dir, 2**i, "colors_mean.csv") # Création de la mosaïque CSV
        #mosaic_img = build_mosaic(img_resized_cropped, path_dir, 2**i, "dict_img.json") #JSON

        cv2.imwrite(f"{path_prefix_output}_{i}.jpg", mosaic_img)

""""
for i in mean_color_dir("../Imgaes rendu Prof").items():
    print(i)
print(find_img_color("../Imgaes rendu Prof",[100, 150, 200]))



mean_color_dir("Images_oiseaux", "colors_mean.csv") 
mosaic_zoom("beau5.jpg","Images_oiseaux","beau",9,9)


cv2.imwrite("ara2.jpg",build_mosaic(cv2.imread("ara.jpg"), "Images_oiseaux", 100,"colors_mean.csv"))
"""

