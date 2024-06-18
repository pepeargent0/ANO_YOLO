import json
import os
import shutil
from PIL import Image

label_map = {
    "1O": 0, "1C": 1, "1E": 2, "1B": 3, "2O": 4, "2C": 5, "2E": 6, "2B": 7,
    "3O": 8, "3C": 9, "3E": 10, "3B": 11, "4O": 12, "4C": 13, "4E": 14, "4B": 15,
    "5O": 16, "5C": 17, "5E": 18, "5B": 19, "6O": 20, "6C": 21, "6E": 22, "6B": 23,
    "7O": 24, "7C": 25, "7E": 26, "7B": 27, "8O": 28, "8C": 29, "8E": 30, "8B": 31,
    "9O": 32, "9C": 33, "9E": 34, "9B": 35, "10O": 36, "10C": 37, "10E": 38, "10B": 39,
    "11O": 40, "11C": 41, "11E": 42, "11B": 43, "12O": 44, "12C": 45, "12E": 46, "12B": 47,
    "J": 48
}


def convert_labelme_to_yolo(labelme_file, yolo_file, image_file):
    with Image.open(image_file) as img:
        image_width, image_height = img.size

    with open(labelme_file, 'r') as f:
        data = json.load(f)

    with open(yolo_file, 'w') as f:
        for shape in data['shapes']:
            label = shape['label']
            class_id = label_map[label]

            points = shape['points']
            x_min = min(p[0] for p in points)
            y_min = min(p[1] for p in points)
            x_max = max(p[0] for p in points)
            y_max = max(p[1] for p in points)

            x_center = (x_min + x_max) / 2 / image_width
            y_center = (y_min + y_max) / 2 / image_height
            width = (x_max - x_min) / image_width
            height = (y_max - y_min) / image_height

            f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")


labelme_dir = 'json'
output_dir = 'yolo'

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(labelme_dir):
    if filename.endswith('.json'):
        labelme_file = os.path.join(labelme_dir, filename)
        yolo_file = os.path.join(output_dir, filename.replace('.json', '.txt'))
        image_file = os.path.join(labelme_dir, filename.replace('.json', '.jpeg'))

        if os.path.exists(image_file):
            convert_labelme_to_yolo(labelme_file, yolo_file, image_file)
            shutil.copy(image_file, output_dir)
            print(f"Convertido {filename} a {yolo_file} y copiado {image_file} a {output_dir}")
        else:
            print(f"No se encontró la imagen {image_file} para {filename}")



"""
import os

# Ruta a la carpeta que contiene los archivos JSON
labelme_dir = 'json'

# Prefijo para los nombres de archivo
prefix = '52256_daniel_ponce_'

# Obtener lista de archivos en la carpeta
files = os.listdir(labelme_dir)

# Inicializar contador
counter = 1

# Renombrar cada archivo
for filename in files:
    # Obtener la extensión del archivo
    _, extension = os.path.splitext(filename)

    # Construir nuevo nombre de archivo
    if counter < 10:
        sub_fijo = '0'+str(counter)
    else:
        sub_fijo = counter
    new_filename = f"{prefix}{sub_fijo}{extension}"

    # Obtener rutas completas a los archivos
    old_file = os.path.join(labelme_dir, filename)
    new_file = os.path.join(labelme_dir, new_filename)

    # Renombrar el archivo
    os.rename(old_file, new_file)
    print(f"Renombrado {filename} a {new_filename}")

    # Incrementar contador
    counter += 1

#52256_daniel_ponce
"""