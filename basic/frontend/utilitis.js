// QR Code
const qrCode = document.getElementById('qrcode');
function generateQRCode(id) {
    qrCode.innerHTML = "";

    // Display QR code div
    qrCode.style.display = 'block';

    new QRCode(qrCode, {
        text: id
    });
}


document.getElementById("search-member-btn").addEventListener("click", function () {
    const inputField = document.getElementById("search-member");

    // Get the ID from the input field
    const memberId = inputField.value.trim();
    if (memberId) {
        generateQRCode(memberId);
    }
});





export default function nextPage(page) {
    window.location.href = page
}