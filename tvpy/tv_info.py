

from pathlib import Path

from rich.panel import Panel
from rich.table import Table

from tvpy.console import cls
from tvpy.tv_tmdb import load_tvpy
from tvpy.util import all_episodes, existing_episodes, last_episode_to_air


def tv_info(folder):
    try:
        info = load_tvpy(folder)

        episodes = all_episodes(info)
        ss, es = zip(*episodes)
        max_s = max(ss)
        max_e = max(es)
        mat = [[''] * max_e for _ in range(max_s)]

        last_e = last_episode_to_air(info)

        for s, e in episodes:
            mat[s-1][e-1] = '[err]x' if (s, e) <= last_e else ':hourglass:'

        existing = existing_episodes(folder)
        assert not (existing - set(episodes)), f'Unexpected episodes found existing - set(episodes)'
        for s, e in existing_episodes(folder):
            mat[s-1][e-1] = '[success]v'

        def info_line(name, content):
            return f'[bold]{name}:[/bold] {content}'
        info = Panel(
            expand=False,
            title=info["name"],
            renderable='\n'.join([
                info_line('Date', info['first_air_date']),
                info_line('Rating', f'{info["rating"]}'),
                info_line('Genres', f'{", ".join([g["name"] for g in info["genres"]])}'),
                info_line('Overview', info['overview'])
            ]))

        episode_table = Table(
            '',
            title=' [success]v[/success]: existing  [err]x[/err] missing  :hourglass: NA',
            title_style='gray',
            title_justify='left')

        for i in range(len(mat[0])):
            episode_table.add_column(f'{i+1}', justify='center')

        for i, row in enumerate(mat):
            episode_table.add_row(f'{i+1}', *row)

        cls.print(info, episode_table)

    except Exception as e:
        cls.print(f'[err]ERROR:[/err] {e}')
