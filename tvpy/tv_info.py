import json
from pathlib import Path
from pprint import pprint

from PTN import parse
from rich import print

from tvpy.config import VERSION
from tvpy.util import files_media


def get_local_info(folder):
    return {
        (e['season'], e['episode']): e
        for e in [
            parse(f.name)
            for f in files_media(folder)]}


def tv_info(folder):
    folder = Path(folder)
    tvpy_json = folder / '.tvpy.json'

    with open(tvpy_json, 'r') as f:
        info = json.load(f)
    try:
        assert info['version'] == VERSION
    except:
        print(f'[red]ERROR[/red]:.tvpy.json out of date. please run [green]tv-json[/green] {folder}')
        return

    title = info['name'] + ' ' + str(info['rating'])
    genres = ', '.join([g['name'] for g in info["genres"]])

    print()
    print(title)
    print('-' * len(title))
    print(f'{"Genres:":<12} {genres}')
    print()

    local_info = get_local_info(folder)
    for season in info['seasons']:
        s = season['season_number']
        episode_count = season['episode_count']
        bar = [f'{i:<3}' for i in range(1, episode_count + 1)]
        status = [
            '[green]V[/green]' if (s, i) in local_info else '[red]X[/red]'
            for i in range(1, episode_count + 1)]

        print(season['name'])
        print(''.join(bar))
        print('  '.join(status))
        print()

    print()

    pprint(info.keys())
