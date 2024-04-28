const button = document.getElementById("record-button");
const legend = document.getElementById("legend");
const audioNode = document.getElementById("audio-node");
function activate_button() {
    // Stop recording
    if (button.classList.contains("activated")) {
        button.classList.remove("activated");
        legend.innerHTML = "Votre message audio est en cours de traitement <i class='text-primary fa-solid fa-spinner fa-spin'></i>";
        button.classList.add("disabled");
        stopRecording();
    }
    // Start recording
    else {
        button.classList.add("activated");
        legend.textContent = "L'enregistrement est lancé...";
        startRecording();
    }
}

let recorder = null; // Variable pour stocker l'objet MediaRecorder

function startRecording() {
    if (recorder && recorder.state === "recording") {
        recorder.stop();
    }

    // Réinitialise les chunks audio
    let audioChunks = [];

    // Démarre l'enregistrement
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            recorder = new MediaRecorder(stream);
            recorder.ondataavailable = e => {
                audioChunks.push(e.data);
            };
            recorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                const audioElement = document.getElementById('audio-sample');
                audioElement.src = audioUrl;
                audioNode.load();
                audioNode.classList.remove("visually-hidden");
                transcribe(audioBlob);
            };
            recorder.start();
        })
        .catch(err => console.error('Error recording:', err));

}
function stopRecording() {
    if (recorder && recorder.state === "recording") {
        recorder.stop(); // Arrêter l'enregistrement
    }
}

const FrText = document.getElementById("fr-text");
const AnText = document.getElementById("an-text");
const EsText = document.getElementById("es-text");

async function transcribe(blob){
    let data = new FormData();
    data.append('file', blob);
    fetch('http://127.0.0.1:5000/transcribe', {
        method: 'POST',
        body: data
    }).then(response => response.json()).then(json => {
        if (json.success === true) {
            FrText.value = json["transcribed_fr"];
            AnText.value = json["transcribed_en"];
            EsText.value = json["transcribed_es"];
        }
        legend.textContent = "Cliquez pour enregistrer l'annonce vocale !"
        button.classList.remove("disabled");
    });

}
