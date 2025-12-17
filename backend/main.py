from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import os
from downloader import Downloader

app = FastAPI()

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "../downloads")
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")

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
