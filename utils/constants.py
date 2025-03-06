ARG_POSSIBLE_FOLDERS = {"css", "files", "images", "js", "photos", "round_video_messages", "stickers", "video_files", "voice_messages"}

ARG_FOLDERS_RECOMMENDED_TO_RENAME_BY_NAME = {"photos", "video_files"}
ARG_FOLDERS_RECOMMENDED_TO_RENAME_BY_METADATA = {"files", "round_video_messages", "video_files"}

ARG_FOLDERS_RECOMMENDED_TO_DELETE = {"css", "images", "js", "stickers", "voice_messages"}
ARG_MESSAGES_TO_DELETE = "messages"
ARG_THUMB_TO_DELETE = "thumb"

MESSAGES_PATTERN = r"messages\d*\.html"
THUMB_PATTERN = r".+_thumb( \(\d+\))?\.[a-zA-Z0-9]+$"

PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic", ".gif", ".bmp", ".tiff"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv"}

# anything_@dd-mm-yyyy_hh-mm-ss(1).anything
TELEGRAM_FILE_PATTERN = r".+_\d+@(\d{2})-(\d{2})-(\d{4})_(\d{2})-(\d{2})-(\d{2})\s*(\(\s*\d+\s*\))?\s*\..*"

# yyyy-mm-dd_hh-mm-ss(1).ext
CUSTOM_FILE_PATTERN = r"^(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})( \(\d+\))?\.[a-zA-Z0-9]+$"
