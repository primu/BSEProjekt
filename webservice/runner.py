import os
from flask import Flask, jsonify, request
from conf import PROJECT_ROOT
from mpi.mpi_digit_recognition import MPIDigitRecognition

recognition = MPIDigitRecognition(os.path.join(PROJECT_ROOT, "conf.json"))
recognition.run()

if recognition.is_main_node():
    app = Flask(__name__)

    @app.route("/train", methods=["POST"])
    def train():
        return jsonify({"result": True})

    @app.route("/query", methods=["POST"])
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