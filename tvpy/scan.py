from pathlib import Path


def folders(root):
    return [x for x in Path(root).iterdir() if x.is_dir()]
