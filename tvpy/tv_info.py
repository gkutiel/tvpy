
from rich.pretty import pprint

from tvpy.console import cls
from tvpy.tv_json import load_tvpy


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
