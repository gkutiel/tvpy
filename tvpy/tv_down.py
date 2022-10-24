from pathlib import Path
from time import sleep

import libtorrent as lt
from rich.pretty import pprint
from rich.progress import (BarColumn, Progress, TaskProgressColumn, TextColumn,
                           TimeRemainingColumn)

from tvpy.torrent import torrents


def q(folder, season: int, episode: int):
    name = Path(folder).name.replace('.', ' ')

    return f'{name} S{season:02}E{episode:02}'


def show_status(local):
    torrent = local.status()
    print("\r{:.2f}% complete (down: {:.1f} kB/s up: {:.1f} kB/s peers: {:d}) {}".format(
        torrent.progress * 100, torrent.download_rate / 1000, torrent.upload_rate / 1000,
        torrent.num_peers, torrent.state), end=" ")


def down(magnet_link, down_folder):
    s = lt.session()
    params = lt.parse_magnet_uri(magnet_link)
    params.save_path = down_folder
    local = s.add_torrent(params)

    with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            TextColumn('[green]Down: {task.fields[down]} kB/s'),
            TextColumn('[blue]Up: {task.fields[up]} kB/s'),
            TextColumn('[orange1]Peers: {task.fields[peers]}')) as progress:

        task = progress.add_task("[green]Downloading...", total=1, down='', up='', peers='')

        while not progress.finished:
            status = local.status()
            progress.update(
                task,
                completed=status.progress,
                down=f'{status.download_rate / 1000:.1f}',
                up=f'{status.upload_rate / 1000:.1f}',
                peers=status.num_peers)

            sleep(0.02)


def tv_down(folder):
    res = torrents.search(q(folder, 1, 7))
    item = res['items'][0]
    link = item['link']
    info = torrents.info(link)
    magnet_link = info['magnetLink']
    print(magnet_link)
    # down(magnet_link, folder)
