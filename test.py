import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)

# Initialize the camera
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Error: Camera not found or failed to open.")
    exit()

def gen_frames():
    while True:
        # Grab the webcam's image
        ret, frame = cam.read()
        if not ret:
            break

        # Resize the raw image into (224-height, 224-width) pixels
        frame = cv2.resize(frame, (650, 500), interpolation=cv2.INTER_AREA)

        # Convert the frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            break

        # Convert to byte array to send over HTTP
        frame = buffer.tobytes()

        # Yield the frame as an HTTP response (MIME type is JPEG image)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    # Render the webpage that will display the webcam stream
    return render_template('index.html')

@app.route('/video')
def video():
    # Stream the webcam feed to the webpage
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
