
VERSION = 0.3
POSTER_WIDTH = 160


class format:
    resolution = '720p'
    encoder = 'NTB'


if __name__ == '__main__':
    from pprint import pprint

    import PTN
    p = PTN.parse('Star.Wars.Andor.S01E07.Announcement.1080p.DSNP.WEB-DL.DDP5.1.1.H.264-NTb.zip')
    pprint(p)
