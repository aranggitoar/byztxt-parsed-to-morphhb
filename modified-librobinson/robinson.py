# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Aranggi Toar
# Copyright (C) 2005-2017 Scripture Systems ApS
#
# Made available under the MIT License.
#
# See the file LICENSE in the distribution for details.
#
from __future__ import unicode_literals
import os
import sys
import reader


def read_robinson(directory, suffix, reading_encoding):
    sys.stderr.write("Now reading %s from directory %s\n" %
            (suffix, directory))
    rd = reader.Reader(directory, suffix)
    rd.read_NT(reading_encoding)
    return rd

def run():
    indirectory = os.path.abspath(os.path.join(os.path.dirname(__file__),
        '..', 'src'))
    suffix = "UB5"

    rd = read_robinson(indirectory, suffix,
            reader.read_UMAR_encoding)

    outdir = "./outdir"
        
    print("Now writing %s of %s" % ("JSON", suffix))
    rd.write_SFM(outdir, "json")
    

if __name__ == '__main__':
    run()
