import cv2
import numpy as np
import mosaic
import apparition
from tqdm import tqdm
import mosaic_rep
import make_video
import os

#On modifie les fonctions de make_video.py pour zoommer sur un pixel précis (x,y)

def make_movie_precis(img : np.ndarray, rect_src: tuple, output_filename: str, zoom_point: tuple, n_dest:int, w: int, h: int, fps:int, duration:int):
    """
    Crée une vidéo zoomée sur un point spécifique (x, y).

    Args:
        img (np.ndarray): Image source.
        rect_src (tuple): Tuple de coordonnées de la région source à zoomer.
        output_filename (str): Nom du fichier vidéo de sortie.
        zoom_point (tuple): Coordonnées du point de zoom (x, y).
        n_dest (int): Taille de la zone de destination.
        w (int): Largeur de la vidéo de sortie.
        h (int): Hauteur de la vidéo de sortie.
        fps (int): Nombre d'images par seconde de la vidéo.
        duration (int): Durée de la vidéo en secondes.

    Note:
        Attention, il faut que (y-n_dest,x-n_dest,y+n_dest,x+n_dest) soient des coordonnées positives et appartenant à l'image sinon il peut y avoir des problèmes
    """
    y,x=zoom_point
    nb_images = fps * duration
    rect_sequence=make_video.rect_morphing(rect_src, (y-n_dest,x-n_dest,y+n_dest,x+n_dest), nb_images)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, fps, (w, h))
    for rect in tqdm(rect_sequence):
        frame = mosaic.crop_and_resize(img, (rect[1], rect[0], rect[3], rect[2]), w, h)
        out.write(frame)
    out.release()

def zoom_precis(img: np.ndarray, zoom_point:tuple,output_filename: str, duration: int):
    """
    Crée une vidéo zoom où l'image finale a la taille la plus grande possible, centrée sur le point de zoom.

    Args:
        img (np.ndarray): Image source.
        zoom_point (tuple): Coordonnées du point de zoom (x, y).
        output_filename (str): Nom du fichier vidéo de sortie.
        duration (int): Durée de la vidéo en secondes.

    Note:
        On doit calculer un n pour rester à l'intérieur de l'image. On determine le minimum entre le point x et w-x 
        en fonction de si le point est du côté gauche ou droite de l'image. On fait de même pour y et on fait le minimum entre x et y.
        On appelle donc la fonction précédente avec le n calculé.
    """
    x,y=zoom_point
    n=min(min(x,img.shape[0]-x),min(y,img.shape[1]-y))
    make_movie_precis(img, (0,0,img.shape[1],img.shape[0]), output_filename, (x,y),n,img.shape[0],img.shape[1], 100, duration)

def recursive_zoom_precis(input_filename:str,path_dir:str,zoom_point:tuple,output_filename:str,duration:int):
    """
    Crée une vidéo zoom pour montrer la mosaïque à un point spécifique.

    Args:
        input_filename (str): Nom du fichier image d'entrée.
        path_dir (str): Chemin du répertoire contenant les images de la mosaïque.
        zoom_point (tuple): Coordonnées du point de zoom (x, y).
        output_filename (str): Nom du fichier vidéo de sortie.
        duration (int): Durée de la vidéo en secondes.
    Note:
        Cette fonction crée une vidéo zoom pour afficher une mosaïque à un point spécifique de l'image.
        Elle commence par ajouter une vidéo d'apparition (`input_filename`) au début de la séquence. Cette vidéo est redimensionnée pour avoir les mêmes dimensions que les autres vidéos de la séquence.
        Ensuite, la fonction recalcule la taille de la région de zoom (`n_dest`) comme dans la fonction précédente, puis enregistre une image centrée sur le point de zoom avec une taille de région de zoom de 2n x 2n.
        La première étape du zoom est effectuée sans mosaïque pour permettre un zoom ultérieur centré sur le point spécifique.
        Les vidéos de zoom et de mosaïque sont ensuite générées à partir de cette image.
        Les vidéos de zoom sont redimensionnées pour avoir les mêmes dimensions que les autres vidéos de la séquence.
        Enfin, les vidéos sont concaténées dans l'ordre suivant : vidéo d'apparition, vidéo de zoom initial, vidéo de mosaïque, vidéo de zoom final.
    
        La commande -fflags +genpts permet de forcer la réécriture des horodatages (pour ensuite les concaténer sans problèmes)
    """
    img=cv2.imread(input_filename)
    apparition.ajout(input_filename,"test_ajout.mp4",100,100)
    x,y=zoom_point
    w=min(x,img.shape[0]-x)
    h=min(y,img.shape[1]-y)
    n_dest=min(h,w)

    cv2.imwrite("img1.jpg", mosaic.crop_and_resize(img,(y-n_dest,x-n_dest,y+n_dest,x+n_dest),n_dest,n_dest))
    zoom_precis(img, (x,y),"test1.mp4",duration)
   
    mosaic_rep.mosaic_zoom("img1.jpg",path_dir,"img1",8,8)
    make_video.recursive_zoom_mp4("img1", 7, "test3.mp4", duration)

    os.system(f"""ffmpeg -i test1.mp4 -vf "scale={2**8}:{2**8}" test2.mp4""")
    os.system(f"""ffmpeg -i test_ajout.mp4 -vf "scale={2**8}:{2**8}" test_ajout2.mp4""")

    os.system(f"ffmpeg -i test_ajout2.mp4 -fflags +genpts test_apparition.mp4")
    os.system(f"ffmpeg -i test2.mp4 -fflags +genpts test_debut.mp4")
    os.system(f"ffmpeg -i test3.mp4 -fflags +genpts test_fin.mp4")

    concat_list_filename = "concat_list2.txt"
    with open(concat_list_filename, "w") as file:
        file.write(f"file 'test_apparition.mp4'\n")
        file.write(f"file 'test_debut.mp4'\n")
        file.write(f"file 'test_fin.mp4'\n")

    os.system(f"ffmpeg -f concat -i {concat_list_filename} -c copy {output_filename}")


"---------------------------------------"
#____________________TESTS____________________
"""""
#Pour le test, le zoom point il faut indiquer d'abord x puis y
img= cv2.imread("mosaique_persons.jpg")
make_movie_precis(img, (0,0,img.shape[1], img.shape[0]), "_test.mp4",(200, 2200),20, img.shape[0], img.shape[1], 100, 5)
zoom_precis(cv2.imread("mosaique_persons.jpg"),(2220,168),"zoom_precis.mp4",3) #il faut que les coordonnées du point soit supérieur à n

recursive_zoom_precis("Images_oiseaux/martin_pecheur2.jpg","Images_oiseaux",(150,110),"test.mp4",1)

"""
