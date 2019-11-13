#!/usr/bin/env python3
"""
Created on Wed Dec  7 15:53:51 2016
@author: Odijk101
"""


from optparse import OptionParser
from typing import cast, Dict, List, Optional
import datetime
import os
import sys
import re
import csv
from .cleanCHILDESMD import cleantext, check_suspect_chars, removesuspects

# functions

charmap = cast(Dict[str, str], {})
errors = cast(List[str], [])

# From CHAT manual (October 1, 2019) https://talkbank.org/manuals/CHAT.pdf
standard_tiers = {
    "act": "Action",
    "add": "Addressee",
    "alt": "Alternate Transcription",
    "cnl": "CONNL",
    "cod": "Coding",
    "coh": "Cohesion",
    "com": "Comment",
    "def": "Definitions",
    "eng": "English Rendition",
    "err": "Error Coding",
    "exp": "Explanation",
    "fac": "Facial Gesture",
    "flo": "Flow",
    "gls": "Gloss",
    "gpx": "Gestural-Proxemic",
    "gra": "Grammatical Relations",
    "grt": "Grammatical Relations Training",
    "int": "Intonational",
    "mod": "Model",
    "mor": "Morphological",
    "ort": "Orthography",
    "par": "Paralinguistics",
    "pho": "Phonology",
    "sin": "Signing",
    "sit": "Situation",
    "spa": "Speech Act",
    "tim": "Timing",
    "trn": "Training"
}


def clean(line):
    result = line.strip()
    return(result)


def combine(str1, str2):
    result = str2 if str1 == "" else space.join([str1.rstrip(), str2.lstrip()])
    return(result)


def despace(str):
    # remvove leading and trailing spaces
    # replace other sequences of spaces by underscore
    result = str.strip()
    result = re.sub(r' +', r'_', result)
    return(result)


def get_charencoding(str):
    #  if str[1:] in legalcharencodings:
    #     result = str[1:]
    #  else:
    #     result = None
    if str[0:1] == mdchar:
        result = str[1:0]
    else:
        result is None
    return(result)


def getcorpus(metadata):
    speaker = metadata['speaker'] if 'speaker' in metadata else ''
    if 'id' in metadata and speaker in metadata['id'] and 'corpus' in metadata['id'][speaker]:
        corpus = metadata['id'][speaker]['corpus']
    else:
        corpus = 'Unknown_corpus'
    return(corpus)


def getmonths(age):
    # input format is 3;6.14 (y;m.d)
    # also accept y.m.d and y;m;d and y.m;d with a warning or any separators for that matter
    cleanage = clean(age)
    errorfound = False
    warningneeded = False
    monthstr = ""
    yearstr = ""
    thelist = re.split(seps, cleanage)
    lthelist = len(thelist)
    # print(age, thelist, file=logfile)
    # print(input('continue?'), file=logfile)
    if lthelist >= 1:
        yearstr = thelist[0]
        if not re.match('[0-9]+', yearstr):
            errorfound = True
    if lthelist >= 2:
        monthstr = thelist[1]
        if not re.match('[0-9]{1,2}', monthstr):
            errorfound = True
    if lthelist < 1 or lthelist > 3:
        errorfound = True
    if not errorfound:
        if not re.match(agere, cleanage):
            warningneeded = True
        year = int(yearstr)
        month = 0 if monthstr == "" else int(monthstr)
        if month < 0 or month > 11:
            errors.append("Warning: Illegal month value in age(0<=m<=11): {}".format(
                cleanage))
        result = 12*year + month
    else:
        result = 0
        errors.append("Error: uninterpretable age value: {}. No months attribute computed".format(
            cleanage))
    if warningneeded:
        errors.append("Warning: Illegal age syntax for {}. Syntax must be y;m.d".format(
            cleanage))
    return(result)


def getoutpaths(fullname, inpath, outpath):
    absinpath = os.path.abspath(inpath)
    absoutpath = os.path.abspath(outpath)
    fullinpath = os.path.dirname(fullname)
    reloutpath = os.path.relpath(fullinpath, start=absinpath)
    fulloutpath = os.path.join(absoutpath, reloutpath)
    return(reloutpath, fulloutpath)


def getparsefile(corpus, base, uttid):
    uttidstr = "u{:011d}".format(uttid)
    newbase = underscore.join([corpus, base, uttidstr])
    result = newbase + parseext
    return(result)


