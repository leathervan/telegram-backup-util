import os
import re
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
from pymediainfo import MediaInfo
from utils import constants

# Checks custom file name <yyyy>-<mm>-<dd>-_<hh>-<mm>-<ss>.<ext>
def is_valid_filename(filename):
    return bool(re.match(constants.CUSTOM_FILE_PATTERN, filename))

# Checks default telegram photo backup name: photo_<number>@<dd>-<mm>-<yyyy>_<hh>-<mm>-<ss>.<ext>
def is_telegram_filename(filename):
    return bool(re.match(constants.TELEGRAM_FILE_PATTERN, filename))

def get_custom_name_from_telegram_name(filename):
    match = re.match(constants.TELEGRAM_FILE_PATTERN, filename)
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

def get_custom_name_from_metadata(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    metadata_date = None
    if ext in constants.PHOTO_EXTENSIONS:  # If its a picture, gets metadata as from picture
        metadata_date = get_image_datetime(filepath)
    elif ext in constants.VIDEO_EXTENSIONS:  # If its a video, gets metadata as from video
        metadata_date = get_video_datetime(filepath)

    if metadata_date is None:
        return None

    new_filename = f"{metadata_date.strftime('%Y-%m-%d_%H-%M-%S')}{ext}"
    return new_filename

# Adds (1) if the file already exists
def safe_rename(old_filepath, new_filepath):
    base, ext = os.path.splitext(new_filepath)
    counter = 1
    new_safe_filepath = new_filepath
    while os.path.exists(new_safe_filepath):
        new_safe_filepath = f"{base} ({counter}){ext}"
        counter += 1

    os.rename(old_filepath, new_safe_filepath)
    return new_safe_filepath

def rename_files_in_folder(path, use_metadata):
    if not os.path.isdir(path):
        return
    
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath):
            ext = os.path.splitext(filename)[1].lower()
            print_folders = os.sep.join(filepath.split(os.sep)[-3:-1]) + os.sep

            if is_valid_filename(filename):
                print(f"[RENAME]\tAlready in the proper format: {print_folders}{filename}")
                continue
            
            new_filename = None
            if use_metadata:
                new_filename = get_custom_name_from_metadata(filepath)
                if new_filename is None:
                    print(f"[RENAME]\tNo metadata found: {print_folders}{filename}")
                    continue
            else:
                if is_telegram_filename(filename):
                    new_filename = get_custom_name_from_telegram_name(filepath)
                else: 
                    print(f"[RENAME]\tThe file name format is not suitable for renaming by name: {print_folders}{filename}")
                    continue
            
            new_filepath = os.path.join(path, new_filename)
            new_filepath = safe_rename(filepath, new_filepath)
            print(f"[RENAME]\tRenamed: {print_folders}{os.path.basename(filepath)} → {print_folders}{os.path.basename(new_filepath)}")

def rename(path, args_by_name, args_by_metadata):
    if args_by_name is None and args_by_metadata is None:# If args is None, skip rename() at all
        return

    if args_by_name == []:  # If args_by_name == [], considers it like flag "all" and deletes recommended folders and files
        for folder in constants.ARG_FOLDERS_RECOMMENDED_TO_RENAME_BY_NAME:
            folder_path = os.path.join(path, folder)
            rename_files_in_folder(folder_path, False)

    if args_by_name: # If args_by_name is not empty, checks args in predefined and delete as folder or file
        for arg in args_by_name:
            if arg in constants.ARG_POSSIBLE_FOLDERS:
                folder_path = os.path.join(path, arg)
                rename_files_in_folder(folder_path, False)
            else: print(f"[RENAME]\tArgument {arg} is not recognized")
    
    if args_by_metadata == []:  # If args_by_name == [], considers it like flag "all" and deletes recommended folders and files
        for folder in constants.ARG_FOLDERS_RECOMMENDED_TO_RENAME_BY_METADATA:
            folder_path = os.path.join(path, folder)
            rename_files_in_folder(folder_path, True)

    if args_by_metadata: # If args_by_name is not empty, checks args in predefined and delete as folder or file
        for arg in args_by_metadata:
            if arg in constants.ARG_POSSIBLE_FOLDERS:
                folder_path = os.path.join(path, arg)
                rename_files_in_folder(folder_path, True)
            else: print(f"[RENAME]\tArgument {arg} is not recognized")


    