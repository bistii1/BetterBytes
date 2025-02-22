// Access the webcam and display it on the page
const video = document.getElementById('video');
const scanButton = document.getElementById('scanButton');
const productInfoDiv = document.getElementById('product-info');

// Set up webcam capture
navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((err) => {
        console.error("Error accessing webcam:", err);
    });

// Capture the image from the webcam and send it to the backend
scanButton.addEventListener('click', () => {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Get the image data as base64
    const imageData = canvas.toDataURL('image/jpeg');

    // Send the image data to the Flask backend
    fetch('/scan_barcode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.product_info) {
            productInfoDiv.innerHTML = `<h2>Product Info:</h2><p>${JSON.stringify(data.product_info)}</p>`;
        } else {
            productInfoDiv.innerHTML = `<h2>Error:</h2><p>${data.error}</p>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        productInfoDiv.innerHTML = `<h2>Error:</h2><p>Failed to scan barcode.</p>`;
    });
});