class MetaValue:
    def __init__(self, el, value_type, text):
        self.value_type = value_type
        self.text = text
        self.uel = despace(el)

    def __str__(self):
        return space.join([metakw, self.value_type, self.uel, "=", self.text])


class MetaDate(MetaValue):
    def __init__(self, el, metadata):
        d = metadata[el]
        normalized_date = d.isoformat()
        super().__init__(el, "date", str(normalized_date))


class MetaInt(MetaValue):
    def __init__(self, el, metadata):
        super().__init__(el, "int", str(metadata[el]))


class MetaTxt(MetaValue):
    def __init__(self, el, metadata):
        super().__init__(el, "text", metadata[el])


def normalizedate(str):
    global errors
    try:
        dt = datetime.datetime.strptime(str, dateformat1)
    except ValueError:
        try:
            dt = datetime.datetime.strptime(str, dateformat2)
            # print("Date {} interpreted as dd-mm-yyyy".format(str), file=logfile)
        except ValueError:
            errors.append("Date {} cannot be interpreted".format(str))
            return None
    d = dt.date()
    return d


def get_headermd(metadata):
    global errors
    for el in sorted(metadata):
        if el in donotprintinheaders:
            pass
        elif el in allheaders:
            curval = metadata[el]
            if type(curval) is str:
                yield MetaTxt(el, metadata)
            elif type(curval) is datetime.date:
                yield MetaDate(el, metadata)
            elif type(curval) is int:
                yield MetaInt(el, metadata)
            if el not in printinheaders:
                errors.append("unknown metadata element encountered: {}".format(
                    el))


def get_uttmd(metadata, outfile):
    global errors

    yield MetaInt('uttid', metadata)
    yield MetaTxt("speaker", metadata)
    # parsefileline = MetaTxt('parsefile', metadata)
    yield MetaTxt("origutt", metadata)
    yield MetaInt('uttstartlineno', metadata)
    yield MetaInt('uttendlineno', metadata)
    yield MetaTxt('childage', metadata)
    yield MetaInt('childmonths', metadata)

    curcode = metadata['speaker']
    if curcode in metadata['participants']:
        for el in metadata['participants'][curcode]:
            if el != 'role':
                yield MetaTxt(el, metadata['participants'][curcode])
    if 'id' in metadata:
        if curcode in metadata['id']:
            for el in sorted(metadata['id'][curcode]):
                curval = metadata['id'][curcode][el]

                if type(curval) is str:
                    yield MetaTxt(el, metadata['id'][curcode])
                elif type(curval) is int:
                    yield MetaInt(el, metadata['id'][curcode])
                elif type(curval) is datetime.date:
                    yield MetaDate(el, metadata['id'][curcode])
                else:
                    errors.append('get_uttmd: unknown type for {}={}'.format(
                        el, curval))


class ChatFileHeader:
    def __init__(self, metadata):
        self.metadata = {}
        for item in metadata:
            self.metadata[item.uel] = item


class ChatTier:
    """Dependent tier containing additional information about a line.
    """

    def __init__(self, id, text):
        self.id = id
        self.text = text

    @property
    def name(self):
        global standard_tiers
        try:
            return standard_tiers[self.id]
        except KeyError:
            return self.id

    def __str__(self):
        return space.join([metakw, "text", self.name, "=", self.text.replace('\n', ' ')])


class AppendLine:
    def __init__(self, text):
        self.text = text


class HeaderModified:
    pass


def processline(base, cleanfilename, entrystartno, lineno, theline, metadata, uttid, headermodified, infilename, repkeep):
    global errors
    startchar = theline[0:1]
    if startchar == mdchar:
        # to implement
        treat_mdline(lineno, theline, metadata, infilename)
        yield HeaderModified()
