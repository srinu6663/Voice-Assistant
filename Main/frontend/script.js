let isListening = false;

function toggleListening() {
    const micButton = document.getElementById("mic-button");
    const waveContainer = document.getElementById("wave-container");
    const status = document.getElementById("status");

    // Play activation sound
    const audio = new Audio('https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3');
    audio.volume = 0.2;
    audio.play();

    isListening = true;

    // UI Effects
    micButton.style.boxShadow = "0 0 80px #9333ea";
    micButton.style.transform = "scale(1.2)";
    status.textContent = "Listening...";
    status.classList.add("listening");

    waveContainer.innerHTML = `
        <div class="wave"></div>
        <div class="wave"></div>
        <div class="wave"></div>
    `;

    // Call Python function via Eel
    eel.process_command()(function(response) {
        console.log("Received response:", response);
        updateResponse(response);  // Display response in UI
    });

    setTimeout(() => {
        isListening = false;
        micButton.style.boxShadow = "0 0 50px rgba(6, 182, 212, 0.8)";
        micButton.style.transform = "scale(1)";
        status.textContent = "Tap to speak";
        status.classList.remove("listening");
        waveContainer.innerHTML = "";
    }, 5000);
}

// Function to update UI with response
eel.expose(updateResponse);
function updateResponse(response) {
    document.getElementById("status").textContent = response;
}
