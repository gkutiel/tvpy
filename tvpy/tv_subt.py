import requests
from rich.pretty import pprint

from tvpy.tv_info import load_tvpy


def get(imdb_id, season, episode):
    url = f'https://wizdom.xyz/api/releases/{imdb_id}'
    res = requests.get(url).json()
    subs = res['subs']
    return subs[f'{season}'][f'{episode}'][0]


def down_sub(sub_id, out_zip):
    url = f'https://wizdom.xyz/api/files/sub/{sub_id}'
    with open(out_zip, 'wb') as out:
        out.write(requests.get(url).content)


def tv_subt(folder):
    info = load_tvpy(folder)
    imdb_id = info['imdb_id']
    sub = get(imdb_id, 1, 7)
    pprint(sub)
    sub_version = sub['version']
    sub_id = sub['id']
    down_sub(sub_id, f'{sub_version}.zip')
