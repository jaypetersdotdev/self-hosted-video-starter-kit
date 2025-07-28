# In whisper/app/main.py
from fastapi import FastAPI, UploadFile, File, Query, Body
from typing import Optional
import whisper
import os
import subprocess

app = FastAPI()
model = whisper.load_model("base")

@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    transcriptType: str = Query("segment", enum=["segment", "word"]),
    returnTimestamps: bool = Query(False)
):
    # Save the uploaded file to the shared volume
    file_path = f"/shared/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Transcribe the audio file
    if transcriptType == "word":
        result = model.transcribe(file_path, word_timestamps=True)
    else:
        result = model.transcribe(file_path)

    # Clean up the saved file
    # os.remove(file_path)

    response = {}

    if transcriptType == "segment":
        response["transcription"] = " ".join([seg["text"] for seg in result["segments"]])
        if returnTimestamps:
            response["timestamps"] = [
                {"start": seg["start"], "end": seg["end"], "text": seg["text"]}
                for seg in result["segments"]
            ]
    elif transcriptType == "word":
        # word-level timestamps are in the 'words' key of each segment if available
        words = []
        for seg in result["segments"]:
            if "words" in seg:
                for word in seg["words"]:
                    words.append({
                        "word": word["word"],
                        "start": word["start"],
                        "end": word["end"]
                    })
            else:
                # fallback: treat the whole segment as one word
                words.append({
                    "word": seg["text"],
                    "start": seg["start"],
                    "end": seg["end"]
                })
        response["transcription"] = " ".join([w["word"] for w in words])
        if returnTimestamps:
            response["timestamps"] = words
    else:
        response["transcription"] = result["text"]

    return response

@app.post("/ffmpeg")
async def run_ffmpeg(command: str = Body(..., embed=True)):
    # SECURITY WARNING: This endpoint allows arbitrary ffmpeg command execution.
    # Only allow commands that start with 'ffmpeg ' to prevent arbitrary code execution.
    if not command.strip().startswith("ffmpeg "):
        return {"error": "Only ffmpeg commands are allowed."}
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        return {"error": str(e)}