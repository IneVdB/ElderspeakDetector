"""This file contains the main code for the website"""


import ssl

from flask import Flask, render_template, url_for, request, jsonify

from modules.request_processing import process_audio

app = Flask(__name__)
app.config["UPLOAD_EXTENSIONS"] = [".wav", ".mp3"]


@app.route("/", methods=["GET"])
def index():
    """router for the index page"""
    return render_template("index.html")


@app.route("/picture_old_woman", methods=["GET"])
def picture_old_woman():
    """router for page elderspeak"""
    url = url_for("static", filename="img/rusthuis.jpg")
    return url


@app.route("/upload", methods=["GET"])
def upload():
    """router for page upload"""
    return render_template("upload.html")


@app.route("/receive_audio", methods=["POST"])  # type: ignore
def recieve_audio():
    """Receive the audio data from the client and return the results"""
    response_data = process_audio(request)
    response = jsonify(response_data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    print(response_data)
    return response


if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("ssl/localhost.com+5.pem", "ssl/localhost.com+5-key.pem")
    app.run(
        debug=False,
        port=5001,
        ssl_context=context,
    )
