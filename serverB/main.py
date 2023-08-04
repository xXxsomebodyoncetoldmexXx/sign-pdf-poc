#!/usr/bin/env python3

import requests
from flask import Flask, request
from flask_restful import Resource, Api
from core import pdfservice, verify
from base64 import b64encode, b64decode

app = Flask(__name__)
api = Api(app)

SERVER_A = "http://localhost:8888"


def get_public_key():
    try:
        return requests.get(SERVER_A + "/api/signature").json().get("Public Key")
    except:
        return None


class SignatureService(Resource):
    def post(self):
        data = request.get_json(force=True).get("File")
        if not data:
            return {"Error": "Missing File parameter"}
        data = b64decode(data)

        pub_key = get_public_key()
        if not pub_key:
            return {"Error": "ServerA is offline"}

        signature = pdfservice.get_sign(data)
        if not signature:
            return {"Error": "Missing sign value"}

        data = pdfservice._normalize_pdf(data)

        try:
            verify.verify_pdf(signature, pub_key, data)
            return {"Result": "OK"}
        except:
            return {"Error": "File is not valid"}


@app.route("/")
def homepage():
    return "<h1>Bank B</h1>"


api.add_resource(SignatureService, "/api/check-signature")

if __name__ == "__main__":
    app.run(port=8889, host="0.0.0.0")
