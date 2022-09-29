from pathlib import Path

import PTN
from tqdm import tqdm

from tvpy.util import files


def tv_sync(src, dst):
    src, dst = Path(src), Path(dst)
    bar = tqdm(files(src))
    for file in bar:
        try:
            info = PTN.parse(file.name)

            title = info['title'].replace(' ', '.')
            season = info['season']
            episode = info['episode']

            dst_folder = dst / title
            dst_folder.mkdir(exist_ok=True)
            dst_file = dst_folder / f'{title}.S{season:02d}E{episode:02d}{file.suffix.lower()}'
            bar.set_description(f'Moving {dst_file}')
            file.rename(dst_file)
        except:
            pass
