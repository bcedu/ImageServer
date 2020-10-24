from flask import Flask, request, render_template, send_from_directory, abort, json, make_response, Response, jsonify
import argparse
from database import setup_db
from models import Image
import random


class ImageServer(object):

    # Prepare the server
    app = Flask(__name__)
    db = None

    def __init__(self, host, port, db_uri):
        # setup db
        db = setup_db(uri=db_uri)
        # Start the server
        ImageServer.app.run(host=host, port=port)

    @staticmethod
    @app.route('/image/<string:id>', methods=['GET'])
    def get_image(id):
        res = Image.query.filter(Image.id == id).first()
        if not res:
            return ImageServer.get_404()
        fullpath = res.path
        resp = make_response(open(fullpath, 'rb').read())
        resp.content_type = "image/jpeg"
        return resp

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
