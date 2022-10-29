

from pathlib import Path

import climage
from rich.layout import Layout
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from tvpy.console import cls
from tvpy.tv_json import load_tvpy
from tvpy.util import all_episodes, existing_episodes, last_episode_to_air


def tv_info(folder):
    try:
        info = load_tvpy(folder)
        poster = Path(folder) / '.poster.jpg'

        episodes = all_episodes(info)
        ss, es = zip(*episodes)
        max_s = max(ss)
        max_e = max(es)
        mat = [[''] * max_e for _ in range(max_s)]

        last_e = last_episode_to_air(info)

        for s, e in episodes:
            mat[s-1][e-1] = '[err]x' if (s, e) <= last_e else ':hourglass:'

        for s, e in existing_episodes(folder):
            mat[s-1][e-1] = '[success]v'

        POSTER_WIDTH = 38
        poster = Text.from_ansi(climage.convert(
            poster,
            is_unicode=True,
            width=POSTER_WIDTH))

        info = Panel(
            title=info["name"],
            renderable='\n'.join([
                f'Rating: {info["rating"]}:star:',
                f'Genres: {", ".join([g["name"] for g in info["genres"]])}']))

        episode_table = Table(
            '',
            title='[success]v[/success]: existing  [err]x[/err] missing  :hourglass: NA',
            title_style='gray',
            title_justify='left')

        for i in range(len(mat[0])):
            episode_table.add_column(f'E{i+1:02}', justify='center')

        for i, row in enumerate(mat):
            episode_table.add_row(f'S{i+1:02}', *row)

        layout = Layout()
        layout.split_column(
            Layout(' ', size=2),
            Layout(name='content'))

        layout['content'].split_column(
            Layout(name='up'),
            Padding(episode_table, (0, 2)))

        layout['up'].split_row(
            Layout(
                Padding(poster, 1),
                name='up',
                size=POSTER_WIDTH + 2),
            Padding(info, 1))

        cls.print(layout)

    except Exception as e:
        print(e)
        cls.print('[red]ERROR')
