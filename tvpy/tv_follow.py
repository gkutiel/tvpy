from pathlib import Path


from tvpy.config import keys, load_config, save_config


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
    path = str(Path(file).absolute())
    config = load_config()
    config[keys.follow] = list(set(config[keys.follow] + [path]))
    save_config(config)
