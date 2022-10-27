from tvpy.console import cls
from tvpy.tv_down import tv_down
from tvpy.tv_json import tv_json
from tvpy.tv_klyn import tv_klyn
from tvpy.tv_renm import tv_renm
from tvpy.tv_subs import tv_subs

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


def tvpy(folder):
    def sep(title):
        cls.print()
        cls.print(f'[dim orchid1]{title}')

    cls.print(logo)

    sep('Generating .tvpy.json')
    tv_json(folder)

    sep('Downloading episodes')
    tv_down(folder)

    sep('Renaming files')
    tv_renm(folder)

    sep('Downloading subtitles')
    tv_subs(folder)

    sep('Removing unused files')
    tv_klyn(folder)

    sep('Renaming files')
    tv_renm(folder)

    cls.save_svg('demo.svg')
