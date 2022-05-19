#!/usr/bin/env python3
"""
Created on Wed Dec  7 15:53:51 2016
@author: Odijk101
"""


from typing import cast, Dict, List, Optional
import datetime
import os
import re
from .cleanCHILDESMD import cleantext, check_suspect_chars, removesuspects

# functions

charmap = cast(Dict[str, str], {})
errors = cast(List[str], [])

# From CHAT manual (October 1, 2019) https://talkbank.org/manuals/CHAT.pdf
standard_tiers = {
    "act": "action",
    "add": "addressee",
    "alt": "alternate transcription",
    "cnl": "connl",
    "cod": "coding",
    "coh": "cohesion",
    "com": "comment",
    "def": "definitions",
    "eng": "english rendition",
    "err": "error coding",
    "exp": "explanation",
    "fac": "facial gesture",
    "flo": "flow",
    "gls": "gloss",
    "gpx": "gestural-proxemic",
    "gra": "grammatical relations",
    "grt": "grammatical relations training",
    "int": "intonational",
    "mod": "model",
    "mor": "morphological",
    "ort": "orthography",
    "par": "paralinguistics",
    "pho": "phonology",
    "sin": "signing",
    "sit": "situation",
    "spa": "speech act",
    "tim": "timing",
    "trn": "training"
}


def clean(line):
    result = line.strip()
    return(result)


def combine(str1, str2):
    result = str2 if str1 == "" else space.join([str1.rstrip(), str2.lstrip()])
    return(result)


def despace(str):
    # remove leading and trailing spaces
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
        result = None
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
    # also accept y.m.d and y;m;d and y.m;d with a warning
    # or any separators for that matter
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
        result = (12 * year) + month
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
    def __init__(self, el: str, value_type: str, text: str):
        self.value_type = value_type
        self.text = text
        self.uel = despace(el)

    def __str__(self):
        try:
            return space.join([metakw, self.value_type, self.uel, "=", self.text])
        except Exception:
            raise Exception([self.uel, self.text])


class MetaDate(MetaValue):
    def __init__(self, el, entry: datetime.date):
        normalized_date = entry.isoformat()
        super().__init__(el, "date", str(normalized_date))


class MetaInt(MetaValue):
    def __init__(self, el, entry: int):
        super().__init__(el, "int", str(entry))


class MetaTxt(MetaValue):
    def __init__(self, el, entry: str):
        super().__init__(el, "text", entry)


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


def get_metavalue(el, entry):
    if type(entry) is str:
        return MetaTxt(el, entry)
    elif type(entry) is datetime.date:
        return MetaDate(el, entry)
    elif type(entry) is int:
        return MetaInt(el, entry)
    else:
        return None


def get_headermd(metadata):
    global errors
    for el in sorted(metadata):
        entry = metadata[el]
        value = get_metavalue(el, entry)
        if value is not None:
            yield value


def get_uttmd(file_metadata, metadata):
    global errors
    for el in sorted(metadata):
        entry = metadata[el]
        if el not in file_metadata or entry != file_metadata[el]:
            value = get_metavalue(el, entry)
            if value is not None:
                yield value

    curcode = metadata['speaker']
    if curcode in metadata['participants']:
        for el in metadata['participants'][curcode]:
            if el != 'role':
                yield MetaTxt(el, metadata['participants'][curcode][el])
    if 'id' in metadata:
        if curcode in metadata['id']:
            for el in sorted(metadata['id'][curcode]):
                entry = metadata['id'][curcode][el]
                value = get_metavalue(el, entry)
                if value is not None:
                    yield value
                else:
                    errors.append('get_uttmd: unknown type for {}={}'.format(
                        el, entry))


class ChatHeadersList:
    """A list of headers was parsed
    """

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


class ChatHeader:
    def __init__(self, metadata=None, line=None, linestartno=None):
        self.headerdata = metadata
        self.line = line
        self.linestartno = linestartno


def processline(base, cleanfilename, entrystartno,
                lineno, theline, file_metadata: Dict[str, str],
                metadata, uttid, prev_header: bool, infilename, repkeep):
    global errors
    startchar = theline[0:1]
    if startchar == mdchar:
        treat_mdline(lineno, theline, metadata, infilename)
        yield ChatHeader(metadata, theline, lineno)
    else:
        if prev_header:
            yield ChatHeadersList(list(get_headermd(metadata)))
            if not file_metadata:
                file_metadata.update(metadata)
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
            entry = theline[endspk + 2:]
            cleanentry = cleantext(entry, repkeep)
            chat_line = ChatLine(uttid, entry, cleanentry)
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

            for item in get_uttmd(file_metadata, metadata):
                # print(str(item))
                chat_line.metadata[item.uel] = item
                pass

            chat_line.text = cleanentry
            yield chat_line
        elif startchar == dependent_tier_char:
            colon = theline.find(':')
            yield ChatTier(theline[1:colon], theline[colon + 1:].lstrip())
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
        entry = headerline[headernameend + 1:]
        cleanentry = clean(entry)
        entrylist = cleanentry.split(',')
        cleanheadername = clean(headername)
        cleanheadernamebase = clean(cleanheadername[:-3])
        speaker_id = cleanheadername[-3:]
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
            if speaker_id not in metadata['id']:
                metadata['id'][speaker_id] = {}
            if cleanheadernamebase == 'birth of':
                thedate = normalizedate(cleanentry)
                metadata['id'][speaker_id][cleanheadernamebase] = thedate
            elif cleanheadernamebase == 'age of':
                # print('<{}>'.format(cleanentry), file=logfile)
                # print(input('Continue?'), file=logfile)
                metadata['id'][speaker_id]['age'] = cleanentry
                if cleanentry != '':
                    metadata['childage'] = cleanentry
                months = getmonths(cleanentry)
                if months != 0:
                    metadata['id'][speaker_id]['months'] = months
                    if months != '':
                        metadata['childmonths'] = months
            else:
                metadata['id'][speaker_id][cleanheadernamebase] = cleanentry

        else:
            errors.append('Warning: {}: unknown metadata element encountered: {}'.format(
                infilename, cleanheadername))


