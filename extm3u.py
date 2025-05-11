#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import io
import re

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
    with io.StringIO(various_pop) as so:
        for line_no, line in enumerate(so, 1):
            if line_no == 1 and not re.match(r"^#EXTM3U", line):
                raise ParseError()
            print(line, end="")
