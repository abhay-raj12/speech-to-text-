
from flask import Flask, render_template, request, jsonify
import whisper
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load whisper model
model = whisper.load_model("base")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        if "audio" not in request.files:
            return jsonify({"error": "No audio file uploaded"})

        file = request.files["audio"]

        if file.filename == "":
            return jsonify({"error": "No file selected"})

        filepath = os.path.join(UPLOAD_FOLDER, "audio.wav")
        file.save(filepath)

        # Whisper transcription
        result = model.transcribe(filepath)

        text = result["text"]

        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=7860)

