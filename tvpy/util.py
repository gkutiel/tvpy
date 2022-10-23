from itertools import chain
from pathlib import Path
from urllib.parse import urlparse, urlunparse


def load_key():
    with open('key.txt') as f:
        return f.read().strip()


def folders(root):
    return [x for x in Path(root).iterdir() if x.is_dir()]


def files(root, patterns=['*.mkv', '*.avi', '*.mp4', '*.srt']):
    root = Path(root)
    return chain(*[root.rglob(e) for e in patterns])


def files_media(root):
    return files(root, patterns=['*.mkv', '*.avi', '*.mp4'])


def files_subs(root):
    return files(root, patterns=['*.srt'])


def url_folder_name(file):
    url = urlparse(file)
    path = Path(url.path)
    folder = urlunparse(url._replace(path=str(path.parent)))
    name = str(path.name)
    assert f'{folder}/{name}' == file, f'{folder}/{name} != {file}'
    return folder, name
