import cv2
import numpy as np
import mosaic
from tqdm import tqdm
import os


def linear_range(val1: int, val2: int, n: int)->list:
    """
    Crée une liste de valeurs linéairement espacées entre val1 et val2, avec n éléments.

    Args:
        val1 (int): La valeur de départ.
        val2 (int): La valeur de fin.
        n (int): Le nombre d'éléments dans la liste.

    Returns:
        list: Liste des valeurs linéairement espacées.
    Note:
        On aurait pu utiliser une fonction déjà existante np.lispace
    
     Examples:
        >>> linear_range(0, 10, 5)
        [0, 2, 5, 7, 10]
        >>> linear_range(1, 4, 4)
        [1, 2, 3, 4]
        >>> linear_range(-3, 3, 7)
        [-3, -2, -1, 0, 1, 2, 3]
        >>> linear_range(0, 50, 6)
        [0, 10, 20, 30, 40, 50]
        >>> linear_range(0, 50, 7)
        [0, 8, 16, 25, 33, 41, 50]
    """
    return [int((val1+((val2-val1)/(n-1))*i)) for i in range(n)]

def rect_morphing(rect_src:tuple, rect_dest:tuple, nb_steps:int):
    """
    Génère une séquence de rectangles en effectuant une transition linéaire entre rect_src et rect_dest.

    Args:
        rect_src (tuple): Le rectangle source sous forme de tuple (y1, x1, y2, x2).
        rect_dest (tuple): Le rectangle cible sous forme de tuple (y1, x1, y2, x2).
        nb_steps (int): Le nombre d'étapes dans la transition.

    Returns:
        list: Liste de rectangles représentant la transition.

    Examples:
        >>> rect_morphing((0, 0, 10, 10), (10, 10, 20, 20), 3)
        [[0, 0, 10, 10], [5, 5, 15, 15], [10, 10, 20, 20]]
        >>> rect_morphing((0, 0, 10, 10), (0, 0, 10, 10), 2)
        [[0, 0, 10, 10], [0, 0, 10, 10]]
        >>> rect_morphing((0, 0, 100, 100), (50, 50, 150, 150), 3)
        [[0, 0, 100, 100], [25, 25, 125, 125], [50, 50, 150, 150]]
        >>> rect_morphing((0, 0, 100, 100), (50, 50, 100, 100), 4)
        [[0, 0, 100, 100], [16, 16, 100, 100], [33, 33, 100, 100], [50, 50, 100, 100]]
    """
    y1=linear_range(rect_src[0],rect_dest[0],nb_steps)
    x1=linear_range(rect_src[1],rect_dest[1],nb_steps)
    y2=linear_range(rect_src[2],rect_dest[2],nb_steps) 
    x2=linear_range(rect_src[3],rect_dest[3],nb_steps)
    return [[y1[i],x1[i],y2[i],x2[i]] for i in range(nb_steps)]

def make_movie(img: np.ndarray, rect_src: tuple, rect_dest: tuple, output_filename: str, w: int, h: int, fps: int, duration: int):
    """
    Crée un fichier vidéo représentant la transition entre deux rectangles dans une image.

    Args:
        img (np.ndarray): L'image source.
        rect_src (tuple): Le rectangle source sous forme de tuple (y1, x1, y2, x2).
        rect_dest (tuple): Le rectangle cible sous forme de tuple (y1, x1, y2, x2).
        output_filename (str): Nom du fichier de sortie.
        w (int): Largeur de l'image de sortie.
        h (int): Hauteur de l'image de sortie.
        fps (int): Nombre d'images par seconde du fichier vidéo.
        duration (int): Durée de la vidéo en secondes.
    """
    nb_images = fps * duration
    rect_sequence = rect_morphing(rect_src, rect_dest, nb_images)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, fps, (w, h))
    for rect in tqdm(rect_sequence):
        frame = mosaic.crop_and_resize(img, (rect[1], rect[0], rect[3], rect[2]), w, h)
        out.write(frame)
    out.release()

def zoom_x2_mp4(input_filename: str, output_filename: str, duration: int):
    """
    Crée une vidéo zoom x2 à partir d'une image en entrée.

    Args:
        input_filename (str): Nom du fichier image en entrée.
        output_filename (str): Nom du fichier vidéo en sortie.
        duration (int): Durée de la vidéo en secondes.
    """
    img=cv2.imread(input_filename)
    shape=img.shape[:2]
    make_movie(img, (0,0,shape[1],shape[0]),(shape[1]//4,shape[0]//4,(3*shape[1])//4,(3*shape[0])//4) , output_filename, shape[1],shape[0], 60, duration)

def recursive_zoom_mp4(input_prefix: str, i_max: int, output_filename: str, duration: int):
    """
    Crée un fichier vidéo résultant de la concaténation des vidéos zoom générées à partir d'une série d'images.

    Args:
        input_prefix (str): Le préfixe du nom des fichiers d'images.
        i_max (int): Le nombre maximal d'images à traiter.
        output_filename (str): Le nom du fichier vidéo de sortie.
        duration (int): La durée de chaque vidéo zoom en secondes.

    Note:
        Cette fonction génère des vidéos zoom à partir des images portant le préfixe input_prefix suivi d'un nombre
        croissant de 1 à i_max. Chaque vidéo zoom est centrée sur l'image correspondante et a une durée de duration
        secondes. Ensuite, elle utilise la commande ffmpeg pour concaténer toutes ces vidéos en un seul fichier vidéo
        nommé output_filename.
    """
    zoom_files = []
    concat_list_filename = "concat_list.txt"  
    
    for i in range(1, i_max+1):
        input_filename = f"{input_prefix}_{i}.jpg"
        zoom_output = f"zoom_{input_prefix}_{i}.mp4"
        zoom_x2_mp4(input_filename, zoom_output, duration)
        zoom_files.append(zoom_output)

    with open(concat_list_filename, "w") as file:
        for zoom_file in zoom_files:
            file.write(f"file '{zoom_file}'\n")

    os.system(f"ffmpeg -f concat -i {concat_list_filename} -c copy {output_filename}")
    #os.remove(concat_list_filename)
"---------------------------------------"
#____________________TESTS____________________
"""""
for elt in  rect_morphing((0, 0, 100, 100), (50, 50, 100, 100), 4):
    print(elt)

print(linear_range(0, 50, 6))
print(linear_range(0, 50, 7))

img= cv2.imread("ara.jpg")
make_movie(img, (0, 0, 14000, 35000), (0,0,70,70), "ara.mp4", img.shape[1]//10, img.shape[0]//10, 60, 10)
zoom_x2_mp4("baby_6.jpg","baby6video.mp4",5)

recursive_zoom_mp4("beauceron",7,"beauceron_recursive.mp4",2)

img= cv2.imread("ara.jpg")
make_movie(img, (0, 0, 14000, 35000), (0,0,70,70), "ara.mp4", img.shape[1]//10, img.shape[0]//10, 60, 10)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
"""

