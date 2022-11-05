import io
import zipfile

import requests

from tvpy.subs import SubProvider

# def down_sub(sub_id, out_zip):
#     url = f'https://wizdom.xyz/api/files/sub/{sub_id}'
#     with open(out_zip, 'wb') as out:
#         out.write(requests.get(url).content)


def get_subs_json(imdb_id):
    url = f'https://wizdom.xyz/api/releases/{imdb_id}'
    res = requests.get(url).json()
    return res['subs']


def select_sub_ids(*, subs, episodes):
    for s, e in episodes:
        try:
            yield s, e, subs[f'{s}'][f'{e}'][0]['id']
        except:
            pass


def download_zips(sub_ids):
    for s, e, id in sub_ids:
        url = f'https://wizdom.xyz/api/files/sub/{id}'
        yield s, e, requests.get(url).content


def srts_from_zips(zips):
    for s, e, zip in zips:
        with zipfile.ZipFile(io.BytesIO(zip)) as z:
            srts = [f for f in z.infolist() if f.filename[-4:] == '.srt']
            for srt in srts:
                with z.open(srt, 'r') as content:
                    yield s, e, content.read()


class Wizdom(SubProvider):
    def get_subs(self, *, imdb_id=None, query=None, lang=None, episodes=...):
        assert lang == 'Hebrew'
        sub_ids = select_sub_ids(
            subs=get_subs_json(imdb_id),
            episodes=episodes)

        zips = download_zips(sub_ids)
        yield from srts_from_zips(zips)
