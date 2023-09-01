import time

from humanize import naturaldelta

from tvpy.console import cls
from tvpy.tv_clean import tv_clean
from tvpy.tv_download import tv_download
from tvpy.tv_follow import read_follow, tv_follow, tv_unfollow
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


def tvpy(folder=None,  k=3):
    cls.print(logo)

    if folder is None:
        folders = read_follow()
    else:
        tv_follow(folder)
        folders = [folder]

    for folder in folders:
        err_msg = f'[red]Something went wrong with {folder}. Unfollowing...'
        try:
            tvpy_folder(folder, k)
        except:
            cls.print(err_msg)
            tv_unfollow(folder)


def tvpy_folder(folder, k):
    def sep(title):
        cls.print()
        cls.print(f'[dim orchid1]{title}')
    try:
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

    except KeyboardInterrupt:
        cls.print(f'[warn]Aborting {folder}')
