
import PTN
from tqdm import tqdm

from tvpy.util import files


def tv_renm(root):
    for file in tqdm(files(root)):
        try:
            info = PTN.parse(file.name)

            title = info['title'].replace(' ', '.')
            season = info['season']
            episode = info['episode']

            name = f'{title}.S{season:02d}E{episode:02d}{file.suffix.lower()}'
            file.rename(file.parent / name)
        except:
            pass
