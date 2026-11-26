import sys
from pathlib import Path

# تأمين المسار عشان يشتغل سواء شغّلت بـ uv run أو python main.py أو uvicorn
ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import gradio as gr
import uvicorn
from fastapi import FastAPI

from crew_project.api.routes import router as api_router
from crew_project.ui.app import demo

api = FastAPI(title="Procurement Crew", version="1.0.0")
api.include_router(api_router)

app = gr.mount_gradio_app(api, demo, path="/")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7860)