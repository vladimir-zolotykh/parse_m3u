#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import io
from collections import namedtuple
import re


Song = namedtuple("Song", "title seconds filename")
PLAYLIST = list[Song]


def parse_m3u(fh: io.TextIOBase) -> PLAYLIST:
    songs: PLAYLIST = []
    if fh.readline() != "#EXTM3U\n":
        print("This is not a .m3u file")
        return songs
    INFO_RE = re.compile(r"#EXTINF:(?P<seconds>-?\d+),(?P<title>.+)")
    WANT_INFO, WANT_FILENAME = range(2)
    state = WANT_INFO
    for lino, line in enumerate(fh, start=2):
        line = line.strip()
        if not line:
            continue
        if state == WANT_INFO:
            info = INFO_RE.match(line)
            if info:
                title = info.group("title")
                seconds = int(info.group("seconds"))
                state = WANT_FILENAME
            else:
                print("Failed to parse line {0}: {1}".format(lino, line))
        elif state == WANT_FILENAME:
            songs.append(Song(title, seconds, line))
            title = seconds = None
            state = WANT_INFO
    return songs


def parse_file(filename: str = "Various-Pop.m3u") -> PLAYLIST:
    with open(filename) as fh:
        return parse_m3u(fh)


if __name__ == "__main__":
    with open("Various-Pop.m3u") as fh:
        print(parse_file())
