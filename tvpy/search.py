import base64
import json
import re
from dataclasses import dataclass
from io import BytesIO
from pprint import pprint

import requests
from PIL import Image

FIELDS = [
    'id',
    'name',
    'poster_path',
    'overview']


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


def poster_base64(url, width=160):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    w, h = img.size
    img = img.resize((width, int(width / w * h)))
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def search(key, q):
    try:
        url = f'https://api.themoviedb.org/3/search/tv/?api_key={key}&query={q}'
        res = requests.get(url)
        res = res.json()
        res = res['results'][0]
        id = imdb_id(key, res['id'])
        return (
            {f: res[f] for f in FIELDS}
            | imdb_rating(id)
            | {
                'imdb_id': id,
                'poster_path': f'https://image.tmdb.org/t/p/original/{res["poster_path"]}'})
    except Exception as e:
        return None


if __name__ == '__main__':
    rating, count = imdb_rating('tt7826376')
    print(rating, count)
