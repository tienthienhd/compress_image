import functools
import os
import time
from io import BytesIO
from typing import List
from PIL import Image
import imagehash

BASE_DIM = 2000
FILE_SIZE_THRESHOLD = 500000
BASE_FOLDER = "data/"


def timeit(f):
    @functools.wraps(f)
    def run(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        print("Time exec '{}': {:.3}s".format(f.__name__, end_time - start_time))
        return result

    return run


@timeit
def compress_images(imgs: List, byte_images: List[int]) -> List[str]:
    file_names = []
    for img, byte_image in zip(imgs, byte_images):
        file_name = None
        try:
            file_name = compress_image(img, byte_image)
        except:
            pass
        file_names.append(file_name)
    return file_names


# @timeit
# def compress_image(img) -> str:
#     hash = imagehash.dhash(img, hash_size=8)
#     filename = "{}.jpg".format(hash)
#     file_path = os.path.join(BASE_FOLDER, filename)
#     if os.path.exists(file_path):
#         return filename
#
#     w, h = img.size
#     max_dim = max(w, h)
#     if max_dim > BASE_DIM:
#         scale = BASE_DIM / max_dim
#         new_w, new_h = int(scale * w), int(scale * h)
#         img = img.resize((new_w, new_h), Image.ANTIALIAS)
#     img_file = BytesIO()
#     img.save(img_file, 'png')
#     img_file_size = img_file.tell()
#     if img_file_size > FILE_SIZE_THRESHOLD:
#         img.save(file_path, optimize=True, quality=95)
#     else:
#         img.save(file_path, optimize=False, quality=100)
#     return filename

@timeit
def compress_image(img, byte_image: int) -> BytesIO:
    w, h = img.size
    max_dim = max(w, h)
    if max_dim > BASE_DIM:
        scale = BASE_DIM / max_dim
        new_w, new_h = int(scale * w), int(scale * h)
        img = img.resize((new_w, new_h), Image.ANTIALIAS)

    img = img.convert('RGB')
    img_file_compressed = BytesIO()
    if byte_image > FILE_SIZE_THRESHOLD:
        img.save(img_file_compressed, 'jpeg', optimize=True, quality=95)
    else:
        img.save(img_file_compressed, 'jpeg', optimize=False, quality=100)
    output_size = img_file_compressed.tell()
    print("Image compressed remain {}%: {} bytes -> {} bytes".format(round(output_size * 100 / byte_image, 1),
                                                                     byte_image,output_size))
    return img_file_compressed
