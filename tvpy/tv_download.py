from pathlib import Path
from time import sleep
from typing import List, Tuple

import libtorrent as lt
import rich.status
from py1337x import py1337x
from rich.progress import (BarColumn, Progress, TaskID, TaskProgressColumn,
                           TextColumn, TimeRemainingColumn)

from tvpy.config import default, load_config
from tvpy.console import cls
from tvpy.lt import Handler
from tvpy.tv_tmdb import load_tvpy
from tvpy.util import (done, file_size_in_mb, missing_episodes, name2title,
                       title2file_name)


def q(folder, season: int, episode: int):
    query = name2title(Path(folder).name)

    return f'{query} S{season:02}E{episode:02}'


def down(magnets, down_folder, raise_ki):
    s = lt.session()
    try:
        with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                TimeRemainingColumn(),
                TextColumn('[dim cyan]Size: {task.fields[size]}MB'),
                TextColumn('[green]Down: {task.fields[down]}kB/s'),
                TextColumn('[blue]Up: {task.fields[up]}kB/s'),
                TextColumn('[orange1]Peers: {task.fields[peers]}')) as progress:

            tasks: List[Tuple[Handler, TaskID]] = []
            for name, link in magnets:
                params = lt.parse_magnet_uri(link)
                params.save_path = str(down_folder)

                h = s.add_torrent(params)
                task = progress.add_task(f'[green]{name}', total=1, size='', down='', up='', peers='')
                tasks.append((h, task))

            while not progress.finished:
                for h, task in tasks:
                    status = h.status()
                    progress.update(
                        task,
                        completed=status.progress,
                        size=f'{status.total_done / 1048576:.1f}',
                        down=f'{status.download_rate / 1000:.1f}',
                        up=f'{status.upload_rate / 1000:.1f}',
                        peers=status.num_peers)

                sleep(1)
    except KeyboardInterrupt:
        if raise_ki:
            raise KeyboardInterrupt()


def tv_download(folder, k=10, raise_ki=False):
    tvpy = load_tvpy(folder)
    torrents = py1337x()

    magnets = []
    with rich.status.Status('', console=cls) as status:
        for s, e in missing_episodes(folder, tvpy, k=k):
            name = title2file_name(tvpy['name'], s, e)
            magnet = Path(folder) / f'{name}.magnet'
            if magnet.exists():
                with open(magnet, 'r') as f:
                    magnet_link = f.read()
            else:
                query = q(folder, s, e)
                status.update(f'[info]Searching for {query}')
                res = torrents.search(query)
                items = res['items']

                if not items:
                    cls.print(f'[warn]Could not find torrent for {query}')
                    continue

                for item in items:
                    mb = file_size_in_mb(item['size'])
                    item['seed_per_mb'] = int(item['seeders']) / mb

                items = sorted(
                    items,
                    key=lambda item: item['seed_per_mb'],
                    reverse=True)

                link = items[0]['link']
                info = torrents.info(link)

                magnet_link = info['magnetLink']
                with open(magnet, 'w') as f:
                    f.write(magnet_link)

            magnets.append((name, magnet_link))

    if magnets:
        down(magnets, folder, raise_ki)

    done()
