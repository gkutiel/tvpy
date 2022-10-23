
import re
from pathlib import Path

import PTN
from rich.pretty import pprint
from tqdm import tqdm

from tvpy.tv_json import load_tvpy
from tvpy.util import files


def tv_renm(folder):
    folder = Path(folder)
    tvpy = load_tvpy(folder)
    title = tvpy['name']
    title = re.sub(r'[^a-zA-Z0-9]', ' ', title)
    title = re.sub(r' +', '.', title)
    for file in tqdm(files(folder)):
        try:
            info = PTN.parse(file.name)
            name = f'{title}.S{info["season"]:02d}E{info["episode"]:02d}{file.suffix.lower()}'
            file.rename(folder / name)
        except:
            pass
