from pathlib import Path

import requests
from lxml import etree, html
from tqdm import tqdm

from tvpy.subs import SubProvider

HEADERS = {
    'referer': 'https://www.addic7ed.com/',
    'sec-fetch-mode': 'navigate'}


def show_id(name):
    url = f'https://www.addic7ed.com/search.php?search={name}&Submit=Search'
    return requests.get(url, allow_redirects=True).url.split('/')[-1]


def subs(show_id, season):
    res = requests.get(f'https://www.addic7ed.com/ajax_loadShow.php?show={show_id}&season={season}')
    dom = html.fromstring(res.content)
    for tr in dom.cssselect('tr.epeven.completed'):
        tree = etree.ElementTree(tr)
        path = tree.getpath(tr)
        season, episode, lang, *_ = tr.xpath(f'{path}/td/text()')
        link = tr.xpath(f'{path}//a/@href')[-1]
        yield int(season), int(episode), lang, link


class Addic7ed(SubProvider):
    def get_subs(self, *, imdb_id=None, query=None, lang=..., season=..., episodes=...):
        episodes = set(episodes)
        id = show_id(query)
        for s, e, l, link in subs(id, season):
            if e in episodes and l.lower() == lang.lower():
                yield s, e, requests.get(
                    f'https://www.addic7ed.com{link}',
                    headers=HEADERS).text
