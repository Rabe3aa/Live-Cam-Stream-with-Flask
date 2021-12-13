from os import scandir
from flask import Flask, request, render_template, redirect, url_for, Response
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture()

def frame_generator():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        


@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/video_process')
def video_process():
    return Response(frame_generator(), mimetype='multipart/x-mixed-replace; boundary = frame')



if __name__=='__main__':
    app.run(debug=True)