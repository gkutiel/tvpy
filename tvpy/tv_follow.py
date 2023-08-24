from pathlib import Path

from tvpy.config import default, load_config, save_config
from tvpy.util import title2folder_name


def read_follow():
    config = load_config()
    return config[default.follow.name]


def tv_unfollow(folder):
    path = str(Path(folder).absolute())
    config = load_config()
    follows = set(config[default.follow.name]) - {path}
    config[default.follow.name] = follows
    save_config(config)


def tv_follow(folder):
    path = str(Path(folder).absolute())
    config = load_config()
    follows = list(set(config[default.follow.name] + [path]))
    config[default.follow.name] = follows
    save_config(config)
