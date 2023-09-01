// Initialize the port with a default value
let port = 8000;

// Update the port variable when the input value change
document.querySelector("#port").addEventListener("input", (event) => {
    port = parseInt(event.target.value);
});

// Add event listener for the Encode button
document.querySelector("#encode-button").addEventListener("click", () => {
    // Get selected image and song files
    const imageFile = document.querySelector("#input-image-encode").files[0];
    const songFile = document.querySelector("#input-song").files[0];

    const formData = new FormData();
    formData.append("image", imageFile);
    formData.append("song", songFile);

    // Check if bot files are selected
    if (imageFile && songFile) {
        fetch(`http://localhost:${port}/api/encode`, {
            method: "POST",
            body: formData,
        }).catch((err) => {
            console.error(err);
        });
    } else {
        // Check if imageFile is selected
        if (imageFile) {
            console.error("You have to select a song !");
        } else {
            console.error("You have to select an image !");
        }
    }
});

// Add event listener for the Decode button
document.querySelector("#decode-button").addEventListener("click", () => {
    // Get selected image and song files
    const imageFile = document.querySelector("#input-image-decode").files[0];

    const formData = new FormData();
    formData.append("image", imageFile);

    // Check if bot files are selected
    if (imageFile) {
        fetch(`http://localhost:${port}/api/decode`, {
            method: "POST",
            body: formData,
        }).catch((err) => {
            console.error(err);
        });
    } else {
        console.error("You have to select an image !");
    }
});
