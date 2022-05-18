# -*- coding: utf-8 -*-
# beta2GalatiaAndUnicode.py
#
# Version 2004-11-23 with changes by ulrikp 2005-03-19 and changes by
# Aranggi Toar 2022-05-18
#
# James Tauber
# http://jtauber.com/
#
# You are free to redistribute this, but please inform me of any errors
#
#
# Modified by Ulrik Sandborg-Petersen to do BETA to SIL Galatia as
# well as a number of other encodings.
#
# Ulrik has a website here, where contact details can be found:
# http://ulrikp.org
#
# SIL Galatia is a beautiful Greek font, freely available here:
# http://http://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&item_id=SILGrk_home
#
# Ulrik Sandborg-Petersen makes his changes available under the same
# conditions as James Tauber did above.
#
#
# Modified by Aranggi Toar to remove uneccessary code.
#
# Aranggi Toar makes his changes available under the same conditions
# as James Tauber did above.
#
#
# USAGE:
#
# trie = beta2unicodeTrie()
# beta = "LO/GOS\n";
# unicode, remainder = trie.convert(beta)
#
# - to get final sigma, string must end in \n
# - remainder will contain rest of beta if not all can be converted
from __future__ import unicode_literals, print_function

import string
import re
import sys


#
# From:
# https://stackoverflow.com/questions/6628306/attributeerror-module-object-has-no-attribute-maketrans
#
try:
    maketrans = ''.maketrans
except AttributeError:
    # fallback for Python 2
    from string import maketrans


class Trie:
    def __init__(self):
        self.root = [None, {}]

    def add(self, key, value):
        curr_node = self.root
        for ch in key:
            curr_node = curr_node[1].setdefault(ch, [None, {}])
        curr_node[0] = value

    def find(self, key):
        curr_node = self.root
        for ch in key:
            try:
                curr_node = curr_node[1][ch]
            except KeyError:
                return None
        return curr_node[0]

    def findp(self, key):
        curr_node = self.root
        remainder = key
        for ch in key:
            try:
                curr_node = curr_node[1][ch]
            except KeyError:
                return (curr_node[0], remainder)
            remainder = remainder[1:]
        return (curr_node[0], remainder)

    def convert(self, keystring):
        valuestring = ""
        key = keystring
        while key:
            value, key = self.findp(key)
            if not value:
                return (valuestring, key)
            valuestring += value
        return (valuestring, key)

