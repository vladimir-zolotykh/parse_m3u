#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
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


if __name__ == "__main__":
    with open("Various-Pop.m3u") as fh:
        d = m3u_bnf().parse_file(fh)
    print(d)
