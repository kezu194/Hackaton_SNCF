import whisper as wh
import load_file


# Execute this script OR use the command line from the projet root folder
# pip install -r src/whisper/requirements.txt
# whisper assets/sounds/0087001479-DCT-20230810-081529-468ca229-718b-4244-b0bb-bfc60a365a77.mp3 --language French -o assets/results -f txt
#                   ^-- The audio file to transcribe                        The language of the audio --^              ^-- Output folder and type of output

if __name__ == '__main__':
    file = load_file.get_first_file()

    model = wh.load_model("small")

    # load audio and pad/trim it to fit 30 seconds
    audio = wh.load_audio(str(file))
    audio = wh.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = wh.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    test, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = wh.DecodingOptions()
    result = wh.decode(model, mel, options)

    # print the recognized text
    print(result.text)
