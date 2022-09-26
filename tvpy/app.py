import base64
import json
import re
from dataclasses import dataclass
from io import BytesIO
from pprint import pprint

import requests
from PIL import Image

from PIL import Image
import requests
import tvpy
import json
from json import dumps, loads
from tvpy.scan import folders
from tvpy.search import search
from tqdm import tqdm
from importlib import resources
from rich import print

VERSION = 0.1
WIDTH = 160


def load_key():
    with open('key.txt') as f:
        return f.read().strip()


def tv_json(root):
    key = load_key()

    for folder in folders(root):
        action, status = 'Uptodate', '[green]SUCCESS'
        tvpy_json = folder / '.tvpy.json'

        try:
            with open(tvpy_json, 'r') as out:
                assert json.load(out)['version'] == VERSION

        except Exception as e:
            with open(tvpy_json, 'w') as out:
                action = 'Downloading'
                name = folder.name.replace('.', ' ').replace('_', ' ')
                res = search(key, name)
                if res is None:
                    status = '[red]ERROR'
                else:
                    response = requests.get(res['poster_path'])
                    img = Image.open(BytesIO(response.content))
                    w, h = img.size
                    img = img.resize((WIDTH, int(WIDTH / w * h)))
                    buffered = BytesIO()
                    img.save(folder / '.tvpy.jpg')
                    img.save(buffered, format="JPEG")
                    poster_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    json.dump({'version': VERSION, 'poster_base64': poster_base64} | res, out)

        print(f'{str(folder):<70}', f'{action:<13}', status)


def tv_html(input_json='tvpy.json', out_html='index.html'):
    with open(input_json) as f:
        data = [loads(line) for line in f.read().splitlines()]

    css = resources.read_text(tvpy, 'index.css')
    js = resources.read_text(tvpy, 'index.js')
    html = resources.read_text(tvpy, 'index.html')

    html = html.format(data=data, js=js, css=css)

    with open(out_html, 'w') as h:
        h.write(html)
