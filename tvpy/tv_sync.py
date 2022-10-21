from pathlib import Path
from traceback import print_exception

import PTN
import toml
from fs import open_fs
from tqdm import tqdm

from tvpy.util import files, url_folder_name


def url_mv(src, dst):
    try:
        src_folder, src_name = url_folder_name(src)
        dst_folder, dst_name = url_folder_name(dst)

        print(src_folder, dst_folder)
        with open_fs(src_folder) as s, open_fs(dst_folder) as d:
            total = s.getsize(src_name)
            bar = tqdm(
                total=total,
                desc=dst,
                unit_scale=True,
                unit='b')

            with s.open(src_name, 'rb') as sf, d.open(dst_name, 'wb') as df:
                while total:
                    bs = sf.read(2 << 20)
                    df.write(bs)
                    bar.update(len(bs))
                    total -= len(bs)

            assert s.getsize(src_name) == d.getsize(dst_name)
            s.remove(src_name)
    except Exception as e:
        print(e)


def tv_sync(tvpy_toml='~/.tvpy.toml'):
    config = toml.load(Path(tvpy_toml).expanduser())
    src = Path(config['src'])
    dst = config['dst']

    for file in files(src):
        try:
            info = PTN.parse(file.name)

            title = info['title'].replace(' ', '.')
            season = info['season']
            episode = info['episode']

            dst_folder = Path(dst) / title
            dst_folder.mkdir(exist_ok=True)
            dst_file = dst_folder / f'{title}.S{season:02d}E{episode:02d}{file.suffix.lower()}'
        except Exception as e:
            print_exception(type(e), e, e.__traceback__)
            continue

        try:
            print(f'Moving {dst_file}')
            file.rename(dst_file)
        except:
            url_mv(file, dst_file)


if __name__ == '__main__':
    from fs.move import move_file
    src = '/tmp/baba.mp4'
    dst = 'smb://gilad:@mybooklive:/video/download/baba.mp4'
    move_file('/tmp/', 'baba.mp4', 'smb://gilad:@mybooklive:/video/download/', 'lala.mp4')
