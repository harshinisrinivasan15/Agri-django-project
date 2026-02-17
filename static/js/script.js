// script.js
document.addEventListener("DOMContentLoaded", function () {

    const input = document.getElementById("imageInput");
    const preview = document.getElementById("previewImage");

    if (!input || !preview) {
        console.log("Elements not loaded yet");
        return;
    }

    input.addEventListener("change", function (event) {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = "block";
            };
            reader.readAsDataURL(file);
        }
    });
});
