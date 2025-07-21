import os
import sys
import make_video
import mosaic_rep

#Pour que ça fonctionne il faut changer les autres fichiers (CSV/JSON)

def main():
    if len(sys.argv)!=6:
        print("Usage: python3 make_movie_rep.py <MASTER_IMG> <THUMBNAILS_DIR> <DURATION> <ZOOM_MAGNITUDE> <OUTPUT_FILENAME>")
        print("Exemple: python3 make_movie_rep.py beau5.jpg Images_oiseaux 2 9 beau_zoom.mp4")
        return

    master_img = sys.argv[1]
    thumbnail_dir = sys.argv[2]
    duration = int(sys.argv[3])
    zoom_magnitude = int(sys.argv[4])
    path_prefix=os.path.splitext(master_img)[0]
    print(path_prefix)
    output_filename = sys.argv[5]

    mosaic_rep.mosaic_zoom(master_img, thumbnail_dir, path_prefix, zoom_magnitude, zoom_magnitude)
    make_video.recursive_zoom_mp4(path_prefix, 7, output_filename, duration)

if __name__=="__main__":
    main()