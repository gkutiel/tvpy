import json
from pathlib import Path

from PTN import parse
from rich.panel import Panel
from rich.pretty import pprint

from tvpy.config import VERSION
from tvpy.console import cls
from tvpy.tv_json import tv_json
from tvpy.util import files_media


def load_tvpy(folder):
    folder = Path(folder)
    tvpy_json = folder / '.tvpy.json'
    with open(tvpy_json, 'r') as f:
        return json.load(f)


def get_existing_episodes(folder, season: int, num_episodes: int):
    existing = [False] * num_episodes
    for f in files_media(folder):
        info = parse(f.name)
        s, e = info['season'], info['episode']
        if s == season:
            existing[e - 1] = True

    return existing


def tv_info(folder):
    try:
        info = load_tvpy(folder)
        assert info['version'] == VERSION
    except:
        print(f'[red]ERROR[/red]:.tvpy.json out of date. please run [green]tv-json[/green] {folder}')
        return

    # genres = ', '.join([g['name'] for g in info["genres"]])

    # cls.rule(f'{info["name"]} {info["rating"]}')
    # cls.print(f'{"Genres:":<12} {genres}', style='warn')

    # cls.print(Panel("Hello, [red]World!"))

    # for season in info['seasons']:
    #     s = season['season_number']
    #     episode_count = season['episode_count']
    #     bar = [f'{i:<3}' for i in range(1, episode_count + 1)]
    #     existing = get_existing_episodes(folder, s, episode_count)
    #     status = [
    #         '[green]V[/green]' if (s, i) in local_info else '[red]X[/red]'
    #         for i in range(1, episode_count + 1)]

    #     print(season['name'])
    #     print(''.join(bar))
    #     print('  '.join(status))
    #     print()

    pprint(info.keys())
