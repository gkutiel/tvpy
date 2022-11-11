import time

from humanize import naturaldelta, naturaltime

from tvpy.console import cls
from tvpy.tv_clean import tv_clean
from tvpy.tv_download import tv_download
from tvpy.tv_follow import read_follow
from tvpy.tv_info import tv_info
from tvpy.tv_rename import tv_rename
from tvpy.tv_subs import tv_subs
from tvpy.tv_tmdb import tv_tmdb

logo = (r'''
📺📺📺📺📺📺📺📺📺📺📺📺📺📺
[yellow2]  _______    _____       
[yellow2] |__   __|  |  __ \      
[yellow2]    | |_   _| |__) |   _ 
[yellow2]    | \ \ / /  ___/ | | |
[yellow2]    | |\ V /| |   | |_| |
[yellow2]    |_| \_/ |_|    \__, |
[yellow2]                    __/ |
[yellow2]                   |___/ 

🥧🥧🥧🥧🥧🥧🥧🥧🥧🥧🥧🥧🥧                                                        
''')


def tvpy(folder=None, k=3, sleep_sec=None):
    def sep(title):
        cls.print()
        cls.print(f'[dim orchid1]{title}')

    cls.print(logo)

    if folder is None and sleep_sec is None:
        sleep_sec = 600

    try:
        while True:
            folders = read_follow() if folder is None else [folder]
            for folder in folders:
                cls.print(f'[yellow2 bold]{folder}')

                sep('Generating .tvpy.json')
                tv_tmdb(folder)

                sep('Downloading episodes')
                tv_download(folder, k=k, raise_ki=True)

                sep('Renaming files')
                tv_rename(folder)

                sep('Downloading subtitles')
                tv_subs(folder)

                sep('Removing unused files')
                tv_clean(folder)

                tv_info(folder)

            if sleep_sec is None:
                break

            cls.print(f'[info]💤 Sleeping for {naturaldelta(sleep_sec)} 💤. (press CTRL+C to abort)')
            time.sleep(sleep_sec)
    except KeyboardInterrupt:
        cls.print('[warn]Aborted')
        pass
