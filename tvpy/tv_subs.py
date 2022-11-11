from pathlib import Path

from PTN import parse
from rich.status import Status

from tvpy.addic7ed import Addic7ed
from tvpy.config import get_lang
from tvpy.console import cls
from tvpy.tv_tmdb import load_tvpy
from tvpy.util import done, existing_episodes, files_subs, title2file_name
from tvpy.wizdom import Wizdom


def existing_subs(folder):
    res = [parse(f.name) for f in files_subs(folder)]
    return {(e['season'], e['episode']) for e in res}


def tv_subs(folder):
    missing_subs = existing_episodes(folder) - existing_subs(folder)
    if not missing_subs:
        done()
        return

    info = load_tvpy(folder)
    title = info['name']
    lang = get_lang()
    provider = Wizdom() if lang == 'Hebrew' else Addic7ed()

    with Status(f'[info]Downloading subtitles...', console=cls) as status:
        srts = provider.get_subs(
            imdb_id=info['imdb_id'],
            query=title,
            lang=lang,
            episodes=missing_subs)

        for s, e, srt in srts:
            path = Path(folder) / f'{title2file_name(title, s, e)}.srt'
            cls.print(f':clapper: [success]{path}')
            with open(path, 'wb') as f:
                f.write(srt)

    done()
