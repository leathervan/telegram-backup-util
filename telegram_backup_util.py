from utils.cli import parse_args
from utils.remover import remove
from utils.renamer import rename

def main():
    args = parse_args()
    
    remove(args.path, args.remove)
    rename(args.path, args.rename_by_name, args.rename_by_metadata)

if __name__ == "__main__":
    main()