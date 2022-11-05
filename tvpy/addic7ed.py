from pathlib import Path

import requests
from lxml import etree, html
from tqdm import tqdm


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


def download(*, name, season, lang, episodes, out_folder):
    episodes = set(episodes)
    out_folder = Path(out_folder)
    id = show_id(name)
    for s, e, l, link in tqdm(subs(id, season)):
        if e in episodes and l.lower() == lang.lower():
            print(link)
            out_srt = out_folder / f'{name}.S{s:02}E{e:02}.srt'
            with open(out_srt, 'w') as out:
                srt = requests.get(
                    f'https://www.addic7ed.com{link}',
                    headers={
                        'referer': 'https://www.addic7ed.com/',
                        'sec-fetch-mode': 'navigate'}).text

                out.write(srt)

            episodes.remove(e)
