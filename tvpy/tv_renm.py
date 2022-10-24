
import re
from pathlib import Path

import PTN
from tqdm import tqdm

from tvpy.tv_json import load_tvpy
from tvpy.util import files


def file_name(tvpy, s, e):
    title = tvpy['name']
    title = re.sub(r'[^a-zA-Z0-9]', ' ', title)
    title = re.sub(r' +', '.', title)

    return f'{title}.S{s:02}E{e:02}'


def tv_renm(folder):
    folder = Path(folder)
    tvpy = load_tvpy(folder)
    for file in tqdm(files(folder)):
        try:
            info = PTN.parse(file.name)
            name = f'{file_name(tvpy, info["season"], info["episode"])}{file.suffix.lower()}'
            file.rename(folder / name)
        except:
            pass
