import json

from flask import Flask, jsonify, request

import numpy as np
from flask.ext.cors import CORS, cross_origin
from helpers.path_for import full_path_for
from mpi.mpi_digit_recognition import MPIDigitRecognition


recognition = MPIDigitRecognition(full_path_for("conf.json"))
recognition.run()

if recognition.is_main_node():
    app = Flask(__name__)
    cors = CORS(app)
    app.config["CORS_HEADERS"] = "Content-Type"

    def log(filename, data):
        with open(filename, "w") as file:
            file.write(json.dumps(data))

    def crop(array, pad=0, ratio=False):
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
                    if top_left["x"] >= x:
                        top_left["x"] = x
                    if top_left["y"] >= y:
                        top_left["y"] = y
                    if bottom_right["x"] <= x:
                        bottom_right["x"] = x
                    if bottom_right["y"] <= y:
                        bottom_right["y"] = y

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

        if ratio:
            if new_width > new_height:
                diff = new_width - new_height
                if diff % 2 != 0:
                    result.append([0] * new_width)

                for x in range(diff / 2):
                    result.insert(0, [0] * new_width)
                    result.append([0] * new_width)

            elif new_height > new_width:
                diff = new_height - new_width
                for row in result:
                    for x in range(diff / 2):
                        row.insert(0, 0)
                        row.append(0)
                    if diff % 2 != 0:
                        row.append(0)
            else:
                pass
        return result

    def scale_to(array, width, height):
        from PIL import Image

        w, h = len(array[0]), len(array)
        image_data = np.zeros((h,w,3), dtype=np.uint8)
        for y, row in enumerate(array):
            for x, cell in enumerate(row):
                if cell > 0:
                    image_data[y][x] = [255, 255, 255]

        im = Image.fromarray(image_data, "RGB")
        im.thumbnail((width, height), Image.ANTIALIAS)
        data = list(im.getdata())

        result = []
        row = []
        i = 0
        for element in data:
            if element[0] > 0 or element[1] > 0 or element[2] > 0:
                row.append(1)
            else:
                row.append(0)
            i += 1
            if i == width:
                i = 0
                result.append(row)
                row = []

        return result

    def power_up_train_array(array, factor):
        result = []
        for row in array:
            new_row = []
            for cell in row:
                new_row.append(cell * factor)
            result.append(new_row)
        return result

    def process_input_matrix(data):
        settings = recognition._config["neurons"]["class"]["settings"]
        sizes = recognition._config["neurons"]["class"]["size"]

        data = crop(data, settings["crop_pad"], True)
        data = scale_to(data, float(sizes[0]), float(sizes[1]))

        return data


    @app.route("/train", methods=["POST"])
    @cross_origin()
    def train():
        data = request.json
        character = request.json["character"]
        data = request.json["data"]
        if data:
            settings = recognition._config["neurons"]["class"]["settings"]

            data = process_input_matrix(data)
            data = power_up_train_array(data, settings["train_factor"])

            recognition.train(character, data)
            return jsonify({"result": True})
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
            app.run(host="0.0.0.0", port=10240)
        except KeyboardInterrupt:
            recognition.stop()