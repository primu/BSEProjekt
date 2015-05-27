import json
from PIL import Image
import sys

import numpy as np
from flask import Flask, jsonify, request
from flask.ext.cors import CORS, cross_origin

from helpers.image_processing import crop2, scale_to
from helpers.utils import full_path_for
from mpi.mpi_digit_recognition import MPIDigitRecognition


recognition = MPIDigitRecognition(full_path_for(sys.argv[1]))
recognition.run()

if recognition.is_main_node():
    app = Flask(__name__)
    cors = CORS(app)
    app.config["CORS_HEADERS"] = "Content-Type"

    def log(filename, data):
        with open(filename, "w") as file:
            file.write(json.dumps(data))

    def process_input_matrix(data):
        settings = recognition._config["neurons"]["class"]["settings"]
        sizes = recognition._config["neurons"]["class"]["size"]

        log("data1", data)
        data = np.array(data, np.uint8)
        data = 255 - data

        log("data2", data.tolist())

        data = Image.fromarray(data)
        data = crop2(data)
        data = scale_to(data, int(sizes[0]), int(sizes[1]))

        return data


    @app.route("/train", methods=["POST"])
    @cross_origin()
    def train():
        try:
            character = request.json["character"]
            data = request.json["data"]
            if data:
                settings = recognition._config["neurons"]["class"]["settings"]

                data = process_input_matrix(data)
                if True: #request.json["hard"]:
                    while str(recognition.query(data)["best_guess"]) != character:
                        recognition.train(character, data)

                return jsonify({"result": True})
            return jsonify({"result": False})
        except Exception as e:
            log("train", json.dumps(str(e)))
            return jsonify({"result": False})

    @app.route("/query", methods=["POST"])
    @cross_origin()
    def query():
        data = request.json
        if data:
            try:
                data = process_input_matrix(data)
                log("query", data)
            except Exception as e:
                log("log", str(e))
            return jsonify(recognition.query(data))
        return jsonify({"result": False})

    if __name__ == "__main__":
        try:
            app.run(host="0.0.0.0", port=int(sys.argv[2]))
        except KeyboardInterrupt:
            recognition.stop()