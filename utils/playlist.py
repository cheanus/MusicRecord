import os
import logging
import re
from typing import Optional
from utils import api


def check_playlist(playlist_name: str, playlist_id: str):
    playlist_dir = os.path.join("doc", "playlist")
    os.makedirs(playlist_dir, exist_ok=True)
    target_path = os.path.join(playlist_dir, f"{playlist_name}-{playlist_id}.md")

    if os.path.exists(target_path):
        return  # Do nothing if the exact file exists

    # Check for existing files with the same playlist_id but different name
    for filename in os.listdir(playlist_dir):
        if filename.endswith(f"-{playlist_id}.md") and not filename.startswith(
            f"{playlist_name}-"
        ):
            old_path = os.path.join(playlist_dir, filename)
            os.rename(old_path, target_path)
            logging.info(f"Renamed playlist file from {old_path} to {target_path}")
            return

    # If no matching file found, create new
    # Create a new file with playlist metadata. Use the api wrapper and handle failures.
    try:
        playlist_desc = api.get_playlist_info(playlist_id)["playlist"].get(
            "description", ""
        )
    except Exception as e:
        logging.warning(f"Failed to fetch playlist info for {playlist_id}: {e}")
        playlist_desc = ""

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(f"# {playlist_name}\n\n## 介绍\n\n{playlist_desc}\n\n## 播放列表\n")
    logging.info(f"Created playlist file: {target_path}")


def update_doc(playlist_name: str, playlist_id: str):
    # Generate playlist markdown content
    try:
        playlist_data = api.get_playlist_songs(playlist_id).get("songs", [])
    except Exception as e:
        logging.error(f"Failed to fetch songs for playlist {playlist_id}: {e}")
        return
    playlist_doc = ""
    for track in playlist_data:
        track_name = track["name"] + "-" + track["ar"][0].get("name", "Unknown")
        track_id = track["id"]
        # sanitize track_name for filesystem usage
        safe_name = _sanitize_filename(track_name)
        review_name = f"{safe_name}-{track_id}.md"
        review_path = os.path.join("doc", "review", review_name)
        if os.path.exists(review_path):
            playlist_doc += f"- [{track_name}](https://music.163.com/#/song?id={track_id}) 【[评论](../review/f{review_name})】\n"
        else:
            playlist_doc += f"- [{track_name}](https://music.163.com/#/song?id={track_id}) <!--【[评论](../review/f{review_name})】 -->\n"

    # Write to file
    playlist_dir = os.path.join("doc", "playlist")
    target_path = os.path.join(playlist_dir, f"{playlist_name}-{playlist_id}.md")
    # Read existing file and replace the 播放列表 section (keep content before it)
    with open(target_path, "r", encoding="utf-8") as f:
        content = f.read()

    marker = "## 播放列表"
    if marker in content:
        before, _sep, _after = content.partition(marker)
        new_content = before + marker + "\n\n" + playlist_doc
    else:
        # If marker missing, append it
        new_content = content + "\n\n" + marker + "\n\n" + playlist_doc

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    logging.info(f"Updated playlist document: {target_path}")


def _sanitize_filename(name: str, replace: str = "-") -> str:
    """Return a filesystem-safe filename by replacing unsafe characters.

    Keeps unicode characters but strips path separators and control characters.
    """
    # Remove path separators and control characters
    name = name.strip()
    # Replace any character that is not alphanumeric, space, dash, underscore, or unicode letters
    # Use a conservative regex: allow word chars and some punctuation, replace others
    name = re.sub(r"[\\/:*?\"<>|\r\n]+", replace, name)
    # Collapse multiple replacements
    name = re.sub(re.escape(replace) + r"+", replace, name)
    return name
