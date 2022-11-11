
from tvpy.wizdom import (Wizdom, download_zips, get_subs_json, select_sub_ids,
                         srts_from_zips)


def test_wizdom():
    imdb_id = 'tt11875316'
    episodes = {(1, 1), (2, 3)}
    subs = get_subs_json(imdb_id)

    sub_ids = select_sub_ids(
        subs=subs,
        episodes=episodes)

    sub_ids = list(sub_ids)
    assert sorted(sub_ids) == [(1, 1, 252486), (2, 3, 300385)]

    zips = download_zips(sub_ids)
    srts = srts_from_zips(zips)
    srts = list(srts)
    assert len(srts) == 2

    assert srts == list(Wizdom().get_subs(
        lang='Hebrew',
        imdb_id=imdb_id,
        episodes=episodes))
