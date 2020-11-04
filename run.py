from flask import Flask, url_for, request, send_from_directory, g, jsonify
from compress_image import compress_images, BASE_FOLDER
from utils import get_images
import logging

LOGGER = logging.getLogger()

flask_app = Flask(__name__, static_folder='web/base/static')


@flask_app.route("/compress_image", methods=["POST"])
def compress():
    try:
        if request.method == 'POST':
            params = request.get_json()
            imgs = get_images(params['image'])
            img_names = compress_images(imgs)
            return jsonify({
                "status_code": 200,
                "message": "Image has saved.",
                "image_name": img_names
            })
        else:
            return {
                "status_code": 400,
                "message": "Please sent request with GET method"
            }
    except Exception as e:
        return jsonify({
            "status_code": 500,
            "message": "Internal Server Error."
        })


@flask_app.route("/get_image/<filename>")
def get_image(filename):
    return send_from_directory(BASE_FOLDER, filename, as_attachment=True)


if __name__ == '__main__':
    flask_app.run("0.0.0.0", debug=True)
