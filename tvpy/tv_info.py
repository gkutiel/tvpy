import json
from pathlib import Path
from typing import List

from PTN import parse
from rich.panel import Panel
from rich.pretty import pprint

from tvpy.config import VERSION
from tvpy.console import cls
from tvpy.tv_json import load_tvpy, tv_json
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


def missing_episodes(info, folder):
    return on_air_episodes(info) - existing_episodes(folder)


def tv_info(folder):
    try:
        info = load_tvpy(folder)

        cls.rule(f'[bold red]{info["name"]}[/bold red] :star: {info["rating"]}', style='green')
        cls.print('[bold orange1]Genres:', ', '.join([g['name'] for g in info["genres"]]))

        for season in info['seasons']:
            s = season['season_number']
            episode_count = season['episode_count']
            cls.print(f'[bold]Season {s}:[/bold] {episode_count} episodes')

        pprint(info['last_episode_to_air'])
    except:
        cls.print('[red]ERROR')
