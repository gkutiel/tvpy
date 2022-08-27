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


def poster_base64(path, width=160):
    url = f'https://image.tmdb.org/t/p/original/{path}'

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    w, h = img.size
    img = img.resize((width, int(width / w * h)))
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def search(key, q):
    try:
        res = requests.get(f'https://api.themoviedb.org/3/search/tv/?api_key={key}&query={q}')
        res = res.json()
        res = res['results'][0]
        id = imdb_id(key, res['id'])
        return (
            {f: res[f] for f in FIELDS}
            | {'imdb_id': id}
            | imdb_rating(id)
            | {'poster_base64': poster_base64(res['poster_path'])})
    except:
        return None


if __name__ == '__main__':
    rating, count = imdb_rating('tt7826376')
    print(rating, count)
