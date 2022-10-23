import json
from pathlib import Path
from typing import List

from PTN import parse
from rich.panel import Panel
from rich.pretty import pprint

from tvpy.config import VERSION
from tvpy.console import cls
from tvpy.tv_json import tv_json
from tvpy.util import files_media


def existing_episodes(folder):
    res = [parse(f.name) for f in files_media(folder)]
    return {(e['season'], e['episode']) for e in res}


def all_episodes(seasons):
    return {
        (s['season_number'], i)
        for s in seasons
        for i in range(1, s['episode_count'] + 1)}


def last_episode_to_air(info):
    res = info['last_episode_to_air']
    return (res['season_number'], res['episode_number'])


def on_air_episodes(info):
    return {
        e for e in all_episodes(info['seasons'])
        if e <= last_episode_to_air(info)}


def tv_info(folder):
    try:
        info = load_tvpy(folder)
        assert info['version'] == VERSION
    except:
        print(f'[red]ERROR[/red]:.tvpy.json out of date. please run [green]tv-json[/green] {folder}')
        return

    pprint(on_air_episodes(info) - existing_episodes(folder))
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
