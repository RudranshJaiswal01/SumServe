from dotenv import load_dotenv 
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.summarize import router as summarize_router

app = FastAPI(title="SumServe - Document Summarization Service")

app.include_router(summarize_router, prefix="/api")

# ---------- Home Page ----------
FRONTEND_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")
app.mount("/", StaticFiles(directory=FRONTEND_PATH, html=True), name="frontend")