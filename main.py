from pathlib import Path

def ask_for_path(prompt: str) -> Path:
    # Checks if the folder name we are providing exist
    while True:
        folder_name = input(prompt).strip()
        path = Path(folder_name).expanduser()

        if not path.exists():
            print(f"This path {path} doesn't exist, try again.")


        if not path.is_dir():
            print(f"This path {path} is not a folder, try again.")


        return path
    

def unique_destination(dest_dir: Path, original_name: str) -> Path:
    file = dest_dir / original_name

    if not file.exists():
        return file
    
    file_name = file.stem
    file_format = file.suffix

    i = 1

    # If file_name have duplicates, keep name, but add a incrementor. 
    while True:
        file = dest_dir / f"{file_name}_{i}{file_format}"

        if not file.exists():
            return file
        
        i += 1

    
def flatten_folder(src: Path, dest: Path) -> None:
    dest = dest.resolve()
    src = src.resolve()

    files_moved = 0
    files_skipped = 0

    for file_path in src.rglob("*"):
        if not file_path.is_file():
            continue

        try:
            file_path.relative_to(dest)

            files_skipped += 1

            continue

        except ValueError:
            pass

        file_target = unique_destination(dest, file_path.name)

        file_path.rename(file_target)
        files_moved += 1

    print(f"Flatten Complete. Moved {files_moved} files. Skipped {files_skipped} files.")


def main():
    # Ask for file location
    src = ask_for_path("What folder are we flattening: ")

    # Ask for destination name
    dest_name = input("Name for the flattened folder (will be created inside the source): ").strip()

    # If nothing, then just name it flattened
    if not dest_name:
        dest_name = "flattened"

    # pathlib feature, joins src with name
    dest = (src / dest_name)

    # Makes a new parent folder if doesn't exist, if exist, then do nothing
    dest.mkdir(parents= True, exist_ok= True)

    # Our flatten folder function
    flatten_folder(src, dest)

    # Print destination
    print(f" Destination: {dest}")

if __name__ == "__main__":
    main()