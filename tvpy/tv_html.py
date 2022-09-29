import base64
import json
from importlib import resources
from io import BytesIO
from xml.etree.ElementTree import VERSION

import requests
from PIL import Image

from tvpy.config import POSTER_WIDTH
from tvpy.tmdb import search
from tvpy.util import folders, load_key


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


def tv_json(root):
    key = load_key()

    for folder in folders(root):
        action, status = 'Uptodate', '[green]SUCCESS'
        tvpy_json = folder / '.tvpy.json'

        try:
            with open(tvpy_json, 'r') as out:
                assert json.load(out)['version'] == VERSION

        except:
            with open(tvpy_json, 'w') as out:
                action = 'Downloading'
                name = folder.name.replace('.', ' ').replace('_', ' ')
                res = search(key, name)
                if res is None:
                    status = '[red]ERROR'
                else:
                    poster = get_img(res['poster_path'])
                    poster = resize_poster(poster)
                    poster.save(folder / '.poster.jpg')
                    json.dump({'version': VERSION, 'poster_base64': img_base64(poster)} | res, out)

        print(f'{str(folder):<70}', f'{action:<13}', status)


def tv_html(input_json='tvpy.json', out_html='index.html'):
    import tvpy
    with open(input_json) as f:
        data = [json.loads(line) for line in f.read().splitlines()]

    css = resources.read_text(tvpy, 'index.css')
    js = resources.read_text(tvpy, 'index.js')
    html = resources.read_text(tvpy, 'index.html')

    html = html.format(data=data, js=js, css=css)

    with open(out_html, 'w') as h:
        h.write(html)
