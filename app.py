from flask import Flask, render_template, request, jsonify
from libs import test

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/transcribe', methods=['POST'])
def transcribe():
    files = request.files
    file = files.get('file')
    file_path = f"audio/{file.filename}.wav"
    file.save(dst=file_path)

    transcript_fr, transcript_en, transcript_es = test(file_path)

    return jsonify({
        "success": True,
        "transcribed_fr": transcript_fr,
        "transcribed_en": transcript_en,
        "transcribed_es": transcript_es
    })


if __name__ == '__main__':
    app.run(debug=True)
