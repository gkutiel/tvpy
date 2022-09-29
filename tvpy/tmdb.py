import json
import re

import requests



def imdb_id(key, id):
    res = requests.get(f'https://api.themoviedb.org/3/tv/{id}?api_key={key}&append_to_response=external_ids')
    res = res.json()
    return res['external_ids']['imdb_id']


def imdb_rating(id):
    url = f'https://p.media-imdb.com/static-content/documents/v1/title/{id}/ratings%3Fjsonp=imdb.rating.run:imdb.api.title.ratings/data.json?u=null&s=p3'
    res = requests.get(url).text
    res = re.search(r'\{.*\}', res)
    assert res is not None
    res = json.loads(res.group(0))
    resource = res['resource']
    return {k: resource[k] for k in ('rating', 'ratingCount')}


def search(key, q):
    FIELDS = [
        'id',
        'name',
        'poster_path',
        'overview']

    try:
        url = f'https://api.themoviedb.org/3/search/tv/?api_key={key}&query={q}'
        res = requests.get(url)
        res = res.json()
        res = res['results'][0]
        id = imdb_id(key, res['id'])

        poster_path = res['poster_path']
        poster_path = f'https://image.tmdb.org/t/p/original/{poster_path}'

        res['poster_path'] = poster_path
        res = {f: res[f] for f in FIELDS}
        res |= imdb_rating(id)
        res |= {'imdb_id': id}

        return res
    except Exception as e:
        return None
