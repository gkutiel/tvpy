from fire import Fire


def tv_follow():
    from tvpy.tv_follow import tv_follow
    Fire(tv_follow)


def tv_tmdb():
    from tvpy.tv_tmdb import tv_tmdb
    Fire(tv_tmdb)


def tv_download():
    from tvpy.tv_download import tv_download
    Fire(tv_download)


def tv_subs():
    from tvpy.tv_subs import tv_subs
    Fire(tv_subs)


def tv_rename():
    from tvpy.tv_rename import tv_rename
    Fire(tv_rename)


def tv_clean():
    from tvpy.tv_clean import tv_clean
    Fire(tv_clean)


def tv_info():
    from tvpy.tv_info import tv_info
    Fire(tv_info)


def tv_html():
    from tvpy.tv_html import tv_html
    Fire(tv_html)


def tvpy():
    from tvpy.tvpy import tvpy
    Fire(tvpy)


if __name__ == '__main__':
    import json

    from py1337x import py1337x

    with open('tmp.json', 'w') as f:

        json.dump(py1337x().search('Andor'), f)
