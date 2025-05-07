#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> parse_str("\
#EXTM3U\\n\
#EXTINF:236,Various - Two Tribes\\n\
Various/Frankie Goes To Hollywood/02-Two Tribes.ogg\\n\
#EXTINF:237,Various - Relax\\n\
Various/Frankie Goes To Hollywood/01-Relax.ogg\\n\
#EXTINF:330,Various - The Power of Love\\n\
Various/Frankie Goes To Hollywood/12-The Power of Love.ogg\\n\
#EXTINF:-1,Various - Material Girl\\n\
Various/Madonna/05-Material Girl.ogg\\n\
#EXTINF:303,The Police - Walking On The Moon\\n\
Various/Sting & The Police 1997/06-Walking On The Moon.ogg\\n\
")
[Song(title='Various - Two Tribes', seconds=236, filename='Various/Frankie Goes To Hollywood/02-Two Tribes.ogg'), Song(title='Various - Relax', seconds=237, filename='Various/Frankie Goes To Hollywood/01-Relax.ogg'), Song(title='Various - The Power of Love', seconds=330, filename='Various/Frankie Goes To Hollywood/12-The Power of Love.ogg'), Song(title='Various - Material Girl', seconds=-1, filename='Various/Madonna/05-Material Girl.ogg'), Song(title='The Police - Walking On The Moon', seconds=303, filename='Various/Sting & The Police 1997/06-Walking On The Moon.ogg')]

"""

import io
from collections import namedtuple
import re
from enum import Enum
from pprint import pprint

State = Enum("State", ["WANT_INFO", "WANT_FILENAME"])
Song = namedtuple("Song", "title seconds filename")
PLAYLIST = list[Song]


def parse_m3u(fh: io.TextIOBase) -> PLAYLIST:
    songs: PLAYLIST = []
    if fh.readline() != "#EXTM3U\n":
        print("This is not a .m3u file")
        return songs
    INFO_RE = re.compile(r"#EXTINF:(?P<seconds>-?\d+),(?P<title>.+)")
    state: State = State.WANT_INFO
    for lino, line in enumerate(fh, start=2):
        line = line.strip()
        if not line:
            continue
        if state == State.WANT_INFO:
            info = INFO_RE.match(line)
            if info:
                title = info.group("title")
                seconds = int(info.group("seconds"))
                state = State.WANT_FILENAME
            else:
                print("Failed to parse line {0}: {1}".format(lino, line))
        elif state == State.WANT_FILENAME:
            songs.append(Song(title, seconds, line))
            title = seconds = None
            state = State.WANT_INFO
    return songs


def parse_string(init_str: str) -> PLAYLIST:
    with io.StringIO(init_str) as so:
        return parse_m3u(so)


def parse_file(filename: str = "Various-Pop.m3u") -> PLAYLIST:
    with open(filename) as fh:
        return parse_m3u(fh)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

from collections import namedtuple
import re
from enum import Enum
from pprint import pprint

State = Enum("State", ["WANT_INFO", "WANT_FILENAME"])
Song = namedtuple("Song", "title seconds filename")
PLAYLIST = list[Song]


def parse_m3u(fh: io.TextIOBase) -> PLAYLIST:
    songs: PLAYLIST = []
    if fh.readline() != "#EXTM3U\n":
        print("This is not a .m3u file")
        return songs
    INFO_RE = re.compile(r"#EXTINF:(?P<seconds>-?\d+),(?P<title>.+)")
    state: State = State.WANT_INFO
    for lino, line in enumerate(fh, start=2):
        line = line.strip()
        if not line:
            continue
        if state == State.WANT_INFO:
            info = INFO_RE.match(line)
            if info:
                title = info.group("title")
                seconds = int(info.group("seconds"))
                state = State.WANT_FILENAME
            else:
                print("Failed to parse line {0}: {1}".format(lino, line))
        elif state == State.WANT_FILENAME:
            songs.append(Song(title, seconds, line))
            title = seconds = None
            state = State.WANT_INFO
    return songs


def parse_file(filename: str = "Various-Pop.m3u") -> PLAYLIST:
    with open(filename) as fh:
        return parse_m3u(fh)


if __name__ == "__main__":
    with open("Various-Pop.m3u") as fh:
        pprint(parse_file())
