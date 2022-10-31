from pathlib import Path

import toml
from rich.pretty import pprint


def load_config():
    home = Path.home()
    config = home / '.tvpy.toml'
    if not config.exists():
        with open(config, 'w') as f:
            tvpy_home = home / 'tvpy'
            follow_txt = home / 'follow.txt'
            toml.dump({
                'TVPY_HOME': str(tvpy_home),
                'resolution': '720p',
                'follow.txt': str(follow_txt)}, f)

    with open(config) as f:
        return toml.load(f)


def read_follow_txt():
    config = load_config()
    tvpy_home = Path(config['TVPY_HOME'])
    tvpy_home.mkdir(parents=True, exist_ok=True)
    with open(config['follow.txt'], 'r') as f:
        return [tvpy_home / folder for folder in f.read().splitlines()]


def tv_folo(folder):
    config = load_config()
    with open(config['follow.txt'], 'a') as f:
        print(Path(folder).name, file=f)


def tv_cnfg():
    config = load_config()
    pprint(config)
