import string
import sys
from verse import *
from chapter import *
from kind import *
import word
from booknames import *

myverseletters = ["a", "b", "c", "d", "e", "f", "g"]

verse_re = re.compile(r'\(?(\d+):(\d+)\)?')

class Book:
    def __init__(self, filename, encoding):
        self.filename = filename
        self.parse_filename(filename)
        self.chapter = 0
        self.ch = 0
        self.vs = 0
        self.verse = -1
        self.chapters = []
        self.verses = []
        self.verse_dict = {}
        self.variant = variant_none
        self.encoding = encoding

    def parse_filename(self, filename):
        path_ingridients = filename.split("/")
        bk = path_ingridients[-1].split(".")[0].upper()
        self.OLB_bookname = bk
        try:
            (self.bookname, self.booknumber) = OLB2More[bk]
        except:
            print "Unknown bookname: '%s'" % bk
            sys.exit()

    def read(self, start_monad):
        self.start_monad = start_monad
        self.chapter_first_monad = start_monad
        self.end_monad = start_monad - 1
        f = self.open_file()
        lines = f.readlines()
        f.close()
        self.parse_lines(lines)
        return self.end_monad

        

    def open_file(self):
        f = open(self.filename, "r")
        return f
            
    def parse_lines(self, lines):
        all = "\n".join(lines)

        if self.OLB_bookname == "MT":
            # Occurs in ByzParsed Matthew
            all = all.replace("23:13 (23:14)", "23:13").replace("23:14 (23:13)", "23:14")
        elif self.OLB_bookname == "RE":
            # Revelation 17:8 was treated as it was because Dr. Robinson
            # uses Online Bible for DOS himself, and 
            # OLB for DOS has a limit on how many words can be in a verse.
            # This one is just particularly long, and breaks the barrier
            # on OLB for DOS.
            
            # All other (ch:vs) should probably be ignored.
            all = all.replace("(17:8)", "$@!@$").replace("17:8", "").replace("$@!@$", " 17:8 ")

        words = []

        mystack = []

        chvs = ""

        for w in all.split():
            if recognize(w) in [kind_verse, kind_parens]:
                    chvs = w

            if w == "M5:":
                mystack.append(":M5")
            elif w == "M6:":
                mystack.append(":M6")
            elif w == "VAR:":
                mystack.append(":END")
            elif w in [":M5", ":M6", ":END"]:
                end_of_stack = mystack[-1]
                mystack = mystack[:-1]
                if w != end_of_stack:
                    print "UP310: %s end_of_stack = '%s', w = '%s', line_words = %s" % (self.bookname, end_of_stack, w, line_words)
                    #
                    # NOTE: They are not balanced in the text, 
                    # so let's not try...
                    #
                    raise "Error! M5/M6/VAR-END not balanced..."
                    pass
            else:
                if len(mystack) == 0:
                    words.append(w)
                else:
                    pass

        overall_text = " ".join(words)

        if text_variant_strongs_parsing_re.search(overall_text) != None:
            overall_text = text_variant_strongs_parsing_re.sub(r'| \1\3 | \2\3 | ', overall_text)

        if text_strongs_varparsing_varparsing_re.search(overall_text) != None:
            overall_text = text_strongs_varparsing_varparsing_re.sub(r'| \1\2 | \1\3 | ', overall_text)

        if text_strongs_vartext_varstrongs_parsing.search(overall_text) != None:
            overall_text = text_strongs_vartext_varstrongs_parsing.sub(r'| \1 \3 | \2 \3 | ', overall_text)
            

        # In Romans 16:27 of WH, we find the line ends with "{HEB}|".
        # We need this to be "{HEB} |".
        overall_text = overall_text.replace("}|", "} |")

        words = []

        for wd in overall_text.split():
            if wd == "|":
                if self.variant == variant_none:
                    self.variant = variant_first
                elif self.variant == variant_first:
                    self.variant = variant_second
                elif self.variant == variant_second:
                    self.variant = variant_none
                else:
                    raise Exception("Error: Unknown self.variant: %s" % self.variant)
            elif recognize(wd) == kind_parens:
                # Remove parens altogether
                pass
            else:
                if self.variant == variant_none:
                    words.append(wd)
                elif self.variant == variant_first:
                        pass
                elif self.variant == variant_second:
                        pass
                else:
                    raise Exception("Error: Unknown variant: %s" % self.variant)
            

        verses = [] # List of lists of strings

        for wd in words:
            if recognize(wd) == kind_verse:
                (ch,vs) = verse_re.findall(wd)[0]
                verses.append([])
                self.ch = ch
                self.vs = vs
                verses[-1].append(wd)
            else:
                verses[-1].append(wd)
                    
                        

        LAST_VERSE_INDEX = len(verses) - 1

        for index in xrange(0, len(verses)):
            bIsLastVerseOfBook = index == LAST_VERSE_INDEX
            self.parseVerse(verses[index], self.end_monad + 1, bIsLastVerseOfBook)

    def parseVerse(self, verse_lines, first_monad, is_last_verse_of_book):
        verse = Verse(verse_lines, self.bookname, self.booknumber, self.encoding)
        self.verses.append(verse)
        chapter_end = self.end_monad
        self.end_monad = verse.parse(first_monad)
        chapter = verse.chapter
        if is_last_verse_of_book:
            chapter_end = self.end_monad
            self.parseChapter(self.chapter, chapter_end)
        elif self.chapter <> chapter:
            if self.chapter <> 0:
                self.parseChapter(self.chapter, chapter_end)
            self.chapter = chapter


    def parseChapter(self, chapter, chapter_end_monad):
        ch = Chapter(self.chapter_first_monad, chapter_end_monad, chapter, self.bookname)
        self.chapters.append(ch)
        self.chapter_first_monad = chapter_end_monad + 1

                
    def writeSFM(self, f, cur_monad):
        for v in self.verses:
            cur_monad = v.writeSFM(f, cur_monad)
        return cur_monad

    def getWords(self):
        result = []
        for v in self.verses:
            result.extend(v.getWords())
        return result
