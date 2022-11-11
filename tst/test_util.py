from pathlib import Path

from tvpy.util import (file_size_in_mb, name2title, title2file_name,
                       title2folder_name)


def test_file_size_in_mb():
    assert file_size_in_mb('1.8 GB') == 1.8 * 2 ** 10
    assert file_size_in_mb('2.4 GB') == 2.4 * 2 ** 10
    assert file_size_in_mb('2 GB') == 2 * 2 ** 10
    assert file_size_in_mb('194.6 MB') == 194.6
    assert file_size_in_mb('157.8 MB') == 157.8


def test_name2title():
    assert name2title('/home/mybooklive/tv/The.Peripheral/') == 'The Peripheral'
    assert name2title('The.Peripheral') == 'The Peripheral'
    assert name2title('The Peripheral') == 'The Peripheral'


def test_title2name():
    assert title2file_name('The Peripheral', 1, 2) == 'The.Peripheral.S01E02'
    assert title2folder_name('The Peripheral') == 'The.Peripheral'
