from tvpy.console import cls
from tvpy.tv_clean import tv_clean
from tvpy.tv_config import read_follow_txt, tv_follow
from tvpy.tv_download import tv_download
from tvpy.tv_info import tv_info
from tvpy.tv_rename import tv_rename
from tvpy.tv_subs import tv_subs
from tvpy.tv_tmdb import tv_tmdb

logo = (r'''
[yellow2]      ___           ___           ___           ___     
[yellow2]     /\  \         /\__\         /\  \         |\__\    
[yellow2]     \:\  \       /:/  /        /::\  \        |:|  |   
[yellow2]      \:\  \     /:/  /        /:/\:\  \       |:|  |   
[yellow2]      /::\  \   /:/__/  ___   /::\~\:\  \      |:|__|__ 
[yellow2]     /:/\:\__\  |:|  | /\__\ /:/\:\ \:\__\     /::::\__\
[yellow2]    /:/  \/__/  |:|  |/:/  / \/__\:\/:/  /    /:/~~/~   
[yellow2]   /:/  /       |:|__/:/  /       \::/  /    /:/  /     
[yellow2]   \/__/         \::::/__/         \/__/     \/__/      
[yellow2]                  ~~~~                                  
[yellow2]                                                        
''')


def tvpy(folder=None, k=10):
    def sep(title):
        cls.print()
        cls.print(f'[dim orchid1]{title}')

    cls.print(logo)

    if folder is None:
        folders = read_follow_txt()
    else:
        tv_follow(folder)
        folders = [folder]

    for folder in folders:
        sep('Generating .tvpy.json')
        tv_tmdb(folder)

        sep('Downloading episodes')
        tv_download(folder, k=k)

        sep('Renaming files')
        tv_rename(folder)

        sep('Downloading subtitles')
        tv_subs(folder)

        sep('Removing unused files')
        tv_clean(folder)

        sep('Renaming files')
        tv_rename(folder)

        tv_info(folder)
