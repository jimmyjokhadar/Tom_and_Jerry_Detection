document.addEventListener("DOMContentLoaded", () => {
    const detectButton = document.getElementById("detectButton");
    const imageInput = document.getElementById("imageInput");
    const loadingSection = document.getElementById("loadingSection");
    const resultSection = document.getElementById("resultSection");
    const resultImage = document.getElementById("resultImage");
    const detectionList = document.getElementById("detectionList");

    detectButton.addEventListener("click", async () => {
        const file = imageInput.files[0];
        if (!file) {
            alert("Please select an image!");
            return;
        }

        // Show loading
        loadingSection.style.display = "block";
        resultSection.style.display = "none";

        const formData = new FormData();
        formData.append("image", file);

        try {
            const res = await fetch("/detect", {
                method: "POST",
                body: formData
            });
            const data = await res.json();

            // Hide loading
            loadingSection.style.display = "none";

            // Show result
            resultImage.src = "data:image/jpeg;base64," + data.image;
            detectionList.innerHTML = "";
            data.detections.forEach(det => {
                detectionList.innerHTML += `<li>${det.label} - ${det.score.toFixed(2)}</li>`;
            });
            resultSection.style.display = "block";

        } catch (err) {
            loadingSection.style.display = "none";
            alert("Error detecting objects. Check console.");
            console.error(err);
        }
    });
});
