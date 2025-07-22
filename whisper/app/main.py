# In whisper/app/main.py
from fastapi import FastAPI, UploadFile, File
import whisper
import os

app = FastAPI()
model = whisper.load_model("base")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # Save the uploaded file to the shared volume
    file_path = f"/shared/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Transcribe the audio file
    result = model.transcribe(file_path)

    # Clean up the saved file
    # os.remove(file_path)

    return {"transcription": result["text"]}