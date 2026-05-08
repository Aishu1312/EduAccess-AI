from fastapi import FastAPI
from routes import speech_routes, gesture_routes, notes_routes

app = FastAPI()

app.include_router(speech_routes.router)
app.include_router(gesture_routes.router)
app.include_router(notes_routes.router)

@app.get("/")
def home():
    return {"message": "EduAccess AI Backend Running"}
