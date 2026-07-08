from fastapi import APIRouter, UploadFile, File
import os

router = APIRouter()

model = None

def get_whisper_model():
    global model
    if model is None:
        import whisper
        model = whisper.load_model("base")
    return model

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):

    temp_file = f"temp_{file.filename}"

    with open(temp_file, "wb") as f:
        f.write(await file.read())

    ws_model = get_whisper_model()
    result = ws_model.transcribe(temp_file)

    os.remove(temp_file)

    return {
        "transcription": result["text"]
    }

