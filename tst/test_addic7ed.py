from tvpy.addic7ed import Addic7ed, filter_subs, show_id, subs


def test_addic7ed():
    episodes = {(1, 1), (1, 2), (1, 3)}
    assert show_id('Andor') == '9073'
    ss = list(subs('9073', 1))
    ss = filter_subs(
        subs=ss,
        lang='English',
        episodes=episodes)

    ss = list(ss)
    srts = list(Addic7ed().get_subs(
        query='Andor',
        lang='English',
        episodes=episodes))

    assert len(ss) == len(list(srts))
