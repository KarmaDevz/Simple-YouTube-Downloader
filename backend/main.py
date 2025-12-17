from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import os
from downloader import Downloader
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


app = FastAPI()

# Setup paths
FRONTEND_DIR = resource_path("frontend")
DOWNLOADS_DIR = resource_path("downloads")


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

# Mount static files (Frontend)
# We mount this LAST so API routes take precedence
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
