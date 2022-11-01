from pathlib import Path

import toml
from rich.pretty import pprint


class keys:
    TVPY_HOME = 'TVPY_HOME'
    follow = 'follow'


def load_config():
    home = Path.home()
    config = home / '.tvpy.toml'
    if not config.exists():
        with open(config, 'w') as f:
            tvpy_home = home / 'tvpy'
            follow_txt = home / 'follow.txt'
            toml.dump({
                keys.TVPY_HOME: str(tvpy_home),
                keys.follow: [str(follow_txt)]}, f)

    with open(config) as f:
        return toml.load(f)


def read_follow():
    config = load_config()
    tvpy_home = Path(config[keys.TVPY_HOME])
    tvpy_home.mkdir(parents=True, exist_ok=True)
    follows = set()
    for follow_txt in config[keys.follow]:
        with open(follow_txt, 'r') as f:
            follows |= set(f.read().splitlines())

    return follows


def tv_follow(follow_txt): pass


def tv_config():
    config = load_config()
    pprint(config)
