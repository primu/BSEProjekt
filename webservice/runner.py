import json

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

    def crop(array, pad=0):
        top_left = {
            "x": 99999,
            "y": 99999
        }

        bottom_right = {
            "x": -1,
            "y": -1
        }

        for y, row in enumerate(array):
            for x, cell in enumerate(row):
                if cell > 0:
                    if top_left["x"] >= x and top_left["y"] >= y:
                        top_left["x"], top_left["y"] = x, y
                    if bottom_right["x"] <= x and bottom_right["y"] <= y:
                        bottom_right["x"], bottom_right["y"] = x, y

        new_width = bottom_right["x"] - top_left["x"] + 2 * pad
        new_height = bottom_right["y"] - top_left["y"] + 2* pad

        result = []

        for x in range(pad):
            result.append([0] * new_width)

        for y, row in enumerate(array):
            if not (top_left["y"] <= y <= bottom_right["y"]):
                continue
            new_row = []
            for x in range(pad):
                new_row.append(0)
            for x, cell in enumerate(row):
                if top_left["x"] <= x <= bottom_right["x"]:
                    new_row.append(cell)
            for x in range(pad):
                new_row.append(0)
            if new_width % 2 != 0:
                new_row.append(0)
            result.append(new_row)

        for x in range(pad):
            result.append([0] * new_width)

        if new_height % 2 != 0:
            result.append([0] * new_width)
        return result

    def scale_to(array, width, height):
        width = float(width)
        height = float(height)
        originalX = float(len(array))
        originalY = float(len(array[0]))

        scaleX = width / originalX
        scaleY = height / originalY

        out = [[0.0 for _ in range(int(height))] for _ in range(int(width))]

        for y, row in enumerate(array):
            for x, cell in enumerate(row):
                newX = int(x * scaleX)
                newY = int(y * scaleY)
                try:
                    if out[newX][newY] == 0.0:
                        out[newX][newY] = 1.0 if cell > 0 else 0.0
                except Exception as e:
                    pass

        return out


    @app.route("/train", methods=["POST"])
    @cross_origin()
    def train():
        return jsonify({"result": True})

    @app.route("/query", methods=["POST"])
    @cross_origin()
    def query():
        data = request.json
        if data:
            with open("log", "w") as file:
                file.write(json.dumps(data))
            sizes = recognition._config["neurons"]["class"]["size"]
            # todo(Pawel): jako parametr
            try:
                data = crop(data)
            except Exception as e:
                print(str(e))
            data = scale_to(data, float(sizes[0]), float(sizes[1]))
            return jsonify(recognition.query(data))
        return jsonify({"result": False})

    if __name__ == "__main__":
        try:
            app.run(host="0.0.0.0", port=10240)
        except KeyboardInterrupt:
            recognition.stop()