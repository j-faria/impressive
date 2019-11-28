#!/usr/bin/env python
from __future__ import print_function
import sys, re, optparse, os
try:
    import HTMLParser
except:
    import html.parser as HTMLParser
__version__ = "0.1.2"

DEBUG = False

REPLACEMENTS = (
    ('\n', " "),
    ('\t', " "),
    ('\r', ""),
    ("\\", "\\\\"),
    ('/', "/\\:"),
    ('-', "\\-"),
)

ENTITIES = {
    "laquo": '"',
    "raquo": '"',
    "ldquo": '"',
    "rdquo": '"',
    "quot": '"',
    "amp": '&',
    "ndash": '-',
    "mdash": '--',
    "rarr": '->',
    "gt": '>',
    "lt": '<',
    "times": 'x',
    "eacute": 'e',
    "nbsp": ' ',
}

class Converter(HTMLParser.HTMLParser):
    def __init__(self, outfile):
        try:
            HTMLParser.HTMLParser.__init__(self, convert_charrefs=False)
        except TypeError:
            HTMLParser.HTMLParser.__init__(self)
        self.f = outfile
        self.f.write(".\\\" generated by KeyJ's html2man.py version %s\n" % __version__)
        self.stack = []
        self.enabled = False
        self.data = ""
        self.start = True
        self.listspace = True

    def flush(self):
        if not self.data: return
        self.f.write(self.data + "\n")
        self.data = ""

    def newblock(self, cmd=None, prefix=None):
        self.flush()
        if cmd:
            self.f.write(cmd + "\n")
            self.start = True
        if prefix:
            self.data = prefix + " "
            self.start = False

    def endheading(self, index=None, indent=0):
        if not self.data: return
        heading = self.data.strip().upper()
        self.data = ""
        self.start = True
        self.f.write(".SH \"%s%s\"\n" % (indent * ' ', heading))
        if index:
            self.f.write(".IX %s \"%s\"\n" % (index, heading))

    def handle_starttag(self, tag, attrs):
        if DEBUG: print("starttag:", tag, attrs)
        tag = tag.lower()
        if (tag == "p") and (tag in self.stack):
            raise HTMLParser.HTMLParseError("nested <p> found")
        self.stack.append(tag)
        if not self.enabled: return
        if tag in ("b", "strong", "code"):
            self.data += "\\fB"
        if tag in ("i", "em"):
            self.data += "\\fI"
        if tag == "dt":
            self.newblock(cmd=".br")
        if tag == "dd":
            self.newblock(cmd=".RS")
        if tag == "pre":
            self.newblock(cmd=".nf")
        if tag in ("h2", "h3"):
            self.newblock()

    def handle_startendtag(self, tag, attrs):
        if DEBUG: print("startendtag:", tag, attrs)
        if not self.enabled: return
        tag = tag.lower()
        if tag == "br":
            self.newblock(cmd=".br")

    def handle_endtag(self, tag):
        if DEBUG: print("endtag:", tag)
        tag = tag.lower()
        if not(self.stack) or (self.stack[-1] != tag):
            raise HTMLParser.HTMLParseError("line %s: start/end tag mismatch\nstack is %r, got %r" % (self.getpos()[0], self.stack, tag))
        del self.stack[-1]
        if not self.enabled: return
        if tag == "p":
            self.newblock(cmd=".PP")
        if tag in ("b", "strong", "code", "i", "em"):
            self.data += "\\fR"
        if tag == "dd":
            self.newblock(cmd=".RE")
            if self.listspace and not("dd" in self.stack):
                self.f.write(".PP\n")
        if tag == "pre":
            self.newblock(cmd=".fi")
        if tag == "h2":
            self.endheading("Header")
        if tag == "h3":
            self.endheading("Subsection", 4)

    def handle_data(self, data):
        if DEBUG: print("data:", repr(data))
        if not self.enabled: return
        if self.stack:
            tag = self.stack[-1]
        else:
            tag = None
        if tag == "pre":
            lines = data.replace("\r", "").rstrip().split("\n")
            self.f.write(".ne %d\n" % len(lines))
            for l in lines:
                self.f.write("\\&  %s\n" % l.replace('\\', '\\\\'))
            self.f.write(".\n")
            self.data = ""
        else:
            for old, new in REPLACEMENTS:
                data = data.replace(old, new)
            if not(self.data) and self.start:
                data = data.lstrip()
            self.data += data

    def handle_charref(self, name):
        if DEBUG: print("charref:", name)

    def handle_entityref(self, name):
        if DEBUG: print("entityref:", name)
        if not self.enabled: return
        self.data += ENTITIES.get(name, "")

    def handle_comment(self, data):
        if DEBUG: print("comment:", repr(data))
        data = data.strip()
        if data[:3].lower() != "man": return
        commands = data.split()[0]
        for x in commands.lower().split(':'):
            x = x.split('=', 1)
            if len(x) == 1:
                cmd = x[0]
                arg = None
            else:
                cmd, arg = x
                arg = arg.replace('~', ' ')
                if arg.startswith('"') and arg.endswith('"'):
                    arg = arg[1:-1]
            if cmd == "on":
                self.enabled = True
            elif cmd == "off":
                self.flush()
                self.enabled = False
            elif cmd == "nolistspace":
                self.listspace = False
            elif cmd == "listspace":
                self.listspace = True
            elif cmd == "head":
                self.data = arg.replace('_', ' ')
                self.endheading("Header")
            elif cmd == "subhead":
                self.data = arg.replace('_', ' ')
                self.endheading("Subsection", 4)
            elif cmd != "man":
                print("unknown command `%s'" % cmd, file=sys.stderr)
        data = data[len(commands):].lstrip().replace("\r\n", "\n")
        if data:
            if self.data:
                self.data += data
            else:
                self.f.write(data + "\n")

    def handle_decl(self, decl):
        if DEBUG: print("decl:", decl)

    def handle_pi(self, data):
        if DEBUG: print("PI:", data)


if __name__ == "__main__":
    parser = optparse.OptionParser(usage="%prog [OPTIONS...] <input.html>", version=__version__)
    parser.add_option("-O", "--output", dest="OutputFile", metavar="FILE",
                      type="string", default=None,
                      help="write document(s) to FILE instead of <input filename>.1")
    options, args = parser.parse_args()
    globals().update(options.__dict__)
    if not args:
        parser.error("no input file specified")
    if len(args) > 1:
        parser.error("invalid number of arguments")
    InputFile = args[0]
    if not OutputFile:
        OutputFile = os.path.splitext(InputFile)[0] + ".1"

    try:
        InputFile = open(InputFile, "r")
    except IOError:
        parser.error("cannot open input file")

    try:
        OutputFile = open(OutputFile, "w")
    except IOError:
        parser.error("cannot open output file")

    c = Converter(OutputFile)
    c.feed(InputFile.read())
    c.close()
    InputFile.close()
    OutputFile.close()
