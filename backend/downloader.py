import yt_dlp
import os

class Downloader:
    def __init__(self, download_dir="downloads"):
        self.download_dir = download_dir
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def get_info(self, url):
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration'),
                "formats": self._parse_formats(info)
            }

    def _parse_formats(self, info):
        formats = []
        # Filter for unique resolutions/qualities
        seen = set()
        for f in info.get('formats', []):
            # Video
            if f.get('vcodec') != 'none' and f.get('acodec') != 'none': # Muxed
                res = f.get('resolution') or f"{f.get('height')}p"
                if res and res not in seen:
                    formats.append({
                        "type": "video",
                        "quality": res,
                        "format_id": f['format_id'],
                        "ext": f['ext']
                    })
                    seen.add(res)
            # Audio only (best)
            elif f.get('vcodec') == 'none' and f.get('acodec') != 'none':
                 # We'll just offer "Best Audio" usually, but let's see if we can distinguish
                 pass
        
        # Add a generic "Best Audio" option
        formats.append({
            "type": "audio",
            "quality": "Best Quality (MP3)",
            "format_id": "bestaudio/best",
            "ext": "mp3"
        })
        
        # Add a generic "Best Video" option
        formats.append({
            "type": "video",
            "quality": "Best Quality (MP4)",
            "format_id": "bestvideo+bestaudio/best",
            "ext": "mp4"
        })

        return formats

    def download(self, url, format_id, type="video"):
        ydl_opts = {
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'quiet': False,
        }

        if type == "audio":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            # For video, we might need to merge if we pick specific streams, 
            # but for simplicity let's rely on format_id or best.
            # If format_id is complex, yt-dlp handles it.
            if format_id == "bestvideo+bestaudio/best":
                 ydl_opts['format'] = format_id
            else:
                # If specific format selected, we might need to merge audio if it's video-only
                # But to keep it simple and robust, let's just use 'bestvideo+bestaudio' 
                # and maybe limit height if we want specific quality.
                # For now, let's stick to the "Best" options for reliability 
                # unless we implement complex format selection logic.
                ydl_opts['format'] = format_id
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return True