def treatparticipants(entrylist, metadata, infilename):
    global errors
    for el in entrylist:
        ellist = el.split()
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
    metadata['origutt'] = line[endspk + 2:]


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


simpleheadernames = ['pid', "transcriber", "coder", "date", "location",
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
optsepdays = r'(\.' + optdays + r')?'
optmonths = '(' + digit2 + optsepdays + ')?'
optsepmonths = '(;' + optmonths + ')?'
agere = '^' + digits + optsepmonths + '$'
allheaders = simpleheadernames + simpleintheadernames + \
    simplecounterheaders + createdmdnames + participantspecificheaders

# global variables
logfile = None
counter = cast(Dict[str, int], {})
cleanfile = None


class ChatLine:
    def __init__(self, uttid: str, original: str, cleaned: str):
        self.metadata = cast(Dict[str, MetaValue], {})
        self.tiers = cast(Dict[str, ChatTier], {})
        self.text = ''
        self.uttid = uttid
        self.original = original
        self.cleaned = cleaned


class ChatFile:
    def __init__(self,
                 charmap: Dict[str, str] = None,
                 metadata: Dict[str, MetaValue] = None,
                 lines: List[ChatLine] = None,
                 header_metadata: Dict = None,
                 headers: List[ChatHeader] = None):
        self.charmap = charmap or {}
        self.metadata = metadata or {}
        self.lines = lines or []
        self.header_metadata = header_metadata or {}
        self.headers = headers or []


class ChatReader:
    def __init__(self):
        global counter, cleanfile
        self.repkeep = False

    def read_file(self, filename: str) -> ChatFile:
        with open(filename, encoding='utf-8') as file:
            return self.read_string(file.read(), filename)

    def read_string(self, content: str, filename: str) -> ChatFile:
        global charmap, counter, errors
        charmap = {}
        errors = []

        file_metadata = cast(Dict[str, str], {})
        metadata = cast(Dict[str, str], {})
        counter = cast(Dict[str, int], {})

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
        prev_header = False
        linetoprocess = ""
        current_line = cast(Optional[ChatLine], None)
        # dependent tier
        current_tiers = cast(List[Optional[ChatTier]], [])

        def process_line_steps(linetoprocess: str):
            nonlocal uttid, prev_header, current_line, current_tiers, file_metadata, metadata
            for step in processline(base,
                                    filename,
                                    entrystartno,
                                    prevlineno,
                                    linetoprocess,
                                    file_metadata,
                                    metadata,
                                    uttid,
                                    prev_header,
                                    filename,
                                    self.repkeep):
                if type(step) is ChatLine:
                    if current_line is not None:
                        known_line = cast(ChatLine, current_line)
                        if current_tiers != []:
                            known_tiers = cast(List[ChatTier], current_tiers)
                            for kt in known_tiers:
                                known_line.tiers[kt.id] = kt
                                current_tiers = []

                        chat_file.lines.append(known_line)
                    current_line = step
                    uttid = step.uttid + 1
                elif type(step) is AppendLine:
                    if current_tiers != []:
                        for ct in current_tiers:
                            cast(ChatTier, ct).text += '\n' + \
                                step.text.lstrip()
                    else:
                        cast(ChatLine, current_line).text += '\n' + \
                            step.text.lstrip()
                elif type(step) is ChatHeadersList:
                    if current_line is None:
                        for name, value in step.metadata.items():
                            chat_file.metadata[name] = value

                if type(step) is ChatTier:
                    current_tiers.append(step)

                if type(step) is ChatHeader:
                    prev_header = True
                    if current_line is None:
                        chat_file.header_metadata.update(step.headerdata)
                        # Keep a record of the raw header for the purpose of reconstrucing CHAT file
                        # Hacky, should also contain the parsed header data
                        chat_file.headers.append(ChatHeader(
                            line=step.line, linestartno=step.linestartno))
                else:
                    prev_header = False

        try:
            for line in content.splitlines():
                prevlineno = lineno
                lineno += 1
                try:
                    if line.lstrip()[0] == dependent_tier_char:
                        line = re.sub(r'^(\s+)?%', '%', line)
                except IndexError:
                    pass
                startchar = line[0:1]
                if startchar in ['\t', ' ']:
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
        except Exception:
            raise Exception("Problem parsing {0}:{1}".format(filename, lineno))
        if current_line is not None:
            known_line = cast(ChatLine, current_line)
            if current_tiers != []:
                known_tiers = cast(List[ChatTier], current_tiers)
                for kt in known_tiers:
                    known_line.tiers[kt.id] = kt
            chat_file.lines.append(known_line)

        return chat_file
