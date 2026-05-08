from transformers import pipeline

summarizer = pipeline("summarization")

def generate_notes(text):
    summary = summarizer(text, max_length=100, min_length=30)
    return summary[0]['summary_text']
