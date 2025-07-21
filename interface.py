import tkinter as tk  
from tkinter import filedialog  
from PIL import Image, ImageTk
import cv2 
import os 
import mosaic_rep 
import make_video

def choisir_image_principale():
    """
    Fonction pour permettre à l'utilisateur de choisir l'image principale à utiliser pour la mosaïque.
    Note:
        On change le chemin de l'image. Il faut que le chemin soit depuis le meme dossier que le fichier.py (relatif)
    """
    global img_principale, chemin_image
    chemin_image = filedialog.askopenfilename(title="Choisir l'image principale", filetypes=[("Fichier Images", '.jpg')])
    chemin_image=os.path.relpath(chemin_image, start=os.curdir) 
    print(chemin_image)
    if chemin_image:
        img = cv2.imread(chemin_image) 
        if img is not None:
            img_principale = img 
            tick_image_label.config(image=tick_image)
        else:
            tk.messagebox.showerror("Erreur", "Impossible d'ouvrir l'image principale. Veuillez vérifier le chemin du fichier.")  

def choisir_dossier_images():
    """
    Fonction pour permettre à l'utilisateur de choisir le dossier contenant les images miniatures utilisées pour la mosaïque.
    """
    global chemin_dossier_images 
    chemin_dossier_images = filedialog.askdirectory(title="Choisir le dossier contenant les petites images") 
    if chemin_dossier_images: #lorsque le dossier est sélectionné on rentre dans la boucle
        if not any(f.endswith(('.png', '.jpg', '.jpeg', '.gif')) for f in os.listdir(chemin_dossier_images)): #si le dossier ne contient pas d'images
            tk.messagebox.showerror("Erreur", "Le dossier sélectionné ne contient pas d'images.") 
        else:
            tick_dossier_label.config(image=tick_image)


def generer_mosaique():
    """
    Fonction pour générer la mosaïque à partir de l'image principale et des images miniatures.
    """
    global img_principale, chemin_dossier_images 
    if img_principale is None: #si aucune image n'a été sélectionnée, on préviens l'utilisateur
        tk.messagebox.showerror("Erreur", "Veuillez choisir une image principale.")  
        return
    if chemin_dossier_images is None: 
        tk.messagebox.showerror("Erreur", "Veuillez choisir un dossier contenant les petites images.")
        return

    #mosaic_rep.mean_color_dir_csv(str(chemin_dossier_images), "colors_mean_interface.csv") #on créé ou modifie le fichier csv
    #On ne recréé pas le fichier car il y a trop d images dans /persons
    #img_mosaique = mosaic_rep.build_mosaic(img_principale, chemin_dossier_images, 70, "colors_mean_interface.csv") #CSV
    img_mosaique = mosaic_rep.build_mosaic(img_principale, chemin_dossier_images, 10, "dict_img.json") #JSON
    #Peut aussi être modifier pour améliorer la vitesse d'execution
    cv2.imwrite("mosaique.jpg", img_mosaique)
    tk.messagebox.showinfo("Succès", "La mosaïque a été générée avec succès !!")

def generer_video():
    """
    Fonction pour générer la vidéo à partir de l'image principale et des images miniatures.
    """
    global img_principale, chemin_dossier_images 
    if img_principale is None:
        tk.messagebox.showerror("Erreur", "Veuillez choisir une image principale.")  
        return
    if chemin_dossier_images is None: 
        tk.messagebox.showerror("Erreur", "Veuillez choisir un dossier contenant les petites images.")
        return
    prefix="test"
    mosaic_rep.mosaic_zoom(chemin_image, chemin_dossier_images, prefix, 9, 9)
    make_video.recursive_zoom_mp4(prefix, 7, "video_recursiv.mp4", 2)
    tk.messagebox.showinfo("Succès", "La vidéo a été générée avec succès !!")

img_principale = None
chemin_dossier_images = None

fenetre = tk.Tk()
fenetre.title("Génération d'une mosaïque")
fenetre.configure(bg="#343834")

tick_image = Image.open("tick.png") 
tick_image = tick_image.resize((20, 20))
tick_image = ImageTk.PhotoImage(tick_image)

txt = tk.Label(fenetre, text="Sélectionnez l'image principale : ", fg="#FEE366", bg="#343834", font=("Helvetica", 12))
txt.pack(pady=10)

frame_image = tk.Frame(fenetre, bg="#343834")  
frame_image.pack()

btn_image_principale = tk.Button(frame_image, text="Parcourir", command=choisir_image_principale, bg="#E79D1A", fg="#594E3B", font=("Helvetica", 10, "bold"))
btn_image_principale.pack(side="left", padx=5)

tick_image_label = tk.Label(frame_image, image=None, bg="#343834")
tick_image_label.pack(side="left", padx=5)

txt2 = tk.Label(fenetre, text="Sélectionnez le dossier thématique des images mini formant l'image principale : ", fg="#FEE366", bg="#343834", font=("Helvetica", 12))
txt2.pack(pady=10)

frame_dossier = tk.Frame(fenetre, bg="#343834")  
frame_dossier.pack()

btn_dossier_images = tk.Button(frame_dossier, text="Parcourir", command=choisir_dossier_images, bg="#E79D1A", fg="#594E3B", font=("Helvetica", 10, "bold"))
btn_dossier_images.pack(side="left", padx=5)

tick_dossier_label = tk.Label(frame_dossier, image=None, bg="#343834")
tick_dossier_label.pack(side="left", padx=5)

btn_generer_mosaique = tk.Button(fenetre, text="Générer la mosaïque", command=generer_mosaique, bg="#EE541F", fg="white", font=("Helvetica", 12, "bold"))
btn_generer_mosaique.pack(padx=10,pady=10)

btn_generer_video = tk.Button(fenetre, text="Générer la vidéo", command=generer_video, bg="#EE541F", fg="white", font=("Helvetica", 12, "bold"))
btn_generer_video.pack(pady=10)

fenetre.mainloop()