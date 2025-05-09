#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
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


def parse_m3u_fh(fh: TextIO) -> pp.ParseResults:
    return m3u_bnf().parse_file(fh)


def parse_m3u_file(filename: str | Path) -> pp.ParseResults:
    with open(filename) as fh:
        return parse_m3u_fh(fh)


if __name__ == "__main__":
    print(parse_m3u_file(Path("Various-Pop.m3u")))
