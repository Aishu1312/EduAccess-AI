from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

summarizer = None

def get_summarizer():
    global summarizer
    if summarizer is None:
        from transformers import pipeline
        summarizer = pipeline("summarization")
    return summarizer

class TextRequest(BaseModel):
    text: str

@router.post("/generate-notes")
def generate_notes(request: TextRequest):

    sum_pipeline = get_summarizer()
    summary = sum_pipeline(
        request.text,
        max_length=120,
        min_length=30,
        do_sample=False
    )

    return {
        "notes": summary[0]["summary_text"]
    }

