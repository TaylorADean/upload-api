from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import werkzeug
import random, string


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

signatures = []


class Uploader(Resource):
    def post(self, signature):

        if signature not in signatures:
            return "Invalid signature", 400

        parse = reqparse.RequestParser()
        parse.add_argument(
            'file',
            type=werkzeug.datastructures.FileStorage,
            location='files'
        )
        args = parse.parse_args()

        upload_file = args['file']
        upload_file.save("temp.txt")

        with open('temp.txt', 'r') as f:
            lines = f.readlines()
            num_lines = len(lines)

        return { 'numLines': num_lines }, 201


class Link(Resource):
    def get(self):
        x = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        signatures.append(x)

        return {'link': f'http://localhost:5000/upload/{x}'}


api.add_resource(Uploader, '/upload/<signature>')
api.add_resource(Link, '/link')

if __name__ == '__main__':
    app.run(debug=True)
