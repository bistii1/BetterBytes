// Initialize QuaggaJS
function startScanner() {
    Quagga.init({
      inputStream: {
        name: "Live",
        type: "LiveStream",
        target: document.querySelector('#scanner-container'),    // Target container for the webcam
        constraints: {
          facingMode: "environment" // Use the rear-facing camera
        }
      },
      decoder: {
        readers: ["code_128_reader", "ean_reader", "ean_8_reader", "upc_reader", "upc_e_reader"]
      }
    }, function(error) {
      if (error) {
        console.error(error);
        return;
      }
      Quagga.start();
    });
  
    // Listen for barcode detections
    Quagga.onDetected(function(result) {
      const barcode = result.codeResult.code;
      document.getElementById('barcode').textContent = barcode;
      fetchFoodInfo(barcode); // Fetch food info from USDA API
    });
  }
  
  // Function to fetch product info from the USDA API
  async function fetchFoodInfo(barcode) {
    const apiKey = 'Y3juRrBZaGXrVnDp9k0UERXRMtYAuY3rKGgWA1nE';  // Replace with your USDA API key
    const url = `https://api.nal.usda.gov/fdc/v1/foods/search?query=${barcode}&apiKey=${apiKey}`;
  
    try {
      const response = await fetch(url);
      const data = await response.json();
      if (data.foods && data.foods.length > 0) {
        const food = data.foods[0];
        const foodInfo = `Name: ${food.description}, Brand: ${food.brandOwner}, FDC ID: ${food.fdcId}`;
        document.getElementById('product-info').textContent = foodInfo;
      } else {
        document.getElementById('product-info').textContent = 'No information found for this barcode.';
      }
    } catch (error) {
      console.error('Error fetching food information:', error);
      document.getElementById('product-info').textContent = 'Error fetching food information.';
    }
  }
  
  // Start scanner on page load
  window.onload = function() {
    startScanner();
  };
  