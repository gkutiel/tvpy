from fire import Fire


def tv_json():
    from tvpy.tv_html import tv_json
    Fire(tv_json)


def tv_html():
    from tvpy.tv_html import tv_html
    Fire(tv_html)


def tv_renm():
    from tvpy.tv_renm import tv_renm
    Fire(tv_renm)


def tv_sync():
    from tvpy.tv_sync import tv_sync
    Fire(tv_sync)
