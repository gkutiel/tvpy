import json
from importlib import resources




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
