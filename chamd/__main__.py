#!/usr/bin/env python3
"""
Created on Wed Dec  7 15:53:51 2016
@author: Odijk101
"""


import csv
import os
import sys
from optparse import OptionParser

from .chat_reader import ChatReader


def isNotEmpty(str):
    if str is None:
        result = False
    elif str == '':
        result = False
    else:
        result = True
    return(result)


# constants


tab = '\t'
myquotechar = '"'
chaexts = [".cha", '.cex']
defaultoutext = ".txt"


def main(args=None):
    global metadata, logfile, counter, cleanfile

    """
    Main entry point.
    """
    if args is None:
        args = sys.argv[1:]

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", default="",
                      help="process the given file (default: None)")
    parser.add_option("-l", "--logfile", dest="logfilename",
                      help="logfile (default sys.stderr)")
    parser.add_option("-c", "--charmap", dest="charmapfilename",
                      help="charmap file name (default charmap.txt)")
    parser.add_option("-p", "--path",
                      dest="path", default=".",
                      help="path of the files to be processed")
    parser.add_option("--cleanfilename",
                      dest="cleanfilename", default="",
                      help="file to write processed utterances to")
    parser.add_option("--exts", dest="exts", default=chaexts,
                      help="Extensions of the files to be processed")
    parser.add_option("--outext", dest="outext", default=defaultoutext,
                      help="Extension of the processed files")
    parser.add_option("--verbose", dest="verbose", action="store_true",
                      default=False, help="show files being processed (default=False)")
    parser.add_option("--outpath",
                      dest="outpath", default=".",
                      help="path where the processed files will be put")
    parser.add_option("--repkeep",
                      dest="repkeep", default=False, action="store_true",
                      help="keep or delete (default) repeated parts ([/],[//],[//])")
    (options, args) = parser.parse_args(args)

    if isNotEmpty(options.logfilename):
        logfile = open(options.logfilename, 'w', encoding='utf8')
    else:
        logfile = sys.stderr

    if isNotEmpty(options.charmapfilename):
        charmapfilename = options.charmapfilename
    else:
        charmapfilename = "charmap.txt"

    # read metadata from the cdc file

    # determine the CHA files to be processed

    if isNotEmpty(options.filename):
        files = [options.filename]
    elif isNotEmpty(options.path):
        files = []
        for root, dirs, thefiles in os.walk(options.path):
            for file in thefiles:
                fullname = os.path.join(root, file)
                (base, ext) = os.path.splitext(file)
                if ext in options.exts:
                    files.append(fullname)

    if isNotEmpty(options.cleanfilename):
        cleanfile = open(options.cleanfilename, 'w', encoding='utf8')

    charmap = {}
    for fullname in files:
        #    thefile= open(fullname, 'r', encoding='utf8')
        #    charencodingline = thefile[0]
        #    thefile.close()
        #    charencoding = get_charencoding(charencodingline)
        #   if charencoding is None:
        #        print("No character encoding encountered in {}".format(fullname), file=logfile)
        reader = ChatReader()
        try:
            chat = reader.read_file(fullname)
            charmap.update(chat.charmap)

            if options.verbose:
                print("processing {}...".format(fullname), file=logfile)
            # mdlog = open('mdlog.txt', 'w', encoding='utf8')
            baseext = os.path.basename(fullname)
            (base, ext) = os.path.splitext(baseext)
            absinpath = os.path.abspath(options.path)
            (initpath, lastfolder) = os.path.split(options.path)
            absoutpath = os.path.abspath(options.outpath)
            fullinpath = os.path.dirname(fullname)
            reloutpath = os.path.relpath(fullinpath, start=absinpath)
            outfullpath = os.path.join(absoutpath, lastfolder, reloutpath)

            # print('fullinpath=<{}>'.format(fullinpath), file=sys.stderr)
            # print('outfullpath=<{}>'.format(outfullpath), file=sys.stderr)
            # print('', file=sys.stderr)

            if not os.path.isdir(outfullpath):
                os.makedirs(outfullpath)
            outfilename = base + options.outext
            outfullname = os.path.join(outfullpath, outfilename)

            with open(outfullname, 'w', encoding='utf8') as outfile:
                for _, item in sorted(chat.metadata.items()):
                    print(item, file=outfile)
                print('\n\n', file=outfile)
                for line in chat.lines:
                    for _, item in sorted(line.metadata.items()):
                        print(item, file=outfile)
                    for _, item in sorted(line.tiers.items()):
                        print(item, file=outfile)
                    print(line.text, file=outfile)
                    print('\n', file=outfile)
        finally:
            for error in reader.errors:
                print(error, file=logfile)
    hexformat = '{0:#06X}'
    # hexformat = "0x%0.4X"
    with open(charmapfilename, 'w', encoding='utf8') as charmapfile:
        charmapwriter = csv.writer(charmapfile, delimiter=tab, quotechar=myquotechar,
                                   quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        for el in charmap:
            ordel = ord(el)
            therow = [el, ordel, hexformat.format(ordel), charmap[el]]
            charmapwriter.writerow(therow)
    # read metadata from the CHA file

    # first read the character encoding

    # and convert it to PaQu style plain text metadata annotations

    # and convert it to LASSY XML meta elements and integrate with a Alpino-parsed  XML-file

    # and convert it to FoliA


if __name__ == "__main__":
    main()
