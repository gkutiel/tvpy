from pathlib import Path

import toml
from simple_term_menu import TerminalMenu

from tvpy.console import cls

VERSION = 0.4
POSTER_WIDTH = 160
DATE_FORMAT = r'%Y-%m-%d'
CACHE_DAYS = 1


LANGS = [
    'Arabic',
    'Bulgarian',
    'Croatian',
    'Czech',
    'Dutch',
    'English',
    'French',
    'German',
    'Greek',
    'Hebrew',
    'Hungarian',
    'Italian',
    'Norwegian',
    'Persian',
    'Portuguese',
    'Romanian',
    'Russian',
    'Spanish',
    'Swedish',
    'Turkish']


class keys:
    lang = 'lang'
    TVPY_HOME = 'TVPY_HOME'
    follow = 'follow'


def save_config(config):
    with open(Path.home() / '.tvpy.toml', 'w') as f:
        toml.dump(config, f)


def init_config():
    save_config({
        keys.lang: '',
        keys.TVPY_HOME: str(Path.home() / 'tvpy'),
        keys.follow: []})


def load_config():
    home = Path.home()
    tvpy_toml = home / '.tvpy.toml'
    if not tvpy_toml.exists():
        init_config()

    with open(tvpy_toml) as f:
        config = toml.load(f)
        lang = config[keys.lang]
        if lang not in LANGS:
            cls.print('[info]Please select the subtitle language:')
            i = TerminalMenu(LANGS).show()
            assert type(i) is int
            config[keys.lang] = LANGS[i]
            save_config(config)

        return config
