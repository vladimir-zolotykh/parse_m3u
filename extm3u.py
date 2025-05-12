#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
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


class ParseError(Exception):
    pass


if __name__ == "__main__":
    State = enum.Enum("State", "HEADER INFO FILENAME")
    Song = namedtuple("Song", "title length filename")
    songs: list[Song] = []
    with io.StringIO(various_pop) as so:
        state: State = State.HEADER
        for line_no, line in enumerate(so, 1):

            def make_error(msg: str) -> None:
                raise ParseError(msg, line_no, line)

            length: int = 0
            title: str = ""
            filename: str = ""
            if state == State.HEADER:
                if not re.match(r"^#EXTM3U", line):
                    make_error("Want HEADER")
                else:
                    state = State.INFO
            elif state == State.INFO:
                m = re.match(r"^#EXTINF:(?P<seconds>-?\d+),(?P<title>[^\n]+)", line)
                if not m:
                    make_error("Want INFO")
                else:
                    seconds = int(m.group("seconds"))
                    title = m.group("title")
                    state = State.FILENAME
            elif state == state.FILENAME:
                m = re.match(r"^(?P<filename>[^\n]+)", line)
                if not m:
                    make_error("Want FILENAME")
                else:
                    songs.append(Song(title, length, m.group("filename")))
                    state = State.INFO
            else:
                assert True, f"{state}: Valid states are HEADER, INFO, FILENAME"
        print(songs)
