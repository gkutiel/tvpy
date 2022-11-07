# 📺📺 TvPy 🥧🥧

Manage TV shows from the terminal.

![demo](https://github.com/gkutiel/tvpy/raw/1a6686c863a74e1c8dd66b4f9087de2f8a349c61/demo.gif)

## Installation
```shell
> pip install tvpy
```

## Usage
```shell
> mkdir The.Peripheral 
> tvpy The.Peripheral 
```

## Other commands
Download information from TMDB:
```shell
> mkdir The.Peripheral 
> tv-json The.Peripheral
```

Display information about a tv show:
```shell
> mkdir The.Peripheral 
> tv-info The.Peripheral
```

Download a tv show:
```shell
> mkdir The.Peripheral 
> tv-download The.Peripheral
```

Download subtitles for a tv show:
```shell
> mkdir The.Peripheral 
> tv-subs The.Peripheral
```

Rename files to match the pattern `<title>.S<season>E<episode>.<ext>`
```shell
> mkdir The.Peripheral 
> tv-rename The.Peripheral
```

| ⚠️ Danger |
|----------|
Remove unused files
```shell
> mkdir The.Peripheral 
> tv-clean The.Peripheral
```

## Follow
TvPy allows you to follow lists of tv shows.
A list is a simple text file where each row contains a name of a tv show.
Here is an example:
```shell
> echo "\
      The.Peripheral
      Andor" > SciFi.txt
> tv-follow SciFi.txt
> tvpy
```
This will keep all the tv shows you follow uptodate.
You can follow as many lists as you wish.

|💡 You can easily share lists by putting them in a Dropbox folder or similar.|
|-----------------------------------------------------------------------------|

## Configuration
A small `.tvpy.toml` configuration file is located at your home directory.
Its content looks like that:
```toml
TVPY_HOME = "/home/me/tvpy"
follow = []
```
The value of `TVPY_HOME` is where `tvpy` downloads all your shows.
The value of `follow` is a list of lists you are following.