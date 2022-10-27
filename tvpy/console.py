from rich.console import Console
from rich.style import Style
from rich.theme import Theme

info = Style.parse('dim cyan')
warn = Style.parse('orange1')
err = Style.parse('bold red')
success = Style.parse('green')

cls = Console(
    record=True,
    theme=Theme({
        'info': info,
        'warn': warn,
        'err': err,
        'success': success}))
