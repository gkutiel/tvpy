from tvpy.util import file_size_in_mb

'3.7 GB'
'1.8 GB'
'222.8 MB'
'2 GB'
'237.1 MB'
'276.4 MB'
'195.2 MB'
'2.3 GB'
'2.4 GB'
'194.3 MB'
'2 GB'
'1.1 GB'
'200.2 MB'
'2 GB'
'1.2 GB'


def test_file_size_in_mb():
    assert file_size_in_mb('1.8 GB') == 1.8 * 2 ** 10
    assert file_size_in_mb('2.4 GB') == 2.4 * 2 ** 10
    assert file_size_in_mb('2 GB') == 2 * 2 ** 10
    assert file_size_in_mb('194.6 MB') == 194.6
    assert file_size_in_mb('157.8 MB') == 157.8
