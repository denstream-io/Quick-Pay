
function domReady(fn) {
    if (
        document.readyState === "complete" ||
        document.readyState === "interactive"
    ) {
        setTimeout(fn, 1000);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

domReady(function () {

    function onScanSuccess(decodedText, decodeResult) {
        alert("You Qr is : " + decodedText, decodeResult);

         // Send scanned data to backend
        try {

            decodedText = decodedText.split('/');
            item_id = Number(decodedText[0]);

            // Redirect to form page with query parameters
            window.location.href = `/qr_cart/${item_id}`;
        } catch (error) {
            alert('Invalid QR code format!');
            console.error(error);
        }
    }

    let htmlscanner = new Html5QrcodeScanner(
        "my-qr-reader",
        { fps: 10, qrbos: 250 }
    );
    htmlscanner.render(onScanSuccess);
});