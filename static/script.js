document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("camera");
    const canvas = document.getElementById("canvas");
    const barcodeDisplay = document.getElementById("barcode");
    const productDisplay = document.getElementById("product-info");
    const gptDisplay = document.getElementById("gpt-info");  // Add a new element for GPT info

    let barcodeDetected = false;  // Flag to stop multiple barcode detections

    // Start the front camera
    navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user" }
    })
    .then(stream => {
        video.srcObject = stream;
        video.play();
        // Start scanning as soon as the camera is active
        startScanning();
    })
    .catch(err => console.error("Camera error:", err));

    function startScanning() {
        const context = canvas.getContext("2d");

        const scanInterval = setInterval(() => {
            if (barcodeDetected) {
                clearInterval(scanInterval);  // Stop scanning after detecting the first barcode
                return;
            }

            // Draw the video frame to canvas
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            // Use QuaggaJS to detect barcode
            Quagga.decodeSingle({
                decoder: { readers: ["ean_reader", "upc_reader"] },
                locate: true,
                src: canvas.toDataURL()
            }, function (result) {
                if (result && result.codeResult) {
                    let barcode = result.codeResult.code;
                    barcodeDisplay.textContent = barcode;
                    barcodeDetected = true;  // Set flag to prevent further detections

                    // Send barcode to Flask backend
                    fetch('/get-product-info', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ barcode: barcode })
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Display product name
                        productDisplay.textContent = data.product || "Product not found.";

                        // Display GPT-4 response if available
                        gptDisplay.textContent = data.gpt_info || "No detailed info available from GPT.";
                    })
                    .catch(error => {
                        console.error("Error fetching product info:", error);
                        productDisplay.textContent = "Error fetching product info.";
                    });
                }
            });
        }, 100); // Check every 100ms for a barcode
    }
});
