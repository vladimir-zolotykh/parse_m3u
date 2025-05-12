#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> print(parse_m3u(various_pop))
[Song(title='Various - Two Tribes', seconds=236, filename='Various/Frankie Goes To Hollywood/02-Two Tribes.ogg'), \
Song(title='Various - Relax', seconds=237, filename='Various/Frankie Goes To Hollywood/01-Relax.ogg'), \
Song(title='Various - The Power of Love', seconds=330, filename='Various/Frankie Goes To Hollywood/12-The Power of Love.ogg'), \
Song(title='Various - Material Girl', seconds=-1, filename='Various/Madonna/05-Material Girl.ogg'), \
Song(title='The Police - Walking On The Moon', seconds=303, filename='Various/Sting & The Police 1997/06-Walking On The Moon.ogg')]
"""
import io
import re
import enum
from collections import namedtuple

various_pop = """\
#EXTM3U
#EXTINF:236,Various - Two Tribes
Various/Frankie Goes To Hollywood/02-Two Tribes.ogg
#EXTINF:237,Various - Relax
Various/Frankie Goes To Hollywood/01-Relax.ogg
#EXTINF:330,Various - The Power of Love
Various/Frankie Goes To Hollywood/12-The Power of Love.ogg
#EXTINF:-1,Various - Material Girl
Various/Madonna/05-Material Girl.ogg
#EXTINF:303,The Police - Walking On The Moon
Various/Sting & The Police 1997/06-Walking On The Moon.ogg
"""
Song = namedtuple("Song", "title seconds filename")
SONGS_T = list[Song]


class ParseError(Exception):
    pass


def parse_m3u(m3u_str: str) -> SONGS_T:
    State = enum.Enum("State", "HEADER INFO FILENAME")
    songs: list[Song] = []
    HEADER_RE = r"^#EXTM3U"
    INF_RE = r"^#EXTINF:(?P<seconds>-?\d+),(?P<title>[^\n]+)"
    FILENAME_RE = r"^(?P<filename>[^\n]+)"
    with io.StringIO(various_pop) as so:
        state: State = State.HEADER
        for line_no, line in enumerate(so, 1):

            def make_error(msg: str) -> None:
                raise ParseError(msg, line_no, line)

            seconds: int
            title: str
            if state == State.HEADER:
                if not re.match(HEADER_RE, line):
                    make_error("Want HEADER")
                else:
                    state = State.INFO
            elif state == State.INFO:
                m = re.match(INF_RE, line)
                if not m:
                    make_error("Want INFO")
                else:
                    seconds = int(m.group("seconds"))
                    title = m.group("title")
                    state = State.FILENAME
            elif state == state.FILENAME:
                m = re.match(FILENAME_RE, line)
                if not m:
                    make_error("Want FILENAME")
                else:
                    songs.append(Song(title, seconds, m.group("filename")))
                    state = State.INFO
            else:
                # fmt: off
                assert True, (f"{state}: Valid states are HEADER, "
                              f"INFO, FILENAME")
                # fmt: on
        return songs


if __name__ == "__main__":
    import doctest

    doctest.testmod()
