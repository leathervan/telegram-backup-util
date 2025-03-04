import os
import re
import sys
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
from pymediainfo import MediaInfo

PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic", ".gif", ".bmp", ".tiff"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv"}
TELEGRAM_PHOTO_PATTERN = r"photo_\d+@(\d{2})-(\d{2})-(\d{4})_(\d{2})-(\d{2})-(\d{2})\.[a-zA-Z0-9]+$"
CUSTOM_FILE_PATTERN = r"^(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})( \(\d+\))?\.[a-zA-Z0-9]+$"

# Checks custom file name <yyyy>-<mm>-<dd>-_<hh>-<mm>-<ss>.<ext>
def is_valid_filename(filename):
    return bool(re.match(CUSTOM_FILE_PATTERN, filename))

# Checks default telegram photo backup name: photo_<number>@<dd>-<mm>-<yyyy>_<hh>-<mm>-<ss>.<ext>
def is_telegram_photoname(filename):
    return bool(re.match(TELEGRAM_PHOTO_PATTERN, filename))

# Gets custom file name from telegram photo backup name
def get_valid_name_from_telegram_name(filename):
    match = re.match(TELEGRAM_PHOTO_PATTERN, filename)
    day = match.group(1)
    month = match.group(2)
    year = match.group(3)
    hour = match.group(4)
    minute = match.group(5)
    second = match.group(6)

    new_filename = f"{year}-{month}-{day}_{hour}-{minute}-{second}{os.path.splitext(filename)[1]}"
    return new_filename

# Gets metatada date
def get_image_datetime(filepath):
    try:
        image = Image.open(filepath)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                if TAGS.get(tag) == "DateTimeOriginal":
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
        return None
    except Exception as e:
        print(f"Ошибка при обработке изображения {filepath}: {e}")
        return None

# Gets metatada date
def get_video_datetime(filepath):
    try:
        media_info = MediaInfo.parse(filepath)
        for track in media_info.tracks:
            if track.track_type == "General":
                creation_time = track.encoded_date  # Некоторые видео не имеют creation_time, использую encoded_date
                if creation_time:
                    return datetime.strptime(creation_time, "%Y-%m-%d %H:%M:%S UTC")

        return None
    except Exception as e:
        print(f"Ошибка при обработке видео {filepath}: {e}")
        return None

# Adds (1) if the file already exists
def safe_rename(old_filepath, new_filepath):
    base, ext = os.path.splitext(new_filepath)
    counter = 1
    new_safe_filepath = new_filepath
    while os.path.exists(new_safe_filepath):
        new_safe_filepath = f"{base} ({counter}){ext}"
        counter += 1

    os.rename(old_filepath, new_safe_filepath)
    print(f"{os.path.basename(old_filepath)} → {os.path.basename(new_safe_filepath)}")

    return new_safe_filepath


def rename_media(folder):
    counter = 0
    for filename in os.listdir(folder):
        counter += 1
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath):
            ext = os.path.splitext(filename)[1].lower()

            if is_valid_filename(filename):
                print(f"{filename}: Уже в правильном формате")
                continue

            # Renames if its telegram name pattern
            if is_telegram_photoname(filename):
                new_filename = get_valid_name_from_telegram_name(filename)
                new_filepath = os.path.join(folder, new_filename)
                safe_rename(filepath, new_filepath)
                continue

            metadata_date = None
            if ext in PHOTO_EXTENSIONS:  # If its a picture, gets metadata as from picture
                metadata_date = get_image_datetime(filepath)
            elif ext in VIDEO_EXTENSIONS:  # If its a video, gets metadata as from video
                metadata_date = get_video_datetime(filepath)

            if metadata_date is None:
                print(f"{filename}: Ошибка, метаданные не найдены.")
                continue

            # Form name from metadata date
            new_filename = f"{metadata_date.strftime('%Y-%m-%d_%H-%M-%S')}{ext}"
            new_filepath = os.path.join(folder, new_filename)
            safe_rename(filepath, new_filepath)
    print(f"Proccessed files: {counter}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Ошибка: Укажите путь к папке в качестве параметра.")
        sys.exit(1)

    folder = sys.argv[1]
    rename_media(folder)
