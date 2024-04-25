import whisper as wh
import load_file


# Execute this script OR use the command line from the projet root folder
# pip install -r src/whisper/requirements.txt
# whisper assets/sounds/0087001479-DCT-20230810-081529-468ca229-718b-4244-b0bb-bfc60a365a77.mp3 --language French -o assets/results -f txt
#                   ^-- The audio file to transcribe                        The language of the audio --^              ^-- Output folder and type of output

if __name__ == '__main__':
    file = load_file.get_first_file()
    model = wh.load_model("small")
    result = model.transcribe(str(file))
    print(result["text"])
