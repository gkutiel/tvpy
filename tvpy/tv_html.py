from importlib import resources

from tvpy.tv_tmdb import load_tvpy


def tv_html(folder, out_html='index.html'):
    import tvpy

    css = resources.read_text(tvpy, 'index.css')
    js = resources.read_text(tvpy, 'index.js')
    html = resources.read_text(tvpy, 'index.html')

    data = [load_tvpy(folder)]

    html = html.format(data=data, js=js, css=css)

    with open(out_html, 'w') as h:
        h.write(html)
