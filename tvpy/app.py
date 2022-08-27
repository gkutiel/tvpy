import tvpy
from json import dumps, loads
from tvpy.scan import scan
from tvpy.search import search
from tqdm import tqdm
from importlib import resources


def load_key():
    with open('key.txt') as f:
        return f.read().strip()


def tv_json(root, output_json='tvpy.json', err_txt='err.txt'):
    key = load_key()
    errors = 0
    with open(output_json, 'w') as f:
        with open(err_txt, 'w') as e:
            names = tqdm(scan(root))
            for name in names:
                res = search(key, name.replace('.', ' '))
                if res is None:
                    errors += 1
                    print(name, file=e)
                    names.set_postfix(errors=errors)
                    continue
                print(dumps(res), file=f)


def tv_html(input_json='tvpy.json', out_html='index.html'):
    with open(input_json) as f:
        data = [loads(line) for line in f.read().splitlines()]

    css = resources.read_text(tvpy, 'index.css')
    js = resources.read_text(tvpy, 'index.js')
    html = resources.read_text(tvpy, 'index.html')

    html = html.format(data=data, js=js, css=css)

    with open(out_html, 'w') as h:
        h.write(html)
