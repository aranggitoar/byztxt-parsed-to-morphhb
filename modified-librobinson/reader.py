# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Benih Yang Baik
# Copyright (C) 2005-2017 Scripture Systems ApS
#
# Made available under the MIT License.
#
# See the file LICENSE in the distribution for details.
#
from __future__ import unicode_literals, print_function
import os
import book
from kind import *
from word import *
from booknames import *

# Old OLB encoding
read_OLB_encoding = 0
# with updates from MAR after 2013-08-02.
read_UMAR_encoding = 1

book_list_OLB = ["MT", "MR", "LU", "JOH", "AC", "RO", "1CO", "2CO",
                 "GA", "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI",
                 "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JO", "2JO", "3JO",
                 "JUDE", "RE"]



class Reader:
    def __init__(self, indir, suffix):
        self.current_monad = 1
        self.suffix = suffix
        self.indir = indir
        self.books = []
        self.lexicon = None
        self.encoding = read_OLB_encoding # default

    def read_NT(self, encoding):
        self.encoding = encoding
        for bkname in book_list("OLB"):
            self.read_book(bkname)

    def read_MT(self):
        self.encoding = encoding
        self.read_book('MT')

    def write_SFM(self, outdir, suffix):
        filename = os.path.join(outdir, "byzparsed.json")
        content = ""
        if os.path.exists(filename):
            os.remove(filename)
        cur_monad = 1
        for index in range(0,27):
            gdb_bookname = book_list("UBS")[index]
            # Write Bible book by Bible book
            #cur_monad = self.writeBookAsSFM(os.path.join(outdir,
            #    "%s.%s" % (gdb_bookname, suffix)), self.books[index], cur_monad)
            cur_monad = self.writeBookAsSFM(filename,
                    self.books[index], cur_monad, content)

    def writeBookAsSFM(self, filename, book, cur_monad, content):
        f = open(filename, "a")
        cur_monad = book.writeSFM(f, cur_monad)
        f.close()
        return cur_monad

    def read_book(self, bookname):
        if self.suffix == "":
            print(bookname)
            filename = self.indir + "/" + bookname
        else:
            print(bookname + "." + self.suffix)
            filename = self.indir + "/" + bookname + "." + self.suffix
        this_book = book.Book(filename, self.encoding)
        self.books.append(this_book)
        self.current_monad = this_book.read(self.current_monad)

    def getBook(self, index):
        return self.books[index]
