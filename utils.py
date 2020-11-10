import base64
import functools
import io
import logging
import re
import time
import urllib
import urllib.request
from werkzeug.datastructures import FileStorage

from PIL import Image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tiff',
                      'png"', 'jpg"', 'jpeg"', 'tiff"'}

DEBUG = False

LOGGER = logging.getLogger()


def timeit(f):
    @functools.wraps(f)
    def run(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        LOGGER.info("Time exec '{}': {:.3}s".format(f.__name__, end_time - start_time))
        return result

    return run


def is_support_type(filename):
    """Check type support"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@timeit
def url_to_image(url):
    """Download image from url"""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=5)
    data = resp.read()
    bytes_image = io.BytesIO(data)
    image = Image.open(bytes_image)
    return image, len(data)


@timeit
def stream_to_image(stream):
    """Parser image in bytes"""
    data = stream.read()
    bytes_image = io.BytesIO(data)
    image = Image.open(bytes_image)

    return image, len(data)


@timeit
def base64_to_image(img_string):
    """Parser image from base64"""
    img_string = re.sub('^data:image/[a-z]+;base64,', '', img_string)
    img_data = base64.b64decode(img_string)
    bytes_image = io.BytesIO(img_data)
    image = Image.open(bytes_image)
    return image, len(img_data)


@timeit
def image_to_base64(img):
    pil_img = Image.fromarray(img[..., ::-1], mode="RGB")
    buff = io.BytesIO()
    pil_img.save(buff, format="png")

    encoded = base64.b64encode(buff.getvalue())
    return encoded.decode('utf-8')


class ImageException(Exception):
    pass


def get_images(images):
    imgs = []
    byte_images = []
    for image in images:
        img, bytes_image = get_image(image)
        imgs.append(img)
        byte_images.append(bytes_image)
    return imgs, byte_images


def get_image(image):
    img = None
    bytes_image = 0
    try:
        if isinstance(image, str):
            if len(image) < 2:
                raise ImageException("String image is wrong format")
            if image.startswith("http"):
                img, bytes_image = url_to_image(image)
            else:
                img, bytes_image = base64_to_image(image)
        elif isinstance(image, FileStorage):
            if is_support_type(image.filename):
                img, bytes_image = stream_to_image(image)
            else:
                raise ImageException("Image is wrong format")

    except Exception as e:
        raise e
    return img, bytes_image