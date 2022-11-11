from enum import Enum
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
    # 'Spanish',
    'Swedish',
    'Turkish']


class default(Enum):
    lang = ''
    TVPY_HOME = Path.home() / 'tvpy'
    follow = []


def save_config(config):
    with open(Path.home() / '.tvpy.toml', 'w') as f:
        toml.dump(config, f)


def init_config():
    save_config({
        default.lang.name: '',
        default.TVPY_HOME.name: str(Path.home() / 'tvpy'),
        default.follow.name: []})


def validate(config):
    for key in default:
        if key.name not in config:
            config[key.name] = key.value

    return config


def load_config():
    home = Path.home()
    tvpy_toml = home / '.tvpy.toml'
    if not tvpy_toml.exists():
        init_config()

    with open(tvpy_toml, 'r') as f:
        config = validate(toml.load(f))
        lang = config[default.lang.name]
        if lang not in LANGS:
            cls.print('[info]Please select the subtitle language:')
            i = TerminalMenu(LANGS).show()
            assert type(i) is int
            config[default.lang.name] = LANGS[i]
            save_config(config)

        return config


def get_lang():
    config = load_config()
    return config[default.lang.name]
