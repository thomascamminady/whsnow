import os
import os.path

from wahoosnowmaker.namespace import Namespace


def notes_file(folder: str, name: str = Namespace.notes_file_name) -> str:
    return os.path.join(folder, name)


def save_notes(folder: str, text: str) -> None:
    with open(notes_file(folder), "w+") as f:
        f.write(text)


def load_notes(folder: str) -> str:
    if not os.path.exists(notes_file(folder)):
        return ""

    with open(notes_file(folder)) as f:
        return f.read()


def name_file(folder: str, name: str = Namespace.name_file_name) -> str:
    return os.path.join(folder, name)


def save_name(folder: str, text: str) -> None:
    with open(name_file(folder), "w+") as f:
        f.write(text)


def load_name(folder: str) -> str:
    if not os.path.exists(name_file(folder)):
        return folder

    with open(name_file(folder)) as f:
        content = f.read()
        if content.strip() == "":
            return folder
        else:
            return content
