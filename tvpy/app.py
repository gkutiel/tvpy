from json import dumps, loads
from tvpy.scan import scan
from tvpy.search import search
from tqdm import tqdm


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


def row(*, poster_base64, name, overview, imdb_id, imdb_rating, imdb_rating_count):
    return ''.join([
        r'<div class="container" style="margin-bottom: 1em">',
        r'<div class="row">',
        r'<div class="colum" style="margin-right: 2em">',
        f'<a target="_blank" href="https://www.imdb.com/title/{imdb_id}/"><img style="max-width:160px;" src="data:image/jpg;base64,{poster_base64}"/></a>',
        r'</div>',
        r'<div class="colum">',
        f'<h2>{name}</h2>',
        f'<h4><b>{imdb_rating}</b> <small>by {imdb_rating_count:,} users</small></h4>',
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
            print(r'<style>.rating{margin-left:.5em;}</style>', file=h)
            print(r'<title>TvPy</title>', file=h)
            print(r'<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📺</text></svg>">', file=h)
            print(r'<meta name="viewport" content="width=device-width, initial-scale=1">', file=h)
            print(r'<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,300italic,700,700italic">', file=h)
            print(r'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.css">', file=h)
            print(r'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/milligram/1.4.1/milligram.css">', file=h)
            print(r'</head>', file=h)
            print(r'<body style="padding-top: 2em;">', file=h)
            print(r'<div class="container">', file=h)

            for line in tqdm(f.read().splitlines()):
                line = loads(line)
                r = row(
                    imdb_id=line['imdb_id'],
                    name=line['name'],
                    overview=line['overview'],
                    poster_base64=line['poster_base64'],
                    imdb_rating=line['rating'],
                    imdb_rating_count=line['ratingCount']
                )
                print(r, file=h)

            print(r'</div>', file=h)
            print(r'</body>', file=h)
            print(r'</html>', file=h)
