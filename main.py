import os
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

def process_folder(folder_path):
    file_extensions = defaultdict(list)

    for root, _, files in os.walk(folder_path):
        for file in files:
            _, ext = os.path.splitext(file)
            file_extensions[ext].append(os.path.join(root, file))

    
    with open("Sorted files.txt", "w") as f:
        for ext, files in file_extensions.items():
            f.write(f"Extension{ext}:\n")
            for file in files:
                f.write(f"- {os.path.basename(file)}: {file}\n")


def main():
    folder_path = "D:\\IT\\Repositories\\Python-WEB-homeworks"

    with ThreadPoolExecutor() as executor:
        executor.submit(process_folder, folder_path)

if __name__ == "__main__":
    main()
