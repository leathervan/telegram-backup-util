import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Утилита для сортировки медиа из Telegram экспорта")

    parser.add_argument("-path", required=True, help="Полный путь к папке експорта")
    
    # -remove | css files images js photos round_video_messages stickers video_files voice_messages | messages thumb
    parser.add_argument("-remove", nargs="*", help="Specifies the folder names to delete")

    # -remove | css files images js photos round_video_messages stickers video_files voice_messages
    parser.add_argument("-rename-by-name", nargs="*", help="Переименовать по имени")

    # -remove | css files images js photos round_video_messages stickers video_files voice_messages
    parser.add_argument("-rename-by-metadata", nargs="*", help="Переименовать по метадате")
    
    return parser.parse_args()
