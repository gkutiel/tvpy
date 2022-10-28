import math
import random
import urllib.parse
from dataclasses import dataclass
from pathlib import Path


def get_name(magnet_uri):
    query = urllib.parse.urlparse(magnet_uri).query
    query = urllib.parse.parse_qs(query)

    return query['dn'][0]


@dataclass
class Status:
    progress: float
    total_done: float
    download_rate: float
    upload_rate: float
    num_peers: int


def rnd_file_size_mb():
    return random.randint(200, 300) * 1_048_576


class Handler:
    def __init__(self):
        self.file_size_mb = rnd_file_size_mb()
        self.time = 0
        self.progress = 0
        self.num_peers = 0

    def status(self):
        self.time += 1
        self.num_peers += random.randint(-2, 5)
        self.num_peers = max(1, self.num_peers)
        self.progress += random.random() / 10 * math.log(self.num_peers)
        self.progress = min(1, self.progress)

        total_done = self.file_size_mb * self.progress
        download_rate = total_done / self.time

        return Status(
            progress=self.progress,
            total_done=total_done,
            download_rate=download_rate,
            upload_rate=download_rate / random.randint(8, 12),
            num_peers=self.num_peers)


@dataclass
class Params:
    name: str
    save_path: str = ''


class Session:
    def add_torrent(self, params: Params):
        path = Path(params.save_path) / params.name
        path.mkdir(exist_ok=True)
        path = path / f'{params.name}.mkv'
        path.touch(exist_ok=True)
        return Handler()


class dummy:
    def session(self):
        return Session()

    def parse_magnet_uri(self, link):
        return Params(name=get_name(link))


lt = dummy()

if __name__ == '__main__':
    h = Handler()
    print(h.time)
