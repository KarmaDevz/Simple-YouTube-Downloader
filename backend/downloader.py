import yt_dlp
import os


class Downloader:
    def __init__(self, download_dir="downloads", ffmpeg_path=None):
        self.download_dir = download_dir
        self.ffmpeg_path = ffmpeg_path

        os.makedirs(self.download_dir, exist_ok=True)

        if self.ffmpeg_path and not os.path.exists(self.ffmpeg_path):
            raise RuntimeError(f"FFmpeg no encontrado en: {self.ffmpeg_path}")

    def get_info(self, url):
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
        }

        if self.ffmpeg_path:
            ydl_opts["ffmpeg_location"] = self.ffmpeg_path

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            return {
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "formats": self._parse_formats(info),
            }

    def _parse_formats(self, info):
        formats = []
        seen = set()

        for f in info.get("formats", []):
            # Video muxed
            if f.get("vcodec") != "none" and f.get("acodec") != "none":
                res = f.get("resolution") or (
                    f"{f.get('height')}p" if f.get("height") else None
                )

                if res and res not in seen:
                    formats.append(
                        {
                            "type": "video",
                            "quality": res,
                            "format_id": f["format_id"],
                            "ext": f["ext"],
                        }
                    )
                    seen.add(res)

        formats.append(
            {
                "type": "audio",
                "quality": "Best Quality (MP3)",
                "format_id": "bestaudio/best",
                "ext": "mp3",
            }
        )

        formats.append(
            {
                "type": "video",
                "quality": "Best Quality (MP4)",
                "format_id": "bestvideo+bestaudio/best",
                "ext": "mp4",
            }
        )

        return formats

    def download(self, url, format_id, type="video"):
        ydl_opts = {
            "outtmpl": os.path.join(self.download_dir, "%(title)s.%(ext)s"),
            "quiet": False,
        }

        if self.ffmpeg_path:
            ydl_opts["ffmpeg_location"] = self.ffmpeg_path

        if type == "audio":
            ydl_opts.update(
                {
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                }
            )
        else:
            ydl_opts["format"] = format_id

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return True
