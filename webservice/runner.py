from flask import Flask, jsonify, request

from flask.ext.cors import CORS, cross_origin
from helpers.path_for import full_path_for
from mpi.mpi_digit_recognition import MPIDigitRecognition


recognition = MPIDigitRecognition(full_path_for("conf.json"))
print(recognition._rank)
recognition.run()

if recognition.is_main_node():
	app = Flask(__name__)
	cors = CORS(app)
	app.config["CORS_HEADERS"] = "Content-Type"

	def scale_to(array, width, height):
		width = float(width)
		height = float(height)
		originalX = float(len(array))
		originalY = float(len(array[0]))

		scaleX = width / originalX
		scaleY = width / originalY

		out = [[0.0 for _ in range(int(height))] for _ in range(int(width))]

		for x, column in enumerate(array):
			for y, cell in enumerate(column):
				newX = int(x * scaleX)
				newY = int(y * scaleY)
				if out[newX][newY] == 0.0:
					out[newX][newY] = 1.0 if cell > 0 else 0.0

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
			sizes = recognition._config["neurons"]["class"]["size"]
			#todo(Pawel): jako parametr
			data = scale_to(data, float(sizes[0]), float(sizes[1]))
			return jsonify(recognition.query(data))
		return jsonify({"result": False})

	if __name__ == "__main__":
		try:
			app.run(host="0.0.0.0", port=10240)
		except KeyboardInterrupt:
			recognition.stop()