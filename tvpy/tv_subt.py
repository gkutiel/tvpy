import zipfile
from pathlib import Path

import requests
from rich.pretty import pprint
from rich.status import Status

from tvpy.config import format
from tvpy.tv_info import load_tvpy


def get(imdb_id, season, episode):
    url = f'https://wizdom.xyz/api/releases/{imdb_id}'
    res = requests.get(url).json()
    subs = res['subs']
    subs = subs[f'{season}'][f'{episode}']
    return subs


def select_sub(subs):
    for sub in subs:
        if sub['release_group'] == format.encoder:
            return sub

    return subs[0]


def down_sub(sub_id, out_zip):
    url = f'https://wizdom.xyz/api/files/sub/{sub_id}'
    with open(out_zip, 'wb') as out:
        out.write(requests.get(url).content)


def tv_subt(folder):
    with Status('[red]Searching...') as status:
        info = load_tvpy(folder)
        imdb_id = info['imdb_id']
        subs = get(imdb_id, 1, 7)
        sub = select_sub(subs)
        sub_version = sub['version']
        sub_id = sub['id']

        status.update('[orange1]Downloading...')
        zip_file = Path(folder) / f'{sub_version}.zip'
        down_sub(sub_id, zip_file)

        status.update('[green]Extracting...')
        with zipfile.ZipFile(zip_file) as z:
            z.extractall()
