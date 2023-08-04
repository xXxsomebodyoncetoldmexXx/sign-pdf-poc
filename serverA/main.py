#!/usr/bin/env python3

from flask import Flask, request
from flask_restful import Resource, Api
from core import key, pdfservice
from base64 import b64encode, b64decode

app = Flask(__name__)
api = Api(app)
keyman = key.KeyManagement()


class SignatureService(Resource):
    def get(self):
        return {"Public Key": b64encode(keyman.get_public_key()).decode()}

    def post(self):
        data = request.get_json(force=True).get("File")
        if not data:
            return {"Error": "Missing File parameter"}
        data = b64decode(data)
        data = pdfservice._normalize_pdf(data)
        signature = keyman.sign(data)
        data = pdfservice.add_sign(data, signature)
        return {"Signed File": b64encode(data).decode()}


@app.route("/")
def homepage():
    return "<h1>Bank A</h1>"


api.add_resource(SignatureService, "/api/signature")

if __name__ == "__main__":
    app.run(port=8888, host="0.0.0.0")