#        print(metadata, file=mdlog)
    else:
        if headermodified:
            yield ChatFileHeader(list(get_headermd(metadata)))
            headermodified = False
        if startchar == uttchar:
            metadata['uttid'] = uttid
            metadata['uttstartlineno'] = entrystartno
            metadata['uttendlineno'] = lineno
            treatutt(theline, metadata)
            corpus = getcorpus(metadata)
            parsefilename = getparsefile(corpus, base, uttid)
            metadata['parsefile'] = parsefilename
            endspk = theline.find(':')
            if endspk < 0:
                errors.append('error in entry  on line(s) {}-{}: {}'.format(entrystartno,
                                                                            lineno, theline))
            entry = theline[endspk+2:]
            cleanentry = cleantext(entry, repkeep)
            chat_line = ChatLine()
            chat_line.uttid = uttid
            chat_line.original = entry
            chat_line.cleaned = cleanentry
            (valid, charcodes) = check_suspect_chars(cleanentry)
            if not valid:
                errors.append("""
{} {} suspect character
input=<{}>
output=<{}>
charcodes={}
""".format(cleanfilename, lineno, theline[:-1], cleanentry, charcodes))

            updateCharMap(cleanentry, charmap)
            # remove suspect characters in the output
            cleanentry = removesuspects(cleanentry)

            for item in get_uttmd(metadata, outfile):
                # print(str(item))
                chat_line.metadata[item.uel] = item
                pass

            chat_line.text = cleanentry
            yield chat_line
        elif startchar == dependent_tier_char:
            colon = theline.find(':')
            yield ChatTier(theline[1:colon], theline[colon+1:].lstrip())
        else:
            yield AppendLine(theline)


def setatt(entrylist, i):
    lentrylist = len(entrylist)
    if lentrylist > i:
        result = clean(entrylist[i])
    else:
        result = ""
    return(result)


def treat_mdline(lineno, headerline, metadata, infilename):
    global counter, errors
    headernameend = headerline.find(headerlineendsym)
    if headernameend < 0:
        cleanheaderline = clean(headerline).lower()
        if cleanheaderline == "@utf8":
            metadata["charencoding"] = "UTF8"
        elif cleanheaderline == "@begin":
            pass
        elif cleanheaderline == "@end":
            pass
        elif cleanheaderline == '@blank':
            pass
        else:
            errors.append("Warning: {}: unknown header {} encountered in line {}".format(
                infilename, headerline, lineno))

    else:
        headername = headerline[1:headernameend]
        entry = headerline[headernameend+1:]
        cleanentry = clean(entry)
        entrylist = cleanentry.split(',')
        cleanheadername = clean(headername)
        cleanheadernamebase = clean(cleanheadername[:-3])
        headerparameter = cleanheadername[-3:]
        cleanheadername = cleanheadername.lower()
        cleanheadernamebase = clean(cleanheadername[:-3])
        if cleanheadername == 'font':
            pass
        elif cleanheadername == 'languages':
            metadata['languages'] = entrylist
        elif cleanheadername == 'colorwords':
            metadata['colorwords'] = entrylist
        elif cleanheadername == 'options':
            pass
        elif cleanheadername == 'participants':
            treatparticipants(entrylist, metadata, infilename)
        elif cleanheadername == 'id':
            treatid(entry, metadata, infilename)
        elif cleanheadername == 'date':
            metadata[cleanheadername] = normalizedate(cleanentry)
        elif cleanheadername in simpleheadernames:
            metadata[cleanheadername] = cleanentry
        elif cleanheadername in skipheadernames:
            pass
        elif cleanheadername in simpleintheadernames:
            metadata[cleanheadername] = int(cleanentry)
        elif cleanheadername in simplecounterheaders:
            counter[cleanheadername] += 1
            metadata[cleanheadername] = counter[cleanheadername]
        elif cleanheadernamebase in participantspecificheaders:
            if 'id' not in metadata:
                metadata['id'] = {}
            if headerparameter not in metadata['id']:
                metadata['id'][headerparameter] = {}
            if cleanheadernamebase == 'birth of':
                thedate = normalizedate(cleanentry)
                metadata['id'][headerparameter][cleanheadernamebase] = thedate
            elif cleanheadernamebase == 'age of':
                # print('<{}>'.format(cleanentry), file=logfile)
                # print(input('Continue?'), file=logfile)
                metadata['id'][headerparameter]['age'] = cleanentry
                if cleanentry != '':
                    metadata['childage'] = cleanentry
                months = getmonths(cleanentry)
                if months != 0:
                    metadata['id'][headerparameter]['months'] = months
                    if months != '':
                        metadata['childmonths'] = months
            else:
                metadata['id'][headerparameter][cleanheadernamebase] = cleanentry

        else:
            errors.append('Warning: {}: unknown metadata element encountered: {}'.format(
                infilename, cleanheadername))


