from abc import ABC, abstractmethod
from typing import Iterable, Set, Tuple


class SubProvider(ABC):
    @abstractmethod
    def get_subs(self, *, imdb_id=None, query=None, lang=None, episodes: Set[Tuple[int, int]] = ...) -> Iterable[Tuple[int, int, str]]:
        raise NotImplementedError()
