import logging
from flask_eureka import Eureka
from flask_eureka.eureka import eureka_bp
from flask import Flask, request, send_from_directory, jsonify, send_file
from flask_restful import reqparse, Resource, Api
from werkzeug.datastructures import FileStorage
from compress_image import compress_image, BASE_FOLDER
from utils import get_image, ImageException

LOGGER = logging.getLogger()

flask_app = Flask(__name__, static_folder='web/base/static')
api = Api(flask_app)


flask_app.register_blueprint(eureka_bp)
flask_app.config["SERVICE_NAME"] = "image-utils"
flask_app.config["EUREKA_SERVICE_URL"] = "http://internal-interal-eureka-elb-1725501689.ap-southeast-1.elb.amazonaws.com/"
flask_app.config["EUREKA_INSTANCE_PORT"] = 15001
flask_app.config["EUREKA_INSTANCE_HOSTNAME"] = "172.16.10.111"
flask_app.config["EUREKA_HEARTBEAT"] = 60
eureka = Eureka(flask_app)
eureka.register_service(name="image-utils", vip_address="image-utils")


class CompressImageApi(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("image", required=True, location=['form', 'args', 'json', 'files'])
            args = parser.parse_args(strict=True)
            if "FileStorage" in args.image:
                parser.replace_argument('image', type=FileStorage, required=True, location='files')
            args = parser.parse_args(strict=True)
            img, byte_image = get_image(args.image)
            img_compressed = compress_image(img, byte_image)
            img_compressed.seek(0)
            return send_file(
                img_compressed,
                mimetype='image/jpeg',
                as_attachment=True,
                attachment_filename="compressed_image.jpg"
            )
        except ImageException as e:
            return {
                "status_code": 400,
                "message": str(e)
            }
        except Exception as e:
            return {
                "status_code": 500,
                "message": "Internal Server Error."
            }


# @flask_app.route("/get_image/<filename>")
# def get_image(filename):
#     return send_from_directory(BASE_FOLDER, filename, as_attachment=True)


api.add_resource(CompressImageApi, '/compress-image')

if __name__ == '__main__':
    flask_app.run("0.0.0.0", port=15000, debug=True)
