import logging
from config import track_playlist_ids
from utils import playlist


def update_all_playlists():
    logging.info("Starting to update all playlists...")
    for playlist_id in track_playlist_ids:
        try:
            playlist_name = playlist.api.get_playlist_info(playlist_id)["playlist"]["name"]
        except Exception as e:
            logging.error(f"Failed to fetch playlist info for {playlist_id}: {e}")
            # Skip this playlist but continue with others
            continue

        try:
            playlist.check_playlist(playlist_name, playlist_id)
            playlist.update_doc(playlist_name, playlist_id)
        except Exception as e:
            logging.error(f"Failed to update playlist {playlist_name} ({playlist_id}): {e}")
            continue
    logging.info("All playlists updated.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    update_all_playlists()
