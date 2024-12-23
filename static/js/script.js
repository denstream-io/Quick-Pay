// Utility function to execute a callback function when the DOM is fully loaded.
function domReady(fn) {
    if (
        document.readyState === "complete" ||  // The DOM is fully loaded.
        document.readyState === "interactive" // The DOM is almost ready (subresources like images may still be loading).
    ) {
        // Execute the callback function after a slight delay to ensure readiness.
        setTimeout(fn, 1000);
    } else {
        // Attach an event listener to execute the callback once the DOMContentLoaded event fires.
        document.addEventListener("DOMContentLoaded", fn);
    }
}

// Execute the main logic when the DOM is ready.
domReady(function () {

    /**
     * Callback function triggered when a QR code is successfully scanned.
     * @param {string} decodedText - The text content extracted from the scanned QR code.
     * @param {object} decodeResult - Additional data about the decoded result (if needed).
     */
    function onScanSuccess(decodedText, decodeResult) {
         // Send scanned data to backend
        try {
            // Split the decoded text to extract relevant data (e.g., item ID).
            decodedText = decodedText.split('/');
            item_id = Number(decodedText[0]); // Convert the extracted item ID to a number.

            // Redirect the user to a backend route with the scanned item ID.
            window.location.href = `/qr_cart/${item_id}`;
        } catch (error) {
            // Handle errors, such as invalid QR code formats, gracefully.
            alert('Invalid QR code format!');
            console.error(error); // Log the error for debugging purposes.
        }
    }

    // Initialize the HTML5 QR Code Scanner with configuration options.
    let htmlscanner = new Html5QrcodeScanner(
        "my-qr-reader", // The HTML element ID where the scanner will render.
        { fps: 10, qrbos: 250 } // Configuration: frames per second and QR code box size.
    );

    // Render the scanner and set the callback function to handle successful scans.
    htmlscanner.render(onScanSuccess);
});