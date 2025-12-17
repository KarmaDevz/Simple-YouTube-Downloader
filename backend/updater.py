import requests
import os
import sys
import subprocess
import tempfile

class Updater:
    def __init__(self, repo_owner, repo_name):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    def check_for_updates(self, current_version):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            latest_release = response.json()
            latest_version = latest_release.get("tag_name")
            
            # Find the exe asset
            assets = latest_release.get("assets", [])
            download_url = None
            for asset in assets:
                if asset["name"].endswith(".exe"):
                    download_url = asset["browser_download_url"]
                    break
            
            # Fallback to html_url if no exe found (though we expect an exe)
            if not download_url:
                download_url = latest_release.get("html_url")

            # Simple string comparison
            if latest_version and latest_version != current_version:
                return {
                    "update_available": True,
                    "latest_version": latest_version,
                    "download_url": download_url,
                    "is_exe": download_url.endswith(".exe") if download_url else False
                }
            else:
                 return {
                    "update_available": False,
                    "latest_version": latest_version,
                     "download_url": None,
                     "is_exe": False
                }
        except Exception as e:
            return {"error": str(e)}

    def download_and_install_update(self, download_url):
        try:
            # Download to a temporary file
            print(f"Descargando actualización de {download_url}...")
            response = requests.get(download_url, stream=True)
            response.raise_for_status()

            # Create a temporary file for the installer/executable
            # We preserve the extension .exe
            fd, temp_path = tempfile.mkstemp(suffix=".exe")
            os.close(fd)

            with open(temp_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Actualización descargada en {temp_path}")
            
            # Execute the new file
            # In a real installer scenario, this installer would replace the old exe.
            # If it's just the app exe, we might need a separate launcher or argument to swap.
            # For this request, "executing the exe" is the requirement.
            subprocess.Popen([temp_path])
            
            # Exit the current process to allow replacement if handled by the new process
            # or simply to close the old version.
            sys.exit(0)
            
        except Exception as e:
            print(f"Error al actualizar: {e}")
            raise e
