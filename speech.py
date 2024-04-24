import os
import speech_recognition as sr

# Fonction pour lire et transcrire les fichiers audio
def transcribe_audio_files(audio_folder):
    transcripts = {}
    recognizer = sr.Recognizer()
    audio_files = os.listdir(audio_folder)
    
    for audio_file in audio_files:
        if audio_file.endswith(".wav"):
            audio_file_path = os.path.join(audio_folder, audio_file)
            with sr.AudioFile(audio_file_path) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language='fr-FR')
                    transcripts[audio_file] = text
                except sr.UnknownValueError:
                    transcripts[audio_file] = "Impossible de comprendre l'audio"
                except sr.RequestError as e:
                    transcripts[audio_file] = "Erreur lors de la demande au service de reconnaissance vocale : {0}".format(e)
    
    return transcripts

# Fonction pour construire et entraîner un modèle NLP (exemple)
#def train_nlp_model(data):
    # Code pour entraîner un modèle NLP sur les données textuelles
    #pass

# Exemple d'utilisation
audio_folder = "/home/lysa/sncf-ecole/Hackaton_SNCF/audio_test"
transcripts = transcribe_audio_files(audio_folder)
#train_nlp_model(transcripts)

