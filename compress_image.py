import os
from io import BytesIO
from typing import List
from PIL import Image
import imagehash

BASE_DIM = 2000
FILE_SIZE_THRESHOLD = 500000
BASE_FOLDER = "data/"


def compress_images(imgs: List) -> List[str]:
    file_names = []
    for img in imgs:
        file_name = None
        try:
            file_name = compress_image(img)
        except:
            pass
        file_names.append(file_name)
    return file_names


def compress_image(img) -> str:
    hash = imagehash.dhash(img, hash_size=8)
    filename = "{}.jpg".format(hash)
    file_path = os.path.join(BASE_FOLDER, filename)
    if os.path.exists(file_path):
        return filename

    w, h = img.size
    max_dim = max(w, h)
    if max_dim > BASE_DIM:
        scale = BASE_DIM / max_dim
        new_w, new_h = int(scale * w), int(scale * h)
        img = img.resize((new_w, new_h), Image.ANTIALIAS)
    img_file = BytesIO()
    img.save(img_file, 'png')
    img_file_size = img_file.tell()
    if img_file_size > FILE_SIZE_THRESHOLD:
        img.save(file_path, optimize=True, quality=95)
    else:
        img.save(file_path, optimize=False, quality=100)
    return filename
