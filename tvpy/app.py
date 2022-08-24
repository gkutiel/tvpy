from distutils.log import error
from json import dumps, loads
from tvpy.scan import scan
from tvpy.search import search
from tqdm import tqdm


def load_key():
    with open('key.txt') as f:
        return f.read()


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


def row(*, imdb_id, name, overview, poster_path):
    return ''.join([
        r'<div class="container" style="margin-bottom: 1em">',
        r'<div class="row">',
        r'<div class="colum" style="max-width: 10em; margin-right: 2em">',
        f'<img src=https://image.tmdb.org/t/p/original{poster_path}></img>',
        r'</div>',
        r'<div class="colum">',
        f'<h2>{name}</h2>',
        f'<span class="imdbRatingPlugin" data-title="{imdb_id}" data-style="p3"><a target="_blank" href="https://www.imdb.com/title/{imdb_id}/?ref_=plg_rt_1"><img src="https://ia.media-imdb.com/images/G/01/imdb/plugins/rating/images/imdb_46x22.png" alt="{name}" /></a></span>',
        f'<p>{overview}</p>',
        r'</div>',
        r'</div>',
        r'</div>',
    ])


def tv_html(input_json='tvpy.json', out_html='index.html'):
    with open(input_json) as f:
        with open(out_html, 'w') as h:
            print(r'<!DOCTYPE html>', file=h)
            print(r'<html lang="en">', file=h)
            print(r'<head>', file=h)
            print(r'<meta name="viewport" content="width=device-width, initial-scale=1">', file=h)
            print(r'<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,300italic,700,700italic">', file=h)
            print(r'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.css">', file=h)
            print(r'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/milligram/1.4.1/milligram.css">', file=h)
            print(
                r'<script>(function(d,s,id){var js,stags=d.getElementsByTagName(s)[0];if(d.getElementById(id)){return;}js=d.createElement(s);js.id=id;js.src="https://ia.media-imdb.com/images/G/01/imdb/plugins/rating/js/rating.js";stags.parentNode.insertBefore(js,stags);})(document,"script","imdb-rating-api");</script>', file=h)
            print(r'</head>', file=h)
            print(r'<body>', file=h)
            print(r'<div class="container">', file=h)

            for line in tqdm(f.read().splitlines()):
                line = loads(line)
                r = row(
                    imdb_id=line['imdb_id'],
                    name=line['name'],
                    overview=line['overview'],
                    poster_path=line['poster_path']
                )
                print(r, file=h)

            print(r'</div>', file=h)
            print(r'</body>', file=h)
            print(r'</html>', file=h)
