import cv2
import mosaic
import mosaic_rep
import numpy as np
from tqdm import tqdm

def acoller(img1_filename:str,img2_filename:str):
    """
    Acolle deux images coupées en deux côte à côte horizontalement
    
    Args:
        img1_filename (str): Chemin de la première image.
        img2_filename (str): Chemin de la deuxième image.
    Note:
        Il faut que les deux images aient la même hauteur (on prends le min de l image 1 et 2)
    """
    img1=cv2.imread(img1_filename)
    img2=cv2.imread(img2_filename)
    h=min(img1.shape[0],img2.shape[0])
    img1_crop=mosaic.crop_and_resize(img1,(0,0,img1.shape[1],img1.shape[0]//2),img1.shape[0]//4,h//4) # //4 pour réduire le temps d'exécution
    img2_crop=mosaic.crop_and_resize(img2,(0,img2.shape[0]//2,img2.shape[1],img2.shape[0]),img2.shape[0]//4,h//4)
    img_coll=cv2.hconcat([img1_crop,img2_crop]) #permet de concatener horizontalement les deux images
    img_fin=mosaic_rep.build_mosaic(img_coll,"/persons",10,"dict_img.json")
    cv2.imwrite("colle.jpg",img_fin)
#acoller("beau5.jpg","beauceron.jpg")

def opac(img1:np.ndarray,img2:np.ndarray,opacite:float):
    """
    Permet de renvoyer une image composée de deux images en appliquant des opacités différentes
    
    Args:
        img1 (np.ndarray): Première image.
        img2 (np.ndarray): Deuxième image.
        opacite (float): Opacité de la première image.
        
    Returns:
        np.ndarray: Image résultante.
    Note:
        Il faut que les deux images soient de même dimensions
    """
    h, w = min(img1.shape[0], img2.shape[0]), min(img1.shape[1], img2.shape[1])
    img1=cv2.resize(img1,(w,h))
    img2=cv2.resize(img2,(w,h))
    superpos = cv2.addWeighted(img1, opacite, img2, 1 - opacite, 0)
    return superpos
    #cv2.imwrite(output_filename,superpos) #pour enregistrer image rajouter output dans les parametres
#opac(cv2.imread("beau5.jpg"),cv2.imread("beauceron.jpg"),"opac.jpg",200,200,0.5)

def fondu(img1_filename:str,img2_filename:str, output_filename:str, w:int,h:int, fps: int, duration: int):
    """
    Renvoie la vidéo de transition entre les deux images
    
    Args:
        img1_filename (str): Chemin de la première image.
        img2_filename (str): Chemin de la deuxième image.
        output_filename (str): Nom du fichier vidéo de sortie.
        w (int): Largeur des images dans la vidéo.
        h (int): Hauteur des images dans la vidéo.
        fps (int): Nombre d'images par seconde de la vidéo.
        duration (int): Durée de la transition en secondes.
    """
    img1 = cv2.resize(cv2.imread(img1_filename), (w, h))
    img2 = cv2.resize(cv2.imread(img2_filename), (w, h))
    nb_images=fps*duration
    opac_step=1/nb_images 
    frames = []
    for i in tqdm(range(nb_images)):
        opacite = i * opac_step
        frame = opac(img1, img2, opacite)
        frames.append(frame)
    video_writer = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
    for frame in frames:
        video_writer.write(frame)
    video_writer.release()
    cv2.destroyAllWindows()

#fondu("persons/2845.jpg", "persons/2517.jpg", "transition.mp4", 200, 200, 300, 3)