def beta2unicodeTrie():
    t = Trie()

    t.add("%2",      "\u002a") # Asterisk
    t.add("%13",     "\u2021") # Double Dagger
    t.add("%30",     "\u02bc") # Modifier Letter Apostrophe
    t.add("\"",      "\u201c")
    t.add("*A",      "\u0391")
    t.add("*B",      "\u0392")
    t.add("*G",      "\u0393")
    t.add("*D",      "\u0394")
    t.add("*E",      "\u0395")
    t.add("*Z",      "\u0396")
    t.add("*H",      "\u0397")
    t.add("*Q",      "\u0398")
    t.add("*I",      "\u0399")
    t.add("*K",      "\u039A")
    t.add("*L",      "\u039B")
    t.add("*M",      "\u039C")
    t.add("*N",      "\u039D")
    t.add("*C",      "\u039E")
    t.add("*O",      "\u039F")
    t.add("*P",      "\u03A0")
    t.add("*R",      "\u03A1")
    t.add("*S",      "\u03A3")
    t.add("*T",      "\u03A4")
    t.add("*U",      "\u03A5")
    t.add("*F",      "\u03A6")
    t.add("*X",      "\u03A7")
    t.add("*Y",      "\u03A8")
    t.add("*W",      "\u03A9")

    t.add("A",      "\u03B1")
    t.add("B",      "\u03B2")
    t.add("G",      "\u03B3")
    t.add("D",      "\u03B4")
    t.add("E",      "\u03B5")
    t.add("Z",      "\u03B6")
    t.add("H",      "\u03B7")
    t.add("Q",      "\u03B8")
    t.add("Q)",     "\u03B8\u2019") # Occurs in BDB Unabridged from Bible Soft, as KAQ) (KAQ'))
    t.add("I",      "\u03B9")
    t.add("K",      "\u03BA")
    t.add("L",      "\u03BB")
    t.add("M",      "\u03BC")
    t.add("M)",     "\u03BC\u2019") # Occurs in BDB Unabridged from Bible Soft, as *RAEM) (*RAEM')
    t.add("N",      "\u03BD")
    t.add("C",      "\u03BE")
    t.add("O",      "\u03BF")
    t.add("P",      "\u03C0")
    t.add("P)",     "\u03C0\u2019") # Occurs in BDB Unabridged from Bible Soft, as A)P) (A)P')
    t.add("R",      "\u03C1")

    t.add("J#17",    "\u03C2\u002F")
    t.add("S#17",    "\u03C2\u002F")
    t.add("S#30",    "\u03C2\u02bc")
    t.add("J\n",    "\u03C2")
    t.add("S\n",    "\u03C2")
    t.add("J ",     "\u03C2\u0020")
    t.add("S ",     "\u03C2\u0020")
    t.add("J'",     "\u03C2\u2019")
    t.add("S'",     "\u03C2\u2019")
    t.add("J,",     "\u03C2,")
    t.add("S,",     "\u03C2,")
    t.add("J!",     "\u03C2!")
    t.add("S!",     "\u03C2!")
    t.add("J.",     "\u03C2.")
    t.add("S.",     "\u03C2.")
    t.add("J:",     "\u03C2\u0387")
    t.add("S:",     "\u03C2\u0387")
    t.add("J;",     "\u03C2\u037E")
    t.add("S;",     "\u03C2\u037E")
    t.add("J]1",    "\u03C2)")  
    t.add("S]16",   "\u03C2\u27e7") # Double square brackets in one glyph
    t.add("S]1",    "\u03C2)")
    t.add("J]",     "\u03C2]")
    t.add("S]",     "\u03C2]")
    t.add("J[",     "\u03C2[")
    t.add("S[",     "\u03C2[")
    t.add("J[1",    "\u03C2(")
    t.add("S[1",    "\u03C2(")
    t.add("JS",     "\u03C2\u03C3")  # NOTE : This doesn't make sense, but it occurs in AGNT '81
    t.add("J@",     "\u03C2@")
    t.add("S@",     "\u03C2@")
    t.add("J_",     "\u03C2\u2014") # Sigma finalis + Em-dash
    t.add("S_",     "\u03C2\u2014") # Sigma finalis + Em-dash
    t.add("S",      "\u03C3")
    t.add("S)",     "\u03C3\u2019") # Occurs in BDB Unabridged from Bible Soft, as S) (S')

    t.add("T",      "\u03C4")
    t.add("T)",     "\u03C4\u2019") # Occurs in BDB Unabridged from Bible Soft, as KAT) (KAT'))
    t.add("U",      "\u03C5")
    t.add("F",      "\u03C6")
    t.add("F)",     "\u03C6\u2019") # Occurs in BDB Unabridged from Bible Soft, as E)F) (E)F')
    t.add("X",      "\u03C7")
    t.add("Y",      "\u03C8")
    t.add("W",      "\u03C9")

    t.add("I+",     "\u03CA")
    t.add("U+",     "\u03CB")

    t.add("A)",     "\u1F00")
    t.add("A(",     "\u1F01")
    t.add("A)\\",   "\u1F02")
    t.add("A(\\",   "\u1F03")
    t.add("A)/",    "\u1F04")
    t.add("A(/",    "\u1F05")
    t.add("E)",     "\u1F10")
    t.add("E(",     "\u1F11")
    t.add("E)\\",   "\u1F12")
    t.add("E(\\",   "\u1F13")
    t.add("E)/",    "\u1F14")
    t.add("E/)",    "\u1F14")
    t.add("E(/",    "\u1F15")
    t.add("H)",     "\u1F20")
    t.add("H(",     "\u1F21")
    t.add("H)\\",   "\u1F22")
    t.add("H\\)",   "\u1F22")
    t.add("H(\\",   "\u1F23")
    t.add("H)/",    "\u1F24")
    t.add("H(/",    "\u1F25")
    t.add("I)",     "\u1F30")
    t.add("I(",     "\u1F31")
    t.add("I)\\",   "\u1F32")
    t.add("I(\\",   "\u1F33")
    t.add("I)/",    "\u1F34")
    t.add("I(/",    "\u1F35")
    t.add("O)",     "\u1F40")
    t.add("O(",     "\u1F41")
    t.add("O)\\",   "\u1F42")
    t.add("O(\\",   "\u1F43")
    t.add("O)/",    "\u1F44")
    t.add("O/)",    "\u1F44")
    t.add("O(/",    "\u1F45")
    t.add("U)",     "\u1F50")
    t.add("U(",     "\u1F51")
    t.add("U)\\",   "\u1F52")
    t.add("U(\\",   "\u1F53")
    t.add("U)/",    "\u1F54")
    t.add("U(/",    "\u1F55")
    t.add("W)",     "\u1F60")
    t.add("W(",     "\u1F61")
    t.add("W)\\",   "\u1F62")
    t.add("W(\\",   "\u1F63")
    t.add("W)/",    "\u1F64")
    t.add("W(/",    "\u1F65")

    t.add("A)=",    "\u1F06")
    t.add("A(=",    "\u1F07")
    t.add("H)=",    "\u1F26")
    t.add("H(=",    "\u1F27")
    t.add("I)=",    "\u1F36")
    t.add("I(=",    "\u1F37")
    t.add("U)=",    "\u1F56")
    t.add("U(=",    "\u1F57")
    t.add("W)=",    "\u1F66")
    t.add("W(=",    "\u1F67")

    t.add("*A)",     "\u1F08")
    t.add("*)A",     "\u1F08")
    t.add(")*A",    "\u1F08")
    t.add("*A(",     "\u1F09")
    t.add("*(A",     "\u1F09")
    t.add("(*A",     "\u1F09")
    t.add("*)\\A",   "\u1F0A")
    t.add("*(\\A",   "\u1F0B")
    t.add("(\\*A",   "\u1F0B")
    t.add("*A)/",    "\u1F0C")
    t.add("*)/A",    "\u1F0C")
    t.add(")/*A",    "\u1F0C")
    t.add("*A(/",    "\u1F0D")
    t.add("*(/A",    "\u1F0D")
    t.add("*A)=",    "\u1F0E")
    t.add("*)=A",    "\u1F0E")
    t.add("*A(=",    "\u1F0F")
    t.add("*(=A",    "\u1F0F")
    t.add("(/|*A",   "\u1F0D\u0345")
    t.add("(/|*A",   "\u1F0D\u0345")
    t.add("*(/A|",   "\u1F0D\u0345")
    #
    t.add("*E)",     "\u1F18")
    t.add("*)E",     "\u1F18")
    t.add(")*E",     "\u1F18")
    t.add("*E(",     "\u1F19")
    t.add("*(E",     "\u1F19")
    t.add("(*E",     "\u1F19")
    t.add("*)\\E",   "\u1F1A")
    t.add(")\\*E",   "\u1F1A")
    t.add("*(\\E",   "\u1F1B")
    t.add("(\\*E",   "\u1F1B")
    t.add("*E)/",    "\u1F1C")
    t.add("*)/E",    "\u1F1C")
    t.add(")/*E",    "\u1F1C")
    t.add("*E(/",    "\u1F1D")
    t.add("*(/E",    "\u1F1D")

    t.add("*H)",     "\u1F28")
    t.add("*)H",     "\u1F28")
    t.add(")*H",     "\u1F28")
    t.add("*H(",     "\u1F29")
    t.add("*(H",     "\u1F29")
    t.add("(*H",     "\u1F29")
    t.add("*H)\\",   "\u1F2A")
    t.add(")\\*H",   "\u1F2A")
    t.add("*)\\H",   "\u1F2A")
    t.add("(\\*H",   "\u1F2B")
    t.add("*(\\H",   "\u1F2B")
    t.add(")/|*H",   "\u1F2C\u0345")
    t.add("*)/H|",   "\u1F2C\u0345")
    #
    t.add("*H)/",    "\u1F2C")
    t.add("*)/H",    "\u1F2C")
    t.add(")/*H",    "\u1F2C")
    t.add("*H(/",    "\u1F2D")
    t.add("*(/H",    "\u1F2D")
    #
    t.add("*)=H",    "\u1F2E")
    t.add("(=*H",    "\u1F2F")
    t.add("*(=H",    "\u1F2F")
    t.add("*I)",     "\u1F38")
    t.add("*)I",     "\u1F38")
    t.add(")*I",     "\u1F38")
    t.add("*I(",     "\u1F39")
    t.add("*(I",     "\u1F39")
    t.add("(*I",     "\u1F39")
    t.add("*I)\\",   "\u1F3A")
    t.add("*)\\I",   "\u1F3A")
    t.add("*I(/",    "\u1F3B")
    t.add("*(/I",    "\u1F3B")
    t.add("*I)/",    "\u1F3C")
    t.add("*)/I",    "\u1F3C")
    t.add("*I(/",    "\u1F3D")
    t.add("*(/I",    "\u1F3D")
    t.add("*I)=",    "\u1F3E")
    t.add("*)=I",    "\u1F3E")
    t.add("*I(=",    "\u1F3F")
    t.add("*(=I",    "\u1F3F")
    #
    t.add("*O)",     "\u1F48")
    t.add("*)O",     "\u1F48")
    t.add(")*O",     "\u1F48")
    t.add("*O(",     "\u1F49")
    t.add("*(O",     "\u1F49")
    #
    #
    t.add("*O)\\",   "\u1F4A")
    t.add("*)\\O",   "\u1F4A")
    t.add("*O(\\",   "\u1F4B")
    t.add("*(\\O",   "\u1F4B")
    t.add("*O)/",    "\u1F4C")
    t.add("*)/O",    "\u1F4C")
    t.add("*O(/",    "\u1F4D")
    t.add("*(/O",    "\u1F4D")
    #
    t.add("*U(",     "\u1F59")
    t.add("*(U",     "\u1F59")
    t.add("(*U",     "\u1F59")
    t.add("*U(\\",   "\u1F5B")
    t.add("*(\\U",   "\u1F5B")
    #
    t.add("*(/U",    "\u1F5D")
    t.add("*U(/",    "\u1F5D")
    #
    t.add("*(=U",    "\u1F5F")
    t.add("*U(=",    "\u1F5F")
    
    t.add("*W)",     "\u1F68")
    t.add("*)W",     "\u1F68")
    t.add(")*W",     "\u1F68")
    t.add("*W(",     "\u1F69")
    t.add("*(W",     "\u1F69")
    t.add("(*W",     "\u1F69")
    #
    #
    t.add("*W)\\",   "\u1F6A")
    t.add("*)\\W",   "\u1F6A")
    t.add("*W(\\",   "\u1F6B")
    t.add("*(\\W",   "\u1F6B")
    t.add("*W)/",    "\u1F6C")
    t.add("*)/W",    "\u1F6C")
    t.add("*W(/",    "\u1F6D")
    t.add("*(/W",    "\u1F6D")
    t.add("*W)=",    "\u1F6E")
    t.add("*)=W",    "\u1F6E")
    t.add("*W(=",    "\u1F6F")
    t.add("*(=W",    "\u1F6F")

    t.add("(=|*W",   "\u1F6F\u0345")
    t.add("*(=W|",   "\u1F6F\u0345")

    t.add("A\\",    "\u1F70")
    t.add("A/",     "\u1F71")
    t.add("E\\",    "\u1F72")
    t.add("E/",     "\u1F73")
    t.add("H\\",    "\u1F74")
    t.add("H/",     "\u1F75")
    t.add("I\\",    "\u1F76")
    t.add("I/",     "\u1F77")
    t.add("O\\",    "\u1F78")
    t.add("O/",     "\u1F79")
    t.add("U\\",    "\u1F7A")
    t.add("U/",     "\u1F7B")
    t.add("W\\",    "\u1F7C")
    t.add("W/",     "\u1F7D")

    t.add("A)/|",   "\u1F84")
    t.add("A|)/",   "\u1F84")
    t.add("A(/|",   "\u1F85")
    t.add("A|(/",   "\u1F85")
    t.add("A)=|",   "\u1F86")
    t.add("H)|",    "\u1F90")
    t.add("H(|",    "\u1F91")
    t.add("H)/|",   "\u1F94")
    t.add("H)=|",   "\u1F96")
    t.add("H(=|",   "\u1F97")
    t.add("W)|",    "\u1FA0")
    t.add("W|)",    "\u1FA0")
    t.add("W(=|",   "\u1FA7")

    t.add("A=",     "\u1FB6")
    t.add("H=",     "\u1FC6")
    t.add("I=",     "\u1FD6")
    t.add("U=",     "\u1FE6")
    t.add("W=",     "\u1FF6")

    t.add("I\\+",   "\u1FD2")
    t.add("I/+",    "\u1FD3")
    t.add("I+/",    "\u1FD3")
    t.add("U\\+",   "\u1FE2")
    t.add("U/+",    "\u1FE3")
    t.add("U+/",    "\u1FE3")

    t.add("A|",     "\u1FB3")
    t.add("A/|",    "\u1FB4")
    t.add("A|/",    "\u1FB4")
    t.add("H|",     "\u1FC3")
    t.add("H/|",    "\u1FC4")
    t.add("H|/",    "\u1FC4")
    t.add("W|",     "\u1FF3")
    t.add("W|/",    "\u1FF4")
    t.add("W/|",    "\u1FF4")

    t.add("A=|",    "\u1FB7")
    t.add("H=|",    "\u1FC7")
    t.add("H|=",    "\u1FC7")
    t.add("W=|",    "\u1FF7")
    t.add("W|=",    "\u1FF7")

    t.add("R(",     "\u1FE5")
    t.add("*R(",    "\u1FEC")
    t.add("*(R",    "\u1FEC")
    t.add("(*R",    "\u1FEC")

    t.add("R)",     "\u1FE4")
    t.add("*R)",    "\u03A1\u0313") # @@@
    t.add("*)R",    "\u03A1\u0313") # @@@
    t.add(")*R",    "\u03A1\u0313")


