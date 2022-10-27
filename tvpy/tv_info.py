

from rich.panel import Panel
from rich.table import Table

from tvpy.console import cls
from tvpy.tv_json import load_tvpy
from tvpy.util import all_episodes, existing_episodes, last_episode_to_air


def tv_info(folder):
    try:
        info = load_tvpy(folder)

        panel = Panel(
            title=info["name"],
            renderable='\n'.join([
                f'Rating: {info["rating"]} :star:',
                f'Genres: {", ".join([g["name"] for g in info["genres"]])}']))

        cls.print()
        cls.print(panel)

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

        episode_table = Table('')
        for i in range(len(mat[0])):
            episode_table.add_column(f'E{i+1:02}', justify='center')

        for i, row in enumerate(mat):
            episode_table.add_row(f'S{i+1:02}', *row)

        cls.print()
        cls.print(' [success]v[/success]: existing  [err]x[/err] missing  :hourglass: NA')
        cls.print(episode_table)

    except:
        cls.print('[red]ERROR')
