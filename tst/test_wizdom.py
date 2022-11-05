from pprint import pprint

from tvpy.wizdom import (Wizdom, download_zips, get_subs_json, select_sub_ids,
                         srts_from_zips)


def test_wizdom():
    imdb_id = 'tt15574312'
    subs = get_subs_json(imdb_id)

    sub_ids = select_sub_ids(
        subs=subs,
        season=1,
        episodes=[1, 2])

    sub_ids = list(sub_ids)
    assert sub_ids == [(1, 1, 300167), (1, 2, 300361)]

    zips = download_zips(sub_ids)
    srts = srts_from_zips(zips)
    srts = list(srts)
    assert len(srts) == 2

    assert srts == list(Wizdom().get_subs(imdb_id=imdb_id, season=1, episodes=[1, 2]))
