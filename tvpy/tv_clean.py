import shutil
from pathlib import Path

from PTN import parse

from tvpy.console import cls
from tvpy.util import done

keep_types = {'MKV', 'MP4', 'AVI', 'SRT'}


def must_keep(p: Path):
    if p.is_dir():
        return not can_remove(p)

    info = parse(p.name)

    return (
        'season' in info
        and 'episode' in info
        and 'filetype' in info
        and info['filetype'] in keep_types)


def can_remove(p: Path):
    info = parse(p.name)

    if 'season' not in info or 'episode' not in info:
        return False

    if p.is_dir():
        return not any(must_keep(f) for f in p.iterdir())

    if not 'filetype' in info:
        return True

    return info['filetype'] not in keep_types


def tv_clean(folder):
    folder = Path(folder)
    for f in folder.iterdir():
        if can_remove(f):
            cls.print(f':wastebasket: [warn]{f.name}')
            if f.is_dir():
                shutil.rmtree(f)
            else:
                f.unlink()

    done()
