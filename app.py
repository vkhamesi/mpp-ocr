from flask import Flask, request, abort
from flask_cors import CORS
from flask_restful import Api, Resource
from src import iban


class IbanDetector(Resource):
    def post(self):
        prediction = iban.guess(request.files['file'])
        if (prediction is None) or (not all(prediction.values())):
            abort(404)
        else:
            return prediction

app = Flask(__name__)
CORS(app)

api = Api(app)

api.add_resource(IbanDetector, "/guess_iban")

if __name__ == "__main__":
    app.run(host='127.0.0.1')