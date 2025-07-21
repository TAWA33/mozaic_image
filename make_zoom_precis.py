import os
import sys
import cv2
import zoom_precis
import mosaic_rep

def main():
    if len(sys.argv) != 8:
        print("Usage: python3 make_zoom_precis.py <MASTER_IMG> <PATH_DIR> <DURATION> <ZOOM_POINT_X> <ZOOM_POINT_Y> <ZOOM_MAGNITUDE> <OUTPUT_FILENAME>")
        print("Exemple: python3 make_zoom_precis.py baby.jpg Images_oiseaux 2 200 150 10 baby_zoom.mp4")
        return

    master_img = sys.argv[1]
    path_dir=sys.argv[2]
    duration = int(sys.argv[3])
    zoom_point_x = int(sys.argv[4])
    zoom_point_y = int(sys.argv[5])
    zoom_magnitude = int(sys.argv[6])
    output_filename = sys.argv[7]
    path_prefix = os.path.splitext(master_img)[0]
    
    img_mast=cv2.imread(master_img)
    shape=img_mast.shape[:2]
    if zoom_point_x>shape[0] or zoom_point_x<0 or zoom_point_y>shape[1] or zoom_point_y<0:
        print("Les coordonnées de zoom sont incompatibles avec l'image.")
        print("le point de zoom sort de l'image ou est trop proche du bord pour pouvoir faire un zoom")
        return

    mosaic_rep.mosaic_zoom(master_img, path_dir, path_prefix, zoom_magnitude, zoom_magnitude)
    zoom_precis.recursive_zoom_precis(master_img, path_dir, (zoom_point_x, zoom_point_y), output_filename, duration)

if __name__ == "__main__":
    main()