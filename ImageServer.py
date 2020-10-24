from flask import Flask, request, render_template, send_from_directory, abort, json, make_response, Response, jsonify, redirect
import argparse
from database import setup_db
from models import Image
import random
import pathlib


class ImageServer(object):

    # Prepare the server
    app = Flask(__name__)
    db = None
    media_path = None
    media_url = None

    def __init__(self, host, port, db_uri, media_path=None, media_url=None):
        # setup db
        db = setup_db(uri=db_uri)
        if not media_path:
            media_path = str(pathlib.Path().absolute()) + "/www"
        if not media_url:
            media_url = media_path
        # Start the server
        ImageServer.app.run(host=host, port=port)

    @staticmethod
    def build_media_url(image):
        return image.path.replace(ImageServer.media_path, ImageServer.media_url)

    @staticmethod
    @app.route('/image/<string:id>', methods=['GET'])
    def get_image(id):
        # Busquem la imatge
        res = Image.query.filter(Image.id == id).first()
        if not res:
            return ImageServer.get_404()

        # Comprovem que podem donar aquesta imatge
        fullpath = res.path
        if not fullpath.startswith(ImageServer.media_path):
            return ImageServer.get_404()

        # Construim la resposta. Lo unic que no volem donar es el full path
        resp = {
            'name': res.name,
            'tags': res.tags,
            'id': res.id,
            'url': ImageServer.build_media_url(res)
        }
        return jsonify(resp)

    @staticmethod
    @app.route('/random_image', methods=['GET'])
    def get_random_image():
        res = Image.query.all()
        if not res:
            return ImageServer.get_404()
        return ImageServer.get_image(random.choice(res).id)

    @staticmethod
    @app.route('/random_image/<string:tag>', methods=['GET'])
    def get_random_image_by_tag(tag):
        search = "%{}%".format(tag)
        res = Image.query.filter(Image.tags.like(search)).all()
        if not res:
            return ImageServer.get_404()
        return ImageServer.get_image(random.choice(res).id)

    @staticmethod
    def get_404():
        res = Image.query.filter(Image.name == "404-not-found.jpg").first()
        return ImageServer.get_image(res.id)

def main(args):
    ImageServer(args.host, args.port, args.database)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ht", "--host", default="127.0.0.1", help="The hostname to listen on. Set this to '0.0.0.0' to have the server available externally as well. Defaults to '127.0.0.1'.")
    parser.add_argument("-p", "--port", default=5000, type=int, help="Port where the server will run. By default it's 5000.")
    parser.add_argument("-db", "--database", default='sqlite:///ImageServer.db')

    main(parser.parse_args())
