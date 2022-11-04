from pathlib import Path
from typing import Union

import toml
from rich.pretty import pprint


class keys:
    TVPY_HOME = 'TVPY_HOME'
    follow = 'follow'


def save_config(config):
    with open(Path.home() / '.tvpy.toml', 'w') as f:
        toml.dump(config, f)


def load_config():
    home = Path.home()
    tvpy_toml = home / '.tvpy.toml'
    if not tvpy_toml.exists():
        config = {
            keys.TVPY_HOME: str(home / 'tvpy'),
            keys.follow: []}

        save_config(config)

    with open(tvpy_toml) as f:
        return toml.load(f)


def read_follow():
    config = load_config()
    tvpy_home = Path(config[keys.TVPY_HOME])
    tvpy_home.mkdir(parents=True, exist_ok=True)
    follows = set()
    for follow_txt in config[keys.follow]:
        with open(follow_txt, 'r') as f:
            follows |= set(f.read().splitlines())

    return [tvpy_home / f for f in follows]


def tv_follow(file):
    '''follow a file

    Args:
        file: follow this file
    '''
    config = load_config()
    config[keys.follow] = list(set(config[keys.follow] + [Path(file).absolute()]))
    save_config(config)
