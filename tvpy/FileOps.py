from abc import ABC, abstractmethod
from pathlib import Path
from typing import cast
from urllib.parse import ParseResult, urlparse, urlunparse


class Folder(ABC):
    @abstractmethod
    def glob(self, pattern: str): pass


class FolderPath(Folder):
    def __init__(self, path: Path):
        assert path.is_dir()
        self.path = path

    def glob(self, pattern: str):
        return (FolderPath(p) for p in self.path.glob(pattern))


class FolderUrl(Folder):
    def __init__(self, url: ParseResult):
        assert not url.params and not url.query and not url.fragment
        self.url = urlunparse(url)

    def glob(self, pattern: str): pass


def cp(src: Folder, dst: Folder): pass


def folder(path: str | Path | ParseResult):
    if type(path) == str:
        src_url = urlparse(str(path))
        if src_url.scheme:
            return FolderUrl(src_url)

    return FolderPath(Path(cast(str | Path, path)))
