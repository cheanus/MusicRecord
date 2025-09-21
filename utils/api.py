import requests
from config import backend_host

# Default timeout (seconds) for HTTP requests
DEFAULT_REQUEST_TIMEOUT = 5


def _get_json(path: str, timeout: int | None = None) -> dict:
    """Helper to GET a URL and return parsed JSON with basic error handling."""
    url = f"{backend_host}{path}"
    try:
        response = requests.get(url, timeout=timeout or DEFAULT_REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Normalize exception type for callers; include URL for easier debugging
        raise RuntimeError(f"HTTP request failed for {url}: {e}") from e


def get_playlist_info(playlist_id: str) -> dict:
    return _get_json(f"/playlist/detail?id={playlist_id}")


def get_playlist_songs(playlist_id: str) -> dict:
    return _get_json(f"/playlist/track/all?id={playlist_id}")
