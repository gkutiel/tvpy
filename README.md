# 📺 TvPy 
Command line tv show manager.

[![asciicast](https://asciinema.org/a/hQeLoj8lYcGtJvErlTWifdmfo.svg)](https://asciinema.org/a/hQeLoj8lYcGtJvErlTWifdmfo)

## Installation
```shell
> pip install tvpy
```

<!-- ## Get an API Key
You need to get an API key from [TMDB](https://www.themoviedb.org/settings/api) and save it as `key.txt` in your working directory. -->

## Usage
```shell
> mkdir Carnival.Row 
> tvpy Carnival.Row 
```

## Other commands

Download information from TMDB:
```shell
> mkdir Carnival.Row 
> tv-json Carnival.Row
```

Display information about a tv show:
```shell
> mkdir Carnival.Row 
> tv-info Carnival.Row
```

Download a tv show:
```shell
> mkdir Carnival.Row 
> tv-down Carnival.Row
```

Download (Hebrew) subtitles for a tv show:
```shell
> mkdir Carnival.Row 
> tv-subs Carnival.Row
```

Rename files to match the pattern `<title>.S<season>E<episode>.<ext>`
```shell
> mkdir Carnival.Row 
> tv-renm Carnival.Row
```

| :exclamation:  Danger   |
|-------------------------|

Remove unused files
```shell
> mkdir Carnival.Row 
> tv-klyn Carnival.Row
```


