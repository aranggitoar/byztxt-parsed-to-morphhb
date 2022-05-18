import string
import re
from word import *
from kind import *
import reader

 
text_variant_strongs_parsing_re= re.compile(r'\|\s+([a-z\[\]]+)\s+\|\s+([a-z\[\]]+)\s+\|([0-9\s]+\{[A-Z0-9\-]+\})\s*')

text_strongs_varparsing_varparsing_re = re.compile(r'(\s+[a-z\[\]]+\s+[0-9]+\s+)\|\s+(\{[A-Z0-9\-]+\})\s+\|\s+(\{[A-Z0-9\-]+\})\s+')

text_strongs_vartext_varstrongs_parsing = re.compile(r'\|\s+([a-z\[\]]+\s+[0-9]+)\s+\|\s+([a-z\[\]]+\s+[0-9]+)\s+\|\s+(\{[A-Z0-9\-]+\})\s+')



class Verse:
    def __init__(self, verse_lines, bookname, booknumber, encoding):
        self.chapter = self.verse = 0
        self.bookname = bookname
        self.booknumber = booknumber
        self.encoding = encoding
        self.first_monad = 0
        self.last_monad = 0
        self.current_monad = 0
        self.verse_lines = verse_lines
        self.variant = variant_none
        self.variant_first_monad = 0
        self.words = []

    def getWords(self):
        return self.words

    def parse_chapter_verse(self, cv):
        if cv[0] == "[":
            if self.bookname == "Mark":
                self.chapter = 16
                self.verse = 9
            else:
                raise Exception("Verse.parse_chapter_verse: Unknown bookname: " + self.bookname)
        else:
            chap_ver_arr = cv.split(":")
            self.chapter = chap_ver_arr[0]
            self.verse = chap_ver_arr[1]

    def parse(self, first_monad):
        # Set member variables
        self.first_monad = self.last_monad = first_monad
        self.current_monad = first_monad

        overall_line = "\n".join(self.verse_lines)

        line_words = overall_line.split()
	
        # Parse chapter/verse
        try:
            self.parse_chapter_verse(line_words[0])
        except:
            print 
            raise Exception("Error parsing verse, first element of: '%s'" % line_words)

        # If this is, e.g., the shorter ending of Mark,
        # start at index 0. Otherwise, start at index 1
        if line_words[0][0] == "[":
            index = 0
        else:
            index = 1

        # Strip parens-words.
        # This is things like "(26-61)", indicating that NA27
        # starts the verse here.
        line_word_candidates = []
        for w in line_words[index:]:
            kind = recognize(w)
            if kind == kind_unknown:
                raise Exception("Error in Verse.parse: Unknown word kind: '" + w + "'")
            else:
                line_word_candidates.append(w)

        # Parse rest of words
        self.parse_words(line_word_candidates)

        if self.last_monad < first_monad:
            print "Error in verse: ", self.bookname, self.chapter, self.verse

        return self.last_monad

    def parse_words(self, words):
        index = 0
        while index < len(words):
            w = Word(self.current_monad, self.encoding)
            index = w.parse(index, words)
            self.words.append(w)
            self.current_monad += 1

    def writeSFM(self, f, cur_monad):
        word_index = 1
        for w in self.words:
            w.writeSFM(f, self.booknumber, self.chapter, self.verse, word_index, cur_monad)
            word_index += 1
            cur_monad += 1
        return cur_monad