def treatparticipants(entrylist, metadata, infilename):
    global errors
    for el in entrylist:
        ellist = el.split()
        ctr = 0
        code = ""
        name = ""
        role = ""
        if len(ellist) == 3:
            code = ellist[0]
            name = ellist[1]
            role = ellist[2]
        elif len(ellist) == 2:
            code = ellist[0]
            name = ""
            role = ellist[1]
        else:
            errors.append("{}: error in participants: too few elements {}".format(
                infilename, entrylist))
        if code != "":
            if "participants" not in metadata:
                metadata["participants"] = {}
            if code not in metadata["participants"]:
                metadata["participants"][code] = {}
            if role != "":
                metadata["participants"][code]["role"] = role
            if name != "":
                metadata["participants"][code]["name"] = name


def ischild(str):
    result = 'child' in str.lower()
    return result


def treatid(entry, metadata, infilename):
    global errors
    cleanentry = clean(entry)
    entrylist = cleanentry.split(idsep)
    lentrylist = len(entrylist)
    if lentrylist != 11:
        errors.append("{}: Warning in id: {} elements instead of 11 in {}".format(
            infilename, lentrylist, entry))
    language = setatt(entrylist, 0)
    corpus = setatt(entrylist, 1)
    code = setatt(entrylist, 2)
    age = setatt(entrylist, 3)
    sex = setatt(entrylist, 4)
    group = setatt(entrylist, 5)
    SES = setatt(entrylist, 6)
    role = setatt(entrylist, 7)
    if role == '':
        if code in metadata["participants"] and "role" in metadata["participants"][code]:
            role = metadata["participants"][code]["role"]
    education = setatt(entrylist, 8)
    custom = setatt(entrylist, 9)
    if code == "":
        errors.append("{}: error in id: no code element in {}".format(
            infilename, entry))
    else:
        if "id" not in metadata:
            metadata["id"] = {}
        if code not in metadata["id"]:
            metadata["id"][code] = {}
        if language != "":
            metadata["id"][code]["language"] = language
        if corpus != "":
            metadata["id"][code]["corpus"] = corpus
        metadata["id"][code]["age"] = age
        if ischild(role):
            metadata['childage'] = age
        if age != "":
            months = getmonths(age)
        else:
            months = ''
        metadata["id"][code]["months"] = months
        if months != '':
            metadata['childmonths'] = months
        metadata["id"][code]["sex"] = sex
        metadata["id"][code]["group"] = group
        metadata["id"][code]["SES"] = SES
        metadata["id"][code]["role"] = role
        metadata["id"][code]["education"] = education
        metadata["id"][code]["custom"] = custom


def treatutt(line, metadata):
    endspk = line.find(':')
    code = line[1:endspk]
    metadata["speaker"] = code
    metadata['origutt'] = line[endspk+2:]


def updateCharMap(str, charmap):
    for i in range(len(str)):
        curchar = str[i]
        if curchar in charmap:
            charmap[curchar] += 1
        else:
            charmap[curchar] = 1

# constants


mdchar = "@"
uttchar = "*"
dependent_tier_char = "%"
headerlineendsym = ':'
idsep = '|'
metakw = '##META'
space = ' '
parseext = ".xml"
underscore = '_'
dateformat1 = "%d-%b-%Y"
dateformat2 = "%d-%m-%Y"


simpleheadernames = ['pid',  "transcriber",  "coder",  "date",  "location",
                     "situation", 'number', 'interaction type', "activities",
                     'comment', 'bck', 'warning', 'transcription',
                     'time start', 'time duration', 'tape location', 'room layout',
                     'recording quality', 'number', 'media', 'session']
simpleintheadernames = ['g', 'page']
simplecounterheaders = ['new episode']
skipheadernames = ['exceptions']
participantspecificheaders = ['birth of', 'birthplace of', 'l1 of', 'age of']
createdmdnames = ['charencoding', 'parsefile', 'speaker', 'origutt']
seps = r'[-.,/;:_!~\\]'
digits = r'[0-9]+'
digit2 = r'[0-9]{1,2}'
optdays = r'(' + digits + r')?'
optsepdays = '(\.' + optdays + r')?'
optmonths = '(' + digit2 + optsepdays + ')?'
optsepmonths = '(;' + optmonths + ')?'
agere = '^' + digits + optsepmonths + '$'
donotprintinheaders = ['id', 'participants', 'languages',
                       'colorwords', 'options', 'uttid', 'parsefile', 'speaker', 'origutt']
