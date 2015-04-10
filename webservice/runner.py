from flask import Flask, jsonify, request

from flask.ext.cors import CORS, cross_origin
from helpers.path_for import full_path_for
from mpi.mpi_digit_recognition import MPIDigitRecognition


recognition = MPIDigitRecognition(full_path_for("conf.json"))
recognition.run()

if recognition.is_main_node():
    app = Flask(__name__)
    cors = CORS(app)
    app.config["CORS_HEADERS"] = "Content-Type"

    @app.route("/train", methods=["POST"])
    @cross_origin()
    def train():

        return jsonify({"result": True})

    @app.route("/query", methods=["POST"])
    @cross_origin()
    def query():
        data = request.json
        if data:
            return jsonify(recognition.query(data))
        return jsonify({"result": False})

    if __name__ == "__main__":
        try:
            app.run(host="0.0.0.0", port=10240)
        except KeyboardInterrupt:
            recognition.stop()