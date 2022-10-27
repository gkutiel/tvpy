import zipfile
from pathlib import Path

import requests
from PTN import parse
from rich.status import Status

from tvpy.tv_json import load_tvpy
from tvpy.util import existing_episodes, files_subs


def list_available_subs(imdb_id, season, episode):
    url = f'https://wizdom.xyz/api/releases/{imdb_id}'
    res = requests.get(url).json()
    subs = res['subs']
    subs = subs[f'{season}'][f'{episode}']
    return subs


def select_sub(subs, encoder='NTB'):
    for sub in subs:
        if sub['release_group'] == encoder:
            return sub

    return subs[0]


def down_sub(sub_id, out_zip):
    url = f'https://wizdom.xyz/api/files/sub/{sub_id}'
    with open(out_zip, 'wb') as out:
        out.write(requests.get(url).content)


def existing_subs(folder):
    res = [parse(f.name) for f in files_subs(folder)]
    return {(e['season'], e['episode']) for e in res}


def tv_subs(folder):
    missing_subs = existing_episodes(folder) - existing_subs(folder)
    for s, e in missing_subs:
        with Status(f'[info]Searching for subtitles S{s:02}E{e:02}') as status:
            info = load_tvpy(folder)
            imdb_id = info['imdb_id']
            subs = list_available_subs(imdb_id, s, e)
            sub = select_sub(subs)
            sub_version = sub['version']
            sub_id = sub['id']

            status.update('[info]Downloading subtitles')
            zip_file = Path(folder) / f'{sub_version}.zip'
            down_sub(sub_id, zip_file)

            status.update('[info]Extracting subtitles')
            with zipfile.ZipFile(zip_file) as z:
                z.extractall(folder)
