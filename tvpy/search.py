from pprint import pprint
from dataclasses import dataclass
import requests

FIELDS = [
    'id',
    'name',
    'poster_path',
    'overview',
    'vote_average',
    'vote_count']


def imdb_id(key, id):
    res = requests.get(f'https://api.themoviedb.org/3/tv/{id}?api_key={key}&append_to_response=external_ids')
    res = res.json()
    return res['external_ids']['imdb_id']


def search(key, q):
    try:
        res = requests.get(f'https://api.themoviedb.org/3/search/tv/?api_key={key}&query={q}')
        res = res.json()
        res = res['results'][0]
        return {f: res[f] for f in FIELDS} | {'imdb_id': imdb_id(key, res['id'])}
    except:
        return None
