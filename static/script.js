document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("camera");
    const canvas = document.getElementById("canvas");
    const captureButton = document.getElementById("capture");
    const barcodeDisplay = document.getElementById("barcode");
    const productDisplay = document.getElementById("product-info");

    // Start the front camera
    navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user" }
    })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => console.error("Camera error:", err));

    captureButton.addEventListener("click", function () {
        // Draw the video frame to canvas
        const context = canvas.getContext("2d");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convert canvas to image data
        const imageData = context.getImageData(0, 0, canvas.width, canvas.height);

        // Use QuaggaJS to detect barcode
        Quagga.decodeSingle({
            decoder: { readers: ["ean_reader", "upc_reader"] },
            locate: true,
            src: canvas.toDataURL()
        }, function (result) {
            if (result && result.codeResult) {
                let barcode = result.codeResult.code;
                barcodeDisplay.textContent = barcode;

                // Send barcode to Flask backend
                fetch('/get-product-info', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ barcode: barcode })
                })
                .then(response => response.json())
                .then(data => {
                    productDisplay.textContent = data.product;
                })
                .catch(error => console.error("Error fetching product info:", error));
            } else {
                barcodeDisplay.textContent = "No barcode detected.";
            }
        });
    });
});
