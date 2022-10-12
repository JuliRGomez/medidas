from flask import Flask
from flask import render_template
from flask import Response
app = Flask(__name__)

from models.hands_live_trigger import image_proccesing
# import cv2
# cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/video_feed")
def video_feed():
    return Response(image_proccesing(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")
if __name__ == "__main__":
    app.run(debug=True)
# cap.release()