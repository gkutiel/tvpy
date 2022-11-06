import base64
import json
from datetime import datetime
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image
from rich.status import Status

from tvpy.config import CACHE_DAYS, DATE_FORMAT, POSTER_WIDTH, VERSION
from tvpy.console import cls
from tvpy.tmdb import get, imdb_id, imdb_rating, search
from tvpy.util import done, load_key, name2title


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


def load_tvpy(folder, tries=1):
    try:
        folder = Path(folder)

        tvpy_json = folder / '.tvpy.json'
        with open(tvpy_json, 'r') as f:
            tvpy = json.load(f)

        assert tvpy['version'] == VERSION

        delta = datetime.now() - datetime.strptime(tvpy['uptodate'], DATE_FORMAT)
        assert delta.days <= CACHE_DAYS

        return tvpy
    except:
        if tries <= 0:
            raise FileNotFoundError(f'Can not load or download {tv_tmdb}')

        tv_tmdb(folder)
        return load_tvpy(folder, tries - 1)


def tv_tmdb(folder, force=False):
    folder = Path(folder)
    folder.mkdir(exist_ok=True)

    key = load_key()
    tvpy_json = folder / '.tvpy.json'

    with Status('', console=cls) as status:
        try:
            assert not force
            load_tvpy(folder)
        except:
            status.update('[info]Searching TMDB...')
            query = name2title(folder.name)
            res = search(key, query)

            if res is None:
                status.stop()
                cls.print(f'[err]Error:[/err] Could not find info for {query}')
                return

            tmdb_id = res['id']
            poster = get_img(res['poster_path'])
            poster = resize_poster(poster)
            poster.save(folder / '.poster.jpg')

            iid = imdb_id(key, tmdb_id)

            res = get(key, tmdb_id)
            res = {**res, **imdb_rating(iid)}
            res['version'] = VERSION
            res['uptodate'] = datetime.now().strftime(DATE_FORMAT)
            res['imdb_id'] = iid
            # res['poster_base64'] = img_base64(poster)
            with open(tvpy_json, 'w') as out:
                json.dump(res, out)

    done()
