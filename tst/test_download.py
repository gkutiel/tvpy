import json
from pprint import pprint

from py1337x import py1337x


def test_search():
    torrents = py1337x()
    pprint(torrents.search('Andor'))


if __name__ == '__main__':
    torrents = py1337x()
    with open('1337.json', 'w') as f:
        json.dump(torrents.search('Andor'), f)
