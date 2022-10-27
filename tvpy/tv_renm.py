
import re
from pathlib import Path

import PTN

from tvpy.console import cls
from tvpy.tv_json import load_tvpy
from tvpy.util import done, files_r


def file_name(tvpy, s, e):
    title = tvpy['name']
    title = re.sub(r'[^a-zA-Z0-9]', ' ', title)
    title = re.sub(r' +', '.', title)

    return f'{title}.S{s:02}E{e:02}'


def tv_renm(folder):
    folder = Path(folder)
    tvpy = load_tvpy(folder)
    for file in files_r(folder):
        try:
            info = PTN.parse(file.name)
            name = f'{file_name(tvpy, info["season"], info["episode"])}{file.suffix.lower()}'
            if name != file.name:
                file.rename(folder / name)
                cls.print(f':keyboard: [success]{name}')
        except:
            pass

    done()
