import base64
import json
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image
from rich import print
from rich.status import Status

from tvpy.config import POSTER_WIDTH, VERSION
from tvpy.tmdb import get, imdb_id, imdb_rating, search
from tvpy.util import load_key


def load_tvpy(folder):
    folder = Path(folder)
    tvpy_json = folder / '.tvpy.json'
    with open(tvpy_json, 'r') as f:
        return json.load(f)


def img_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    poster_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return poster_base64


def resize_poster(img, width=POSTER_WIDTH):
    w, h = img.size
    img = img.resize((width, int(width / w * h)))
    return img


def get_img(poster_path):
    response = requests.get(poster_path)
    img = Image.open(BytesIO(response.content))
    return img


def tv_json(folder):
    folder = Path(folder)
    key = load_key()
    tvpy_json = folder / '.tvpy.json'

    try:
        with open(tvpy_json, 'r') as out:
            assert json.load(out)['version'] == VERSION

    except:
        with Status('[orange1]Searching...') as status:
            name = folder.name.replace('.', ' ').replace('_', ' ')
            res = search(key, name)

            if res is None:
                status.update('[red]Error')
                status.stop()
                return

            status.update('[green]Saving...')
            tmdb_id = res['id']
            poster = get_img(res['poster_path'])
            poster = resize_poster(poster)
            poster.save(folder / '.poster.jpg')

            iid = imdb_id(key, tmdb_id)

            res = get(key, tmdb_id)
            res |= {'imdb_id': iid}
            res |= imdb_rating(iid)

        with open(tvpy_json, 'w') as out:
            json.dump({'version': VERSION, 'poster_base64': img_base64(poster)} | res, out)
