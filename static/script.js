document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("camera");
    const canvas = document.getElementById("canvas");
    const barcodeDisplay = document.getElementById("barcode");
    const productDisplay = document.getElementById("product-info");

    let barcodeDetected = false;  // Prevent multiple barcode detections

    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
    .then(stream => {
        video.srcObject = stream;
        video.play();
        startScanning(); // Start barcode scanning
    })
    .catch(err => console.error("Camera error:", err));

    function startScanning() {
        const context = canvas.getContext("2d");

        setInterval(() => {
            if (barcodeDetected) return; // Stop if barcode already detected

            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            Quagga.decodeSingle({
                decoder: { readers: ["ean_reader", "upc_reader"] },
                locate: true,
                src: canvas.toDataURL()
            }, function (result) {
                if (result && result.codeResult) {
                    let barcode = result.codeResult.code;
                    barcodeDisplay.textContent = barcode;
                    barcodeDetected = true; // Stop multiple detections

                    fetch('/get-product-info', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ barcode: barcode })
                    })
                    .then(response => response.json())
                    .then(data => {
                        productDisplay.textContent = data.product || "Product not found.";
                    })
                    .catch(error => {
                        console.error("Error fetching product info:", error);
                        productDisplay.textContent = "Error fetching product info.";
                    });
                }
            });
        }, 500); // Adjust scanning interval
    }
});
