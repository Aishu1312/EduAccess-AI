from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.speech_routes import router as speech_router
from routes.notes_routes import router as notes_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(speech_router)
app.include_router(notes_router)

@app.get("/")
def home():
    return {"message": "EduAccess AI Running Successfully"}
