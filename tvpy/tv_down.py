from pathlib import Path
from time import sleep

import libtorrent as lt
from PTN import parse
from rich.progress import (BarColumn, Progress, TaskProgressColumn, TextColumn,
                           TimeRemainingColumn)

from tvpy.torrent import torrents
from tvpy.tv_json import load_tvpy
from tvpy.tv_renm import file_name
from tvpy.util import files_media


def q(folder, season: int, episode: int):
    name = Path(folder).name.replace('.', ' ')

    return f'{name} S{season:02}E{episode:02}'


def show_status(local):
    torrent = local.status()
    print("\r{:.2f}% complete (down: {:.1f} kB/s up: {:.1f} kB/s peers: {:d}) {}".format(
        torrent.progress * 100, torrent.download_rate / 1000, torrent.upload_rate / 1000,
        torrent.num_peers, torrent.state), end=" ")


def down(name, magnet_link, down_folder):
    s = lt.session()
    params = lt.parse_magnet_uri(magnet_link)
    params.save_path = down_folder
    h = s.add_torrent(params)

    with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            TextColumn('[magenta]Size: {task.fields[size]} MB'),
            TextColumn('[green]Down: {task.fields[down]} kB/s'),
            TextColumn('[blue]Up: {task.fields[up]} kB/s'),
            TextColumn('[orange1]Peers: {task.fields[peers]}')) as progress:

        task = progress.add_task(f'[green]{name}', total=1, size='', down='', up='', peers='')

        while not progress.finished:
            status = h.status()
            progress.update(
                task,
                completed=status.progress,
                size=f'{status.total_download / 1048576:.1f}',
                down=f'{status.download_rate / 1000:.1f}',
                up=f'{status.upload_rate / 1000:.1f}',
                peers=status.num_peers)

            sleep(1)


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


def missing_episodes(folder, tvpy):
    return on_air_episodes(tvpy) - existing_episodes(folder)


def tv_down(folder):
    tvpy = load_tvpy(folder)
    for s, e in missing_episodes(folder, tvpy):
        name = file_name(tvpy, s, e)
        magnet = Path(folder) / f'{name}.magnet'
        if magnet.exists():
            with open(magnet, 'r') as f:
                magnet_link = f.read()
        else:
            res = torrents.search(q(folder, s, e))
            item = res['items'][0]
            link = item['link']
            info = torrents.info(link)

            magnet_link = info['magnetLink']
            with open(magnet, 'w') as f:
                f.write(magnet_link)

        down(name, magnet_link, folder)
