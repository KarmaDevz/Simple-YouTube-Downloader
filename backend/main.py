from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import os
from downloader import Downloader
import sys
import os
from updater import Updater

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


app = FastAPI()

# Setup paths
FFMPEG_PATH = resource_path(os.path.join("ffmpeg", "ffmpeg.exe"))
FRONTEND_DIR = resource_path("frontend")
DOWNLOADS_DIR = resource_path("downloads")

# Version and Updater
CURRENT_VERSION = "v0.0.1"
updater = Updater("KarmaDevz", "Simple-YouTube-Downloader")

# Initialize downloader
downloader = Downloader(download_dir=DOWNLOADS_DIR)

class DownloadRequest(BaseModel):
    url: str
    format_id: str
    type: str

@app.get("/api/info")
async def get_video_info(url: str):
    try:
        info = downloader.get_info(url)
        return info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/download")
async def download_video(request: DownloadRequest):
    try:
        success = downloader.download(request.url, request.format_id, request.type)
        if success:
            return {"status": "success", "message": "Download started/completed"}
        else:
            raise HTTPException(status_code=500, detail="Download failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/check-update")
async def check_update():
    return updater.check_for_updates(CURRENT_VERSION)

@app.post("/api/update")
async def perform_update(request: Request):
    try:
        data = await request.json()
        download_url = data.get("download_url")
        if not download_url:
             raise HTTPException(status_code=400, detail="Missing download_url")
        
        # This will block until download finishes, then exit.
        # Ideally we might want to do this in a background task, 
        # but since we are exiting, blocking is acceptable or we use BackgroundTasks.
        # However, since we want to report error if it fails before download completes,
        # keeping it synchronous (or awaited async) until execution is fine for this MVP.
        updater.download_and_install_update(download_url)
        return {"status": "success", "message": "Update started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files (Frontend)
# We mount this LAST so API routes take precedence
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
