import re
from itertools import chain
from pathlib import Path

from PTN import parse

from tvpy.console import cls


def file_size_in_mb(size: str):
    # e.g 1.8 GB, 222.8 MB
    size_mb, units = size.split(' ')
    assert units in {'GB', 'MB'}
    size_mb = float(size_mb)
    return size_mb if units == 'MB' else size_mb * 2**10


def load_key():
    return '7bfa2260d938bb3881e0dd89c47a6021'
    # with open('key.txt', 'r') as f:
    #     return f.read().strip()


def title2file_name(title, s, e):
    name = re.sub(r"[']", '', title)
    name = re.sub(r'[^a-zA-Z0-9]', ' ', name)
    name = re.sub(r' +', '.', name)

    return f'{name}.S{s:02}E{e:02}'


def title2folder_name(title):
    name = re.sub(r'[^a-zA-Z0-9]', ' ', title)
    name = re.sub(r' +', '.', name)

    return name


def name2title(name):
    return Path(name).name.replace('.', ' ').replace('_', ' ')


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


def existing_episodes(folder):
    res = [parse(f.name) for f in files_media(folder)]
    return {(e['season'], e['episode']) for e in res if 'season' in e}


def all_episodes(info):
    episodes = {
        (s['season_number'], i)
        for s in info['seasons']
        for i in range(1, s['episode_count'] + 1)}

    return sorted({(s, e) for s, e in episodes if s > 0})


def last_episode_to_air(info):
    res = info['last_episode_to_air']
    return (res['season_number'], res['episode_number'])


def on_air_episodes(info):
    return {
        e for e in all_episodes(info)
        if e <= last_episode_to_air(info)}


def missing_episodes(folder, tvpy, k):
    episodes = sorted(on_air_episodes(tvpy) - existing_episodes(folder))
    return episodes[:k]


def done():
    cls.print(f'[green]Done :+1:')
