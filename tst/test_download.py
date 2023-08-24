from tvpy.tv_download import search_torrent
import json
from pprint import pprint


def test_search():
    info = search_torrent('Andor S01E01')
    assert info is not None
    link = info['magnetLink']
    assert link[:6] == 'magnet'


def test_search_2():
    info = search_torrent('Ahsoka S01E01')
    pprint(info)
    assert info is not None
    link = info['magnetLink']
    assert link[:6] == 'magnet'
