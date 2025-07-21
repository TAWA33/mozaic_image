""" Pour taper dans le terminal, se mettres dans le dossier et ensuite taper : chmod +x ./max.py pour avoir les droits et ensuite taper ./max.py <listes nombres>"""
import os
import sys
import make_video
import mosaic

def main():
    if len(sys.argv) != 6:
        print("Usage: python3 make_movie.py <MASTER_IMG> <THUMBNAIL_IMG> <DURATION> <ZOOM_MAGNITUDE> <OUTPUT_FILENAME>")
        print("Exemple: python3 make_movie.py baby.jpg baby.jpg 2 9 baby_zoom.mp4")
        return

    master_img = sys.argv[1]
    thumbnail_img = sys.argv[2]
    duration = int(sys.argv[3])
    zoom_magnitude = int(sys.argv[4])
    output_filename = sys.argv[5]
    path_prefix=os.path.splitext(master_img)[0]
    print(path_prefix)
    mosaic.mosaic_zoom(master_img, thumbnail_img, path_prefix, zoom_magnitude, zoom_magnitude)
    make_video.recursive_zoom_mp4(path_prefix, 7, output_filename, duration)

if __name__ == "__main__":
    main()