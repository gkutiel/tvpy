from rich.console import Console
from rich.theme import Theme

cls = Console(theme=Theme({
    'warn': 'bold orange1',
    'err': 'bold red'}))
