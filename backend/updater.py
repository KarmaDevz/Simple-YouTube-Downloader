import requests

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
            
            # Simple string comparison for now. Ideally use semver.
            # Assuming tags are like "v1.0.0"
            if latest_version and latest_version != current_version:
                return {
                    "update_available": True,
                    "latest_version": latest_version,
                    "download_url": latest_release.get("html_url")
                }
            else:
                 return {
                    "update_available": False,
                    "latest_version": latest_version,
                     "download_url": None
                }
        except Exception as e:
            return {"error": str(e)}
