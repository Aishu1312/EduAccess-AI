from fastapi import APIRouter
from pydantic import BaseModel
from transformers import pipeline

router = APIRouter()

summarizer = pipeline("summarization")

class TextRequest(BaseModel):
    text: str

@router.post("/generate-notes")
def generate_notes(request: TextRequest):

    summary = summarizer(
        request.text,
        max_length=120,
        min_length=30,
        do_sample=False
    )

    return {
        "notes": summary[0]["summary_text"]
    }
