from flask import Flask, render_template, Response, jsonify
import cv2
from pyzbar.pyzbar import decode

app = Flask(__name__)
camera = cv2.VideoCapture(0)  # Open webcam

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Convert to grayscale for better barcode detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect barcodes
        barcodes = decode(gray)
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            x, y, w, h = barcode.rect

            # Draw rectangle around the barcode
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display scanned barcode data
            text = f"{barcode_data} ({barcode_type})"
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Encode frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/scan_barcode')
def scan_barcode():
    """Return last detected barcode."""
    success, frame = camera.read()
    if not success:
        return jsonify({"error": "Camera error"})

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray)
    if barcodes:
        barcode_data = barcodes[0].data.decode("utf-8")
        return jsonify({"barcode": barcode_data})
    
    return jsonify({"barcode": None})

if __name__ == '__main__':
    app.run(debug=True)
