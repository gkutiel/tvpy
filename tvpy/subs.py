from abc import ABC, abstractmethod
from typing import Iterable, Tuple


class SubProvider(ABC):
    @abstractmethod
    def get_subs(self, *, imdb_id=None, query=None, lang=None, season=..., episodes=...) -> Iterable[Tuple[int, int, str]]:
        raise NotImplementedError()
