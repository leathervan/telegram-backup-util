import os
import sys

def delete_files_by_name(directory: str, substring: str):
    if not os.path.isdir(directory):
        print("Указанная папка не существует.")
        return
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and substring in filename:
            try:
                os.remove(file_path)
                print(f"Удалено: {file_path}")
            except Exception as e:
                print(f"Ошибка при удалении {file_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python script.py <путь_к_папке> <строка>")
        sys.exit(1)

    delete_files_by_name(sys.argv[1], sys.argv[2])

    #python deleter.py <path> <str>
