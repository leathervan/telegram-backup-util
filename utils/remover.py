import os
import sys
import shutil
import re
from utils import constants

def delete_by_path(path):
    print_folders = os.sep.join(path.split(os.sep)[-3:])
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
            print(f"[REMOVE]\tFolder successfully deleted: {print_folders}")
        elif os.path.isfile(path):
            os.remove(path)
            print(f"[REMOVE]\tFile successfully deleted: {print_folders}")
        else:
            print(f"[REMOVE]\tCannot delete, the path does not exist or is not a folder/file: {print_folders}")
    except Exception as e:
        print(f"[REMOVE]\tError deleting {print_folders}: {e}")


def delete_files_in_folder_by_pattern(path, pattern):
    compiled_pattern = re.compile(pattern)

    for file in os.listdir(path):
        if compiled_pattern.fullmatch(file):
            file_path = os.path.join(path, file)
            delete_by_path(file_path)

def delete_files_recursively(path, pattern):
    compiled_pattern = re.compile(pattern)

    for root, _, files in os.walk(path):
        for file in files:
            if compiled_pattern.fullmatch(file):
                file_path = os.path.join(root, file)
                delete_by_path(file_path)



def remove(path, args):
    if args is None: # If args is None, skip remove() at all
        return

    if args == []:  # If args == [], considers it like flag "all" and deletes recommended folders and files
        for folder in constants.ARG_FOLDERS_RECOMMENDED_TO_DELETE:
            folder_path = os.path.join(path, folder)
            if os.path.isdir(folder_path):
                delete_by_path(folder_path)
        
        delete_files_in_folder_by_pattern(path, constants.MESSAGES_PATTERN)
        delete_files_recursively(path, constants.THUMB_PATTERN)

        return

    if args: # If args is not empty, checks args in predefined and delete as folder or file
        for arg in args:
            if arg in constants.ARG_POSSIBLE_FOLDERS:
                delete_path = os.path.join(path, arg)
                delete_by_path(delete_path)
            
            elif arg == constants.ARG_MESSAGES_TO_DELETE:
                delete_files_in_folder_by_pattern(path, constants.MESSAGES_PATTERN)

            elif arg == constants.ARG_THUMB_TO_DELETE:
                delete_files_recursively(path, constants.THUMB_PATTERN)
            
            else: print(f"[REMOVE]\t-remove argument {arg} is not recognized")

        return
