from pathlib import Path

from tvpy.config import default, load_config, save_config
from tvpy.util import title2folder_name


def read_follow():
    config = load_config()
    tvpy_home = Path(config[default.TVPY_HOME.name])
    tvpy_home.mkdir(parents=True, exist_ok=True)
    follows = set()
    for follow_txt in config[default.follow.name]:
        with open(follow_txt, 'r') as f:
            follows |= set(f.read().splitlines())

    return {tvpy_home / title2folder_name(f) for f in follows if f}


def tv_follow(file):
    '''follow a file

    Args:
        file: follow this file
    '''
    path = str(Path(file).absolute())
    config = load_config()
    config[default.follow.name] = list(set(config[default.follow.name] + [path]))
    save_config(config)
