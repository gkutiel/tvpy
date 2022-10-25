from itertools import chain
from pathlib import Path


def load_key():
    with open('key.txt') as f:
        return f.read().strip()


def folders(root):
    return [x for x in Path(root).iterdir() if x.is_dir()]


def tvpys(folder):
    return Path(folder).rglob('.tvpy.json')


def files(folder, patterns=['*.mkv', '*.avi', '*.mp4', '*.srt']):
    return chain(*[Path(folder).glob(e) for e in patterns])


def files_r(folder, patterns=['*.mkv', '*.avi', '*.mp4', '*.srt']):
    return chain(*[Path(folder).rglob(e) for e in patterns])


def files_media(root):
    return files(root, patterns=['*.mkv', '*.avi', '*.mp4'])


def files_subs(root):
    return files(root, patterns=['*.srt'])


def files_media_r(root):
    return files_r(root, patterns=['*.mkv', '*.avi', '*.mp4'])


def files_subs_r(root):
    return files_r(root, patterns=['*.srt'])
