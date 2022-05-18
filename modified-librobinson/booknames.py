# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 by Aranggi Toar
# Copyright (C) 2005-2017 Scripture Systems ApS
#
# Made available under the MIT License.
#
# See the file LICENSE in the distribution for details.
#


book_lists = {
    "OLB" : ["MT", "MR", "LU", "JOH", "AC", "RO", "1CO", "2CO", "GA",
        "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI", "TIT",
        "PHM", "HEB", "JAS", "1PE", "2PE", "1JO", "2JO", "3JO",
        "JUDE", "RE"],
    
    "UBS" : ["mat", "mrk", "luk", "jhn", "act", "rom", "1co", "2co",
        "gal", "eph", "php", "col", "1th", "2th", "1ti", "2ti",
        "tit", "phm", "heb", "jas", "1pe", "2pe", "1jn", "2jn",
        "3jn", "jud", "rev"],

    "ENGLISH" : ["Matthew", "Mark", "Luke", "John", "Acts", "Romans",
        "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
        "Philippians", "Colossians", "1 Thessalonians",
        "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus",
        "Philemon", "Hebrew", "James", "1 Peter", "2 Peter",
        "1 John", "2 John", "3 John", "Jude", "Revelation"],
}

OLB2More = {
    "MT"  : ("Matthew", 1),
    "MR"  : ("Mark", 2),
    "LU"  : ("Luke", 3),
    "JOH" : ("John", 4),
    "AC"  : ("Acts", 5),
    "RO"  : ("Romans", 6),
    "1CO" : ("I_Corinthians", 7),
    "2CO" : ("II_Corinthians", 8),
    "GA"  : ("Galatians", 9),
    "EPH" : ("Ephesians", 10),
    "PHP" : ("Philippians", 11),
    "COL" : ("Colossians", 12),
    "1TH" : ("I_Thessalonians", 13),
    "2TH" : ("II_Thessalonians", 14),
    "1TI" : ("I_Timothy", 15),
    "2TI" : ("II_Timothy", 16),
    "TIT" : ("Titus", 17),
    "PHM" : ("Philemon", 18),
    "HEB" : ("Hebrews", 19),
    "JAS" : ("James", 20),
    "1PE" : ("I_Peter", 21),
    "2PE" : ("II_Peter", 22),
    "1JO" : ("I_John", 23),
    "2JO" : ("II_John", 24),
    "3JO" : ("III_John", 25),
    "JUDE": ("Jude", 26),
    "RE"  : ("Revelation", 27)
}


def book_list(scheme):
    return book_lists[scheme]
