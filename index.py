import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
from noisereduce import reduce_noise


# Initialiser le recognizer
recognizer = sr.Recognizer()

# Chemin vers le fichier audio MP3
mp3_file_path = "/home/lysa/sncf-ecole/Hackaton_SNCF/audio_test/son.mp3"

# Charger le fichier audio MP3
audio = AudioSegment.from_mp3(mp3_file_path)
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
from noisereduce import reduce_noise

# Initialiser le recognizer
recognizer = sr.Recognizer()

# Chemin vers le fichier audio MP3
mp3_file_path = "/home/lysa/sncf-ecole/Hackaton_SNCF/audio_test/son.mp3"

# Charger le fichier audio MP3
audio = AudioSegment.from_mp3(mp3_file_path)

# Réduire le bruit dans le fichier audio
noisy_part = audio.get_array_of_samples()
reduced_noise = reduce_noise(audio, noisy_part)

# Convertir le fichier audio MP3 réduit en WAV
wav_file_path = "/home/lysa/sncf-ecole/Hackaton_SNCF/audio_test/son_reduced.wav"
reduced_noise.export(wav_file_path, format="wav")

# Transcrire l'audio WAV en texte
with sr.AudioFile(wav_file_path) as source:
    # Lire le fichier audio WAV
    audio_data = recognizer.record(source)

    try:
        # Transcrire l'audio en texte
        text = recognizer.recognize_google(audio_data, language='fr-FR')
        print("Transcription : " + text)
    except sr.UnknownValueError:
        print("Impossible de comprendre l'audio")
    except sr.RequestError as e:
        print("Erreur lors de la demande au service de reconnaissance vocale : {0}".format(e))

# Convertir le fichier audio MP3 en WAV
wav_file_path = "/home/lysa/sncf-ecole/Hackaton_SNCF/audio_test/son.wav"
audio.export(wav_file_path, format="wav")

# Transcrire l'audio WAV en texte
with sr.AudioFile(wav_file_path) as source:
    # Lire le fichier audio WAV
    audio_data = recognizer.record(source)

    try:
        # Transcrire l'audio en texte
        text = recognizer.recognize_google(audio_data, language='fr-FR')
        print("Transcription : " + text)
    except sr.UnknownValueError:
        print("Impossible de comprendre l'audio")
    except sr.RequestError as e:
        print("Erreur lors de la demande au service de reconnaissance vocale : {0}".format(e))
