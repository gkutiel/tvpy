from pprint import pprint

from py1337x import py1337x

torrents = py1337x()


def show_status(local):
    torrent = local.status()
    print("\r{:.2f}% complete (down: {:.1f} kB/s up: {:.1f} kB/s peers: {:d}) {}".format(
        torrent.progress * 100,
        torrent.download_rate / 1000,
        torrent.upload_rate / 1000,
        torrent.num_peers,
        torrent.state), end=" ")


if __name__ == '__main__':
    res = torrents.search('Andor S01E01')
    pprint(res)
    # s = lt.session()
    # magnet_uri = 'magnet:?xt=urn:btih:7AEE6A3FD1DBC0DE5031638C6F40314FAB8E79E4&dn=Accident+Man%3A+Hitman%27s+Holiday+%282022%29+%5B720p%5D+%5BYTS.MX%5D&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2710%2Fannounce&tr=udp%3A%2F%2Fp4p.arenabg.ch%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.cyberia.is%3A6969%2Fannounce&tr=http%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce'
    # params = lt.parse_magnet_uri(magnet_uri)
    # params.save_path = '/tmp'
    # local = s.add_torrent(params)

    # while True:
    #     show_status(local)
    # info = lt.torrent_info('/tmp/movie/movie.mp4')
    # print(info)
    # lt.make_magnet_uri()
