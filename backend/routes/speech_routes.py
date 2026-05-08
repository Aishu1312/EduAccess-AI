from fastapi import APIRouter, UploadFile, File
import whisper
import os

router = APIRouter()

model = whisper.load_model("base")

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):

    temp_file = f"temp_{file.filename}"

    with open(temp_file, "wb") as f:
        f.write(await file.read())

    result = model.transcribe(temp_file)

    os.remove(temp_file)

    return {
        "transcription": result["text"]
    }
