
from pathlib import Path

import PTN

from tvpy.console import cls
from tvpy.tv_tmdb import load_tvpy
from tvpy.util import done, files_r, title2file_name


def tv_rename(folder):
    folder = Path(folder)
    tvpy = load_tvpy(folder)
    for file in files_r(folder):
        try:
            info = PTN.parse(file.name)
            name = f'{title2file_name(tvpy["name"], info["season"], info["episode"])}{file.suffix.lower()}'
            if name != file.name:
                file.rename(folder / name)
                cls.print(f':keyboard: [success]{name}')
        except:
            pass

    done()
