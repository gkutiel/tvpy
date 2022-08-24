from pathlib import Path


def scan(root):
    root = Path(root)
    names = [x.name for x in root.iterdir() if x.is_dir()]
    return names
