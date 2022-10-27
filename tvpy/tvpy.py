from tvpy.tv_down import tv_down
from tvpy.tv_json import tv_json
from tvpy.tv_renm import tv_renm
from tvpy.tv_subs import tv_subs


def tvpy(folder):
    tv_json(folder)
    tv_down(folder)
    tv_subs(folder)
    tv_renm(folder)
