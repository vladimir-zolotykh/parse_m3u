#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> parse_m3u_file(Path("Various-Pop.m3u"))
ParseResults([ParseResults(['236', 'Various - Two Tribes', 'Various/Frankie Goes To Hollywood/02-Two Tribes.ogg'], {'seconds': '236', 'title': 'Various - Two Tribes', 'filename': 'Various/Frankie Goes To Hollywood/02-Two Tribes.ogg'}), ParseResults(['237', 'Various - Relax', 'Various/Frankie Goes To Hollywood/01-Relax.ogg'], {'seconds': '237', 'title': 'Various - Relax', 'filename': 'Various/Frankie Goes To Hollywood/01-Relax.ogg'}), ParseResults(['330', 'Various - The Power of Love', 'Various/Frankie Goes To Hollywood/12-The Power of Love.ogg'], {'seconds': '330', 'title': 'Various - The Power of Love', 'filename': 'Various/Frankie Goes To Hollywood/12-The Power of Love.ogg'}), ParseResults(['-1', 'Various - Material Girl', 'Various/Madonna/05-Material Girl.ogg'], {'seconds': '-1', 'title': 'Various - Material Girl', 'filename': 'Various/Madonna/05-Material Girl.ogg'}), ParseResults(['303', 'The Police - Walking On The Moon', 'Various/Sting & The Police 1997/06-Walking On The Moon.ogg'], {'seconds': '303', 'title': 'The Police - Walking On The Moon', 'filename': 'Various/Sting & The Police 1997/06-Walking On The Moon.ogg'})], {})
"""
from typing import TextIO
from pathlib import Path
import pyparsing as pp


def m3u_bnf() -> pp.core.ParserElement:
    hdr = pp.Suppress("#EXTM3U")
    filename = pp.restOfLine.set_results_name("filename")
    title = pp.restOfLine.set_results_name("title")
    seconds = pp.Regex(r"-?\d+").set_results_name("seconds")
    info = pp.Suppress("#EXTINF:") + seconds + pp.Suppress(",") + title
    nl = pp.LineEnd().suppress()
    entry = pp.Group(info + nl + filename) + nl
    m3u = hdr + nl + pp.OneOrMore(entry)
    return m3u


def _parse_m3u_fh(fh: TextIO) -> pp.ParseResults:
    return m3u_bnf().parse_file(fh)


def parse_m3u_file(filename: str | Path) -> pp.ParseResults:
    with open(filename) as fh:
        return _parse_m3u_fh(fh)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
