from kind import *
from booknames import *
import reader
import robinsontags
import convert

state_none = 0
state_surface = 1
state_strongs1 = 2
state_strongs2 = 3
state_strongs3 = 4
state_parsing = 5
state_alt_strongs1 = 6
state_alt_strongs2 = 7
state_alt_strongs3 = 8
state_alt_parsing = 9

variant_none = 0
variant_first = 1
variant_second = 2

class Word:
    def __init__(self, monad, encoding):
        self.monad = monad
        self.encoding = encoding
        self.surface = ""
        self.accented_surface = ""
        self.parsing = ""
        self.strongslemma = ""
        self.ANLEXlemma = ""
        self.alt_parsing = ""
        self.Strongs1 = -1
        self.Strongs2 = -1
        self.Strongs3 = -1
        self.alt_Strongs1 = -1
        self.alt_Strongs2 = -1
        self.alt_Strongs3 = -1
        self.altlemma = ""
        self.tag_object = None

    def getStrongs(self):
        lemma = ""
        if self.Strongs1 != -1:
            lemma += str(self.Strongs1)
        if self.Strongs2 != -1:
            lemma += "&" + str(self.Strongs2)
        if self.Strongs3 != -1:
            lemma += "&" + str(self.Strongs3)
        return lemma

    def getAltStrongs(self):
        lemma = ""
        if self.alt_Strongs1 != -1:
            lemma += str(self.alt_Strongs1)
        if self.alt_Strongs2 != -1:
            lemma += "&" + str(self.alt_Strongs2)
        if self.alt_Strongs3 != -1:
            lemma += "&" + str(self.alt_Strongs3)
        return lemma

    def setStrongs(self, strongs):
        if "&" in strongs:
            mylist = strongs.split("&")
            self.Strongs1 = int(mylist[0])
            self.Strongs2 = int(mylist[1])
            if len(mylist) == 3:
                self.Strongs3 = int(mylist[2])
        elif "/" in strongs:
            self.Strongs1 = strongs
        else:
            self.Strongs1 = int(strongs)

    def convert2beta(self, mystr):
        if self.encoding == reader.read_OLB_encoding:
            return convert.OLBtoBETAtranslate(mystr)
        elif self.encoding == reader.read_UMAR_encoding:
            return convert.UMARtoBETAtranslate(mystr)
        else:
            raise Exception("Error: Unknwn self.encoding = %s" % self.encoding)

    def writeSFM(self, f, booknumber, chapter, verse, word_index, monad):
        string = ""

        bookname = book_list("ENGLISH")[int(booknumber) - 1]

        if int(chapter) == 1 and int(verse) == 1 and int(word_index) == 1:
            # Add opening parenteses for the first verse of the Bible
            if bookname == "Matthew":
                string = string + '{"' + bookname + '":[[['
            else:
                string = string + ']]],"' + bookname + '":[[['
        elif int(chapter) > 1 and int(verse) == 1 and int(word_index) == 1:
            string = string + "]],[["
        elif int(verse) == 1 and int(word_index) == 1:
            string = string + ",["
        elif int(verse) > 1 and int(word_index) == 1:
            string = string + "],["
        elif int(word_index) > 1:
            string = string + ","

        string = string + "["

        # For debugging.
        # string = string + "{bn" + str(booknumber) + ",c" + \
        #         str(chapter) + ",v" + str(verse) + ",w" + \
        #         str(word_index) + "}"

        surfaceUTF8 = self.beta2utf8(self.convert2beta(self.surface))

        string = string + '"' + surfaceUTF8 + '"'

        if '&' in self.getStrongs():
            string = string + ',"G' + "&G".join(self.getStrongs().rsplit("&", 1)) + '"'
        else:
            string = string + ',"G' + self.getStrongs() + '"'

        if len(self.parsing) > 0:
            string = string + "," + '"' + self.parsing + '"' + "]"

        # Add closing parentheses for the last verse of the Bible
        if bookname == "Revelation" and int(chapter) == 22 and int(verse) == 21 and int(word_index) == 11:
            string = string + "]]]}"

        # Write into new lines
        #print >>f, string
        # Write into a continuous line
        f.write(string)

    def beta2utf8(self, beta):
        result = ""
        for s in beta.split(" "):
            # Add '\n' at the end to convert final sigma to real final sigma.
            # The '\n' will be stripped out by the conversion
            utf16, remainder = convert.beta2unicodetrie.convert(s+"\n")

            # Convert Unicode string to UTF8
            utf8 = utf16.encode("utf-8")
            
            if remainder != "":
                #raise Exception("UTF8 = '" + utf8 +"'\nbeta = " + beta + "\n, and remainder was not empty, but was: '" + remainder + "'")
                print "UTF8 = '" + utf8 +"'\nbeta = " + beta + "\n, and remainder was not empty, but was: '" + remainder + "'"
            result += utf8 + " "
        return result[0:-1]

    def getSFMReference(self, f, booknumber, chapter, verse, word_index):
        return "\\rf %02d-%03d-%03d-%03d\r" % (int(booknumber), int(chapter), int(verse), int(word_index))


    def parseStrongs(self, strongs):
        """This is necessary because "[tou 3588]" occurs in Romans, and
	qeou 2316> occurs in ByzParsed RE 21:2."""
        return strongs.replace(']', '').replace(">", "")

    def parse(self, index, words):
        """Parses up to the end of this word. Returns the index that points
        one after the end of the word."""

        state = state_none
        LAST_WORD = len(words) - 1
        while True:
            if index > LAST_WORD:
                return index
            # Advance if this is parens.
            # This is such things as (26-61) indicating (I think)
            # that NA27 starts the verse here (26:61).
            elif recognize(words[index]) == kind_parens:
                index += 1
            elif state == state_none:
                # Read surface
                if not recognize(words[index]) == kind_word:
                    raise Exception("Error in words: word[index] is not kind_word:" + str(words[index:]))
                self.surface = words[index]
	
                # Advance index
                index += 1

                state = state_surface
            elif state == state_surface:
                # Try next word
                kind = recognize(words[index])
                if kind == kind_number:
                    self.Strongs1 = int(self.parseStrongs(words[index]))
                    state = state_strongs1
                    # In Romans, the text "[tou 3588]" occurs.
                    if self.surface[0] == '[' and words[index][-1] == ']':
                        self.surface += ']'
                    if words[index][-1] == ">":
                        self.surface += ">"
                    index += 1
                elif kind in [kind_pipe, kind_VAR, kind_END]:
                    return index
                elif kind == kind_word:
                    # We are not doing parsing or variant, so we have the next surface
                    return index
                else:
                    raise Exception("Error in Word.parse: 1: Unknown kind:" + str(kind) + "'" +str(words[index]) + "'")
            elif state == state_strongs1:
                # Try next word
                kind = recognize(words[index])
                if kind == kind_number:
                    self.Strongs2 = int(self.parseStrongs(words[index]))
                    state = state_strongs2
                    index += 1
                elif kind == kind_parsing:
                    if words[index][-1] != "}":
                        raise Exception("Error in words: parsing does not end with }: " + str(words[index:]))
                    state = state_parsing
                    self.parsing = words[index][1:-1] # Strip '{' and '}'
                    index += 1
                else:
                    raise Exception("Error in Word.parse: 2: Unknown kind:" + str(kind) + " '" +str(words[index]) + "', words = " + str(words))
            elif state == state_strongs2:
                kind = recognize(words[index])
                
                # It should be parsing or Strongs3 at this point
                if kind == kind_parsing:
                    if words[index][-1] != "}":
                        raise Exception("Error in words: parsing does not end with }: " + str(words[index:]))
                    state = state_parsing
                    self.parsing = words[index][1:-1] # Strip '{' and '}'
                    index += 1
                elif kind == kind_number:
                    state = state_strongs3
                    self.Strongs3 = self.parseStrongs(words[index])
                    index += 1
                else:
                    raise Exception("Error in Word.parse: 3: Unknown kind: " + str(kind) + "'" +str(words[index]) + "' " + str(words))
            elif state == state_strongs3:
                # Try next word
                kind = recognize(words[index])
                
                # It should be parsing at this point
                if kind == kind_parsing:
                    if words[index][-1] != "}":
                        raise Exception("Error in words: parsing does not end with }: " + str(words[index:]))
                    state = state_parsing
                    self.parsing = words[index][1:-1] # Strip '{' and '}'
                    index += 1
                else:
                    raise Exception("Error in Word.parse: 32: Unknown kind: " + str(kind) + "'" +str(words[index]) + "' " + str(words))
            elif state == state_parsing:
                # So the parsing is read.  The next should either be kind_word
                # or kind_number (but may be state_parsing)

                # If we have gone past the end, return
                if len(words) <= index:
                    return index

                # Try next word
                kind = recognize(words[index])
                if kind == kind_number:
                    self.alt_Strongs1 = int(words[index])
                    state = state_alt_strongs1
                    index += 1
                elif kind == kind_word or kind in [kind_pipe, kind_VAR, kind_END, kind_parens, kind_verse]:
                    # If this is a kind_word, kind_pipe or kind_parens,
                    # we should return now.
                    # If it is a kind_word or a kind_parens, the next word will
                    # take care of it.
                    # If it is a kind_pipe, the verse will take care of it.
                    return index
                elif kind == kind_parsing:
                    if words[index][-1] != "}":
                        raise Exception("Error in words: parsing does not end with }: " + str(words[index:]))
                    state = state_alt_parsing
                    self.alt_parsing = words[index][1:-1] # Strip '{' and '}'
                    index += 1
                else:
                    raise Exception("Error in Word.parse: 5: Unknown kind:" + str(kind) + "'" +str(words[index]) + "'")
            elif state == state_alt_strongs1:
                # Try next word
                kind = recognize(words[index])
                if kind == kind_number:
                    self.alt_Strongs2 = int(words[index])
                    state = state_alt_strongs2
                    index += 1
                elif kind == kind_parsing:
                    if words[index][-1] != "}":
                        raise Exception("Error in words: parsing does not end with }: " + str(words[index:]))
                    state = state_alt_parsing
                    self.alt_parsing = words[index][1:-1] # Strip '{' and '}'
                    index += 1
                else:
                    raise Exception("Error in Word.parse: 7: Unknown kind: " + str(kind) + " '" +str(words[index]) +"'" + "\nwords = '%s'" % words)
            elif state == state_alt_strongs2:
                # Try next word
                kind = recognize(words[index])
                # It should be parsing or number at this point
                if kind == kind_parsing:
                    if words[index][-1] != "}":
                        raise Exception("Error in words: parsing does not end with }: " + str(words[index:]))
                    state = state_alt_parsing
                    self.alt_parsing = words[index][1:-1] # Strip '{' and '}'
                    index += 1
                elif kind == kind_number:
                    self.alt_Strongs3 = int(words[index])
                    state = state_alt_strongs3
                    index += 1
                else:
                    raise Exception("Error in Word.parse: 8: Unknown kind:" + str(kind) + "'" +str(words[index]) + "'")
            elif state == state_alt_strongs3:
                # Try next word
                kind = recognize(words[index])
                # It should be parsing at this point
                if kind == kind_parsing:
                    if words[index][-1] != "}":
                        raise Exception("Error in words: parsing does not end with }: " + str(words[index:]))
                    state = state_alt_parsing
                    self.alt_parsing = words[index][1:-1] # Strip '{' and '}'
                    index += 1
                else:
                    raise Exception("Error in Word.parse: 9: Unknown kind:" + str(kind) + "'" +str(words[index]) + "'")
            elif state == state_alt_parsing:
                # If we have gone past the end, return
                if len(words) <= index:
                    return index
                
                # Otherwise, the next should be a word.
                kind = recognize(words[index])
                if kind == kind_word or kind in [kind_parens, kind_pipe, kind_VAR, kind_END, kind_verse]:
                    return index
                else:
                    raise Exception("Error in Word.parse: 10: Unknown kind:" + str(kind) + "'" +str(words[index]) + "'")