#    t.add("~",      "~")
#    t.add("-",      "-")
    
#    t.add("(null)", "(null)")
#    t.add("&", "&")
    
    t.add("0", "0")
    t.add("1", "1")
    t.add("2", "2")
    t.add("3", "3")
    t.add("4", "4")
    t.add("5", "5")
    t.add("6", "6")
    t.add("7", "7")
    t.add("8", "8")
    t.add("9", "9")
    
    t.add("@", "@")
    t.add("%3", "\u002f") # Solidus, "/"
    t.add("#17", "\u002f") # Solidus, "/"
    t.add("[80", "\u002f") # Solidus, "/"
    t.add("]80", "\u002f") # Solidus, "/"
    t.add("$", "$")
    
    t.add(" ", " ")
    
    t.add(".", ".")
    t.add(",", ",")
    t.add("#", "\u0374") # Kaira (numerical apostrophe)
    t.add("# ", "\u0374 ") # Kaira (numerical apostrophe)
    t.add("# \n", "\u0374 ") # Kaira (numerical apostrophe)
    t.add("%19", "\u2013") # En-dash
    t.add("'", "\u2019")
    t.add(":", "\u0387")
    t.add(";", "\u037e")
    t.add("_", "\u2014") # Em-dash
    t.add("-", "\u2010") # Hyphen
    t.add("!", "!")
    

    t.add("[", "[")
    t.add("]", "]")

    t.add("[1", "(")
    t.add("]1", ")")
    t.add("[16",u"\u27e6") # Double square bracket in one glyph - open
    t.add("]16",u"\u27e7") # Double square bracket in one glyph - close
    t.add("[1I]1",   "(I)")
    t.add("[1II]1",  "(II)")
    t.add("[11]1",   "(1)")
    t.add("[12]1",  "(2)")

    
    t.add("[2", "(")
    t.add("]2", ")")

    t.add("\n", "")

    t.add("*#2", "\u03da")  # GREEK (CAPITAL) LETTER STIGMA
    t.add("#2", "\u03db")   # GREEK SMALL LETTER STIGMA
    t.add("*V", "\u03dc")   # GREEK CAPITAL LETTER DIGAMMA
    t.add("V",  "\u03dd")   # GREEK SMALL LETTER DIGAMMA
    
    return t

def beta2unicode(beta_string):
    # note that this adds \n to ensure correct handling of final sigma
    unicode_string, remainder = beta2unicodetrie.convert(beta_string + "\n")
    if remainder:
        raise ValueError("unknown sequence %s in %s" % (remainder, beta_string))
    return unicode_string

beta2unicodetrie = beta2unicodeTrie()

OLBtoBETAtrans = maketrans("abgdezhyiklmnxoprsvtufcqw", "ABGDEZHQIKLMNCOPRSSTUFXYW")

BETAtoOLBtrans = maketrans("ABGDEZHQIKLMNCOPRSTUFXYW", "abgdezhyiklmnxoprstufcqw")

def OLBtoBETAtranslate(str):
    s1 = str.translate(OLBtoBETAtrans)
    return s1.replace("<", "[").replace(">", "]")

def UMARtoBETAtranslate(str):
    s1 = str.translate(OLBtoBETAtrans)
    return s1.replace("<", "[").replace(">", "]")
