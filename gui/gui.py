import sys

from flask import Flask, render_template


app = Flask(__name__)
app.debug = True

@app.route("/")
def main():
    return render_template("main.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(sys.argv[1]), debug=True)