import zipfile
from pathlib import Path

import requests
from PTN import parse
from rich.status import Status

from tvpy.console import cls
from tvpy.tv_json import load_tvpy
from tvpy.util import done, existing_episodes, files_subs


def list_available_subs(imdb_id, season, episode):
    url = f'https://wizdom.xyz/api/releases/{imdb_id}'
    res = requests.get(url).json()
    subs = res['subs']
    subs = subs[f'{season}'][f'{episode}']
    return subs


def select_sub(subs, encoder='NTB'):
    key = 'release_group'
    for sub in subs:
        if key in sub and sub[key] == encoder:
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
    info = load_tvpy(folder)
    imdb_id = info['imdb_id']
    for s, e in missing_subs:
        name = f'{info["name"]} S{s:02}E{e:02}'
        with Status(f'[info]Searching...', console=cls) as status:
            try:
                subs = list_available_subs(imdb_id, s, e)
                sub = select_sub(subs)
                sub_version = sub['version']
                sub_id = sub['id']

                status.update('[info]Downloading...')
                zip_file = Path(folder) / f'{sub_version}.zip'
                down_sub(sub_id, zip_file)

                status.update('[info]Extracting...')
                with zipfile.ZipFile(zip_file) as z:
                    z.extractall(folder)

                status.stop()
                cls.print(f':clapper: [success]{name}')
            except:
                status.stop()
                cls.print(f'[err]Error:[/err] Could not find subtitles for {name}')

    done()
