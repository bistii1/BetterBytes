document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("camera");
    const canvas = document.getElementById("canvas");
    const barcodeDisplay = document.getElementById("barcode");
    const productDisplay = document.getElementById("product-info");
    const gptDisplay = document.getElementById("gpt-info");  // Add a new element for GPT info

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
                        // Display product name
                        productDisplay.textContent = data.product || "Product not found.";

                        // Process and display GPT-4 response if available
                        if (data.gpt_info) {
                            let text_info = data.gpt_info;

                            // Processing text for formatting
                            text_info = text_info
                                .replace(/^\s*"(.*?)"\s*$/, "$1") // Remove leading and trailing quotes
                                .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // Convert **bold** to <strong>
                                .replace(/\\n/g, "<br>") // Convert \n to <br> for line breaks
                                .replace(/\\u2019/g, "'") // Fix the unicode for apostrophe
                                .replace(/\"(.*?)\"/g, "&quot;$1&quot;") // Replace escaped quotes for better display
                                .replace(/- /g, "<li>")  // Convert bullet points to <li> for list formatting
                                .replace(/<\/li>/g, "</li><br>") // Add line breaks between list items
                                .replace(/<\/li><br><br>/g, "</li>"); // Clean extra breaks

                            gptDisplay.innerHTML = text_info;
                        } else {
                            // Fallback message if no GPT info is provided
                            gptDisplay.textContent = "No additional information available.";
                        }
                    })
                    .catch(error => {
                        console.error("Error fetching product info:", error);
                        productDisplay.textContent = "Error fetching product info.";
                        gptDisplay.textContent = "Error retrieving information.";
                    });
                }
            });
        }, 500); // Adjust scanning interval
    }
});
