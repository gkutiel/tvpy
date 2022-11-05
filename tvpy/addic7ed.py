from collections import defaultdict

import requests
from lxml import etree, html

from tvpy.config import LANGS
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


def filter_subs(*, subs, lang, episodes):
    episodes = set(episodes)
    for s, e, l, link in subs:
        if (s, e) in episodes and l.lower() == lang.lower():
            episodes.remove((s, e))
            yield s, e, link


class Addic7ed(SubProvider):
    def get_subs(self, *, imdb_id=None, query=None, lang=..., episodes=...):
        assert lang in LANGS

        id = show_id(query)
        se = defaultdict(set)
        for s, e in episodes:
            se[s].add(e)

        for season in se.keys():
            for s, e, link in filter_subs(
                    subs=subs(id, season),
                    lang=lang,
                    episodes=episodes):

                yield s, e, requests.get(
                    f'https://www.addic7ed.com{link}',
                    headers=HEADERS).content
