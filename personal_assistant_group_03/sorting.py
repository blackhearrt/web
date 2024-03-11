import shutil
import re
from pathlib import Path


class FileScanner:
    def __init__(self):
        self.images = list()
        self.documents = list()
        self.audio = list()
        self.video = list()
        self.folders = list()
        self.archives = list()
        self.others = list()
        self.unknown = set()
        self.extensions = set()

        self.registered_extensions = {
            "JPEG": self.images,
            "PNG": self.images,
            "JPG": self.images,
            "DOC": self.documents,
            "DJVU": self.documents,
            "PDF": self.documents,
            "TXT": self.documents,
            "DOCX": self.documents,
            "PPTX": self.documents,
            "XLSX": self.documents,
            "ZIP": self.archives,
            "OGG": self.audio,
            "WAV": self.audio,
            "MP3": self.audio,
            "AVI": self.video,
            "MOV": self.video,
            "MP4": self.video
        }

    def get_extensions(self, file_name):
        return Path(file_name).suffix[1:].upper()

    def scan(self, folder):
        for item in folder.iterdir():
            if item.is_dir():
                if item.name not in ("JPEG", "JPG", "PNG", "TXT", "DOCX", "DOC",
                                     "PDF", "PPTX", "XLSX", "OTHER", "ZIP", "MP3",
                                     "MP4", "AVI", "MOV", "OGG", "WAV"):
                    self.folders.append(item)
                    self.scan(item)
                continue

            extension = self.get_extensions(file_name=item.name)
            new_name = folder / item.name
            if not extension:
                self.others.append(new_name)
            else:
                try:
                    container = self.registered_extensions[extension]
                    self.extensions.add(extension)
                    container.append(new_name)
                except KeyError:
                    self.unknown.add(extension)
                    self.others.append(new_name)


class FileNormalizer:
    def __init__(self):
        self.UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
        self.TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i",
                           "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                           "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

        self.TRANS = {}

        for key, value in zip(self.UKRAINIAN_SYMBOLS, self.TRANSLATION):
            self.TRANS[ord(key)] = value
            self.TRANS[ord(key.upper())] = value.upper()

    def normalize(self, name):
        name, *extension = name.split('.')
        new_name = name.translate(self.TRANS)
        new_name = re.sub(r'\W', "_", new_name)
        return f"{new_name}.{'.'.join(extension)}"


IGNORED_FILES = ["sorting.py", "scan.py", "normalize.py", "files_generator.py", "main.py", "Notebook.py", "Address_book.py", "auto_save.bin"]


class FileSorter:
    def __init__(self, folder_path):
        self.folder_path = Path(folder_path)
        self.file_scanner = FileScanner()
        self.file_normalizer = FileNormalizer()
        self.file_scanner.scan(self.folder_path)

    def handle_file(self, path, dist):
        target_folder = self.folder_path / dist
        target_folder.mkdir(exist_ok=True)
        if path.name not in IGNORED_FILES:
            path.replace(target_folder / self.file_normalizer.normalize(path.name))

    def handle_archive(self, path, dist):
        target_folder = self.folder_path / dist
        target_folder.mkdir(exist_ok=True)

        new_name = self.file_normalizer.normalize(path.name.replace(".zip", ''))

        archive_folder = target_folder / new_name
        archive_folder.mkdir(exist_ok=True)
        path.rename(archive_folder / path.name)

        try:
            shutil.unpack_archive(str(path.resolve()), archive_folder)
        except shutil.ReadError:
            return
        except FileNotFoundError as e:
            archive_folder.rmdir()
            return
        path.unlink()

    def remove_empty_folders(self, path):
        for item in path.iterdir():
            if item.is_dir():
                self.remove_empty_folders(item)
                try:
                    item.rmdir()
                except OSError:
                    pass

    def get_folder_objects(self):
        for folder in self.folder_path.iterdir():
            if folder.is_dir():
                self.remove_empty_folders(folder)
                try:
                    folder.rmdir()
                except OSError:
                    pass

    def sort_files(self):
        for file in self.file_scanner.images:
            self.handle_file(file, "Images")

        for file in self.file_scanner.audio:
            self.handle_file(file, "Audio")

        for file in self.file_scanner.video:
            self.handle_file(file, "Videos")

        for file in self.file_scanner.documents:
            self.handle_file(file, "Documents")

        for file in self.file_scanner.others:
            self.handle_file(file, "Others")

        for file in self.file_scanner.archives:
            self.handle_archive(file, "Archive")

        self.get_folder_objects()