allheaders = simpleheadernames + simpleintheadernames + \
    simplecounterheaders + createdmdnames + participantspecificheaders
printinheaders = [
    headeratt for headeratt in allheaders if headeratt not in donotprintinheaders]

# global variables
metadata = {}
outfile = None
logfile = None
counter = cast(Dict[str, int], {})
cleanfile = None


class ChatLine:
    def __init__(self):
        self.metadata = {}
        self.tiers = {}
        self.text = ''


class ChatFile:
    def __init__(self,
                 charmap: Dict[str, str] = {},
                 metadata: Dict[str, MetaValue] = {},
                 lines: List[ChatLine] = []):
        self.charmap = charmap
        self.metadata = metadata
        self.lines = lines

class ChatReader:
    def __init__(self):
        self.repkeep = False

    def read_file(self, filename: str) -> ChatFile:
        with open(filename, encoding='utf-8') as file:
            return self.read_string(file.read(), filename)

    def read_string(self, content: str, filename: str) -> ChatFile:
        global charmap, counter, errors, metadata
        charmap = {}
        errors = []
        self.errors = errors
        baseext = os.path.basename(filename)
        (base, ext) = os.path.splitext(baseext)

        metadata['session'] = base
        metadata['childage'] = ''
        metadata['childmonths'] = ''

        chat_file = ChatFile()
        chat_file.charmap = charmap

        lineno = 0
        entrystartno = 0
        contlinecount = 0
        uttid = 1
        counter = {}

        for el in simplecounterheaders:
            counter[el] = 0
        headermodified = False
        linetoprocess = ""
        current_line = cast(Optional[ChatLine], None)
        # dependent tier
        current_tier = cast(Optional[ChatTier], None)

        def process_line_steps(linetoprocess: str):
            global metadata
            nonlocal uttid, headermodified, current_line, current_tier
            for step in processline(base,
                                    filename,
                                    entrystartno,
                                    prevlineno,
                                    linetoprocess,
                                    metadata,
                                    uttid,
                                    headermodified,
                                    filename,
                                    self.repkeep):
                if type(step) is ChatLine:
                    if current_line != None:
                        known_line = cast(ChatLine, current_line)
                        if current_tier != None:
                            known_tier = cast(ChatTier, current_tier)
                            known_line.tiers[known_tier.id] = known_tier
                            current_tier = None
                        chat_file.lines.append(known_line)
                    current_line = step
                    uttid = step.uttid + 1
                elif type(step) is AppendLine:
                    if current_tier != None:
                        cast(ChatTier, current_tier).text += '\n' + \
                            step.text.lstrip()
                    else:
                        cast(ChatLine, current_line).text += '\n' + \
                            step.text.lstrip()
                elif type(step) is ChatFileHeader:
                    for name, value in step.metadata.items():
                        chat_file.metadata[name] = value

                if type(step) is ChatTier:
                    current_tier = step

                if type(step) is HeaderModified:
                    headermodified = True
                else:
                    headermodified = False

        try:
            for line in content.splitlines():
                prevlineno = lineno
                lineno += 1
                startchar = line[0:1]
                if startchar in ['\t']:
                    linetoprocess = combine(linetoprocess, line)
                    contlinecount += 1
                elif startchar in [mdchar, uttchar, dependent_tier_char, space]:
                    entrystartno = prevlineno - contlinecount
                    contlinecount = 0
                    if linetoprocess != "":
                        process_line_steps(linetoprocess)
                    linetoprocess = line
                # print(metadata, file=logfile)
                # print(input('Continue?'), file=logfile)
            # deal with the last line
            entrystartno = lineno - contlinecount
            process_line_steps(linetoprocess)
        except:
            raise Exception("Problem parsing {0}:{1}".format(filename, lineno))
        if current_line != None:
            known_line = cast(ChatLine, current_line)
            if current_tier != None:
                known_tier = cast(ChatTier, current_tier)
                known_line.tiers[known_tier.id] = known_tier
            chat_file.lines.append(known_line)

        return chat_file
