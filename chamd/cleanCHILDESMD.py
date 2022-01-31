#!/usr/bin/env python3
import re

baseversion = "0"
subversion = "04"
version = baseversion + "." + subversion


def scoped(str):
    result = scopestr + str
    return(result)


space = " "
eps = ''

skiplines = 1
header = 1
lctr = 0

# hexformat = '{0:#06X}'
hexformat = '\\u{0:04X}'

# scopestr = r'<([^<>]*)>\s*'

scopestr = r'<(([^<>]|\[<\]|\[>\])*)>\s*'

# [/-] and [/?] CHAT manual p. 74 not covered yet]

gtrepl = '\x00A9'  # copyright sign
ltrepl = '\x00AE'  # Registered sign
gtreplre1 = re.compile(scoped(gtrepl))
ltreplre1 = re.compile(scoped(ltrepl))
gtreplre2 = re.compile(gtrepl)
ltreplre2 = re.compile(ltrepl)


pauses3 = re.compile(r'\(\.\.\.\)')
pauses2 = re.compile(r'\(\.\.\)')
pauses1 = re.compile(r'\([0-9]*\.[0-9]*\)')
leftbracket = re.compile(r'\(')
rightbracket = re.compile(r'\)')
atsignletters = re.compile(r'@[\w:]+')
www = re.compile(r'www')
filledpause = re.compile(r'&-[\w:]+')
phonfrag0 = re.compile(r'&\+[\w:]+')
phonfrag1 = re.compile(r'&=[\w:]+')
phonfrag2 = re.compile(r'&[\w:]+')
zerostr = re.compile(r'0(\w+)')
barezero = re.compile(r'0')
plusdot3 = re.compile(r'\+\.\.\.')
ltstr = r'\[<\]'
ltre = re.compile(ltstr)

# ltre1 = re.compile(scoped(ltstr))
# ltre2 = re.compile(ltstr)
chatword = r'(&[-+=]?)?[\w\(\):+]+'
doubleslashstr = r'\[//\]'
wdoubleslash = chatword + r'\s*' + doubleslashstr
doubleslash1 = re.compile(scoped(doubleslashstr))
doubleslash2 = re.compile(doubleslashstr)
wdoubleslash1 = re.compile(wdoubleslash)
exclam2 = re.compile(r'\[!\]')
exclam1 = re.compile(r'<([^>]*)>\s*\[!\]')
slash = r'\[/\]'
wslash = chatword + r'\s*' + slash
slash2 = re.compile(scoped(slash))
slash1 = re.compile(slash)
wslash1 = re.compile(wslash)
gtstr = r'\[>\]'
gtre = re.compile(gtstr)
# gtre1 = re.compile(scoped(gtstr))
# gtre2 = re.compile(gtstr)
qstr = r'\[\?\]'
qre1 = re.compile(scoped(qstr))
qre2 = re.compile(qstr)
eqexclam = re.compile(r'<([^>]*)>\s*\[=![^\]]*\]')
eqtext1 = re.compile(r'<([^>]*)>\s*\[=[^\]]*\]')
eqtext2 = re.compile(r'\[=[^\]]*\]')
colonre = re.compile(r'[^ ]+\s+\[:([^\]]*)\]')
doubleexclam = re.compile(r'\[!!\]')
plus3 = re.compile(r'\+\/(\/)?[\.\?]')
plus2 = re.compile(r'\+[\.\^<,\+"]')
plusquote = re.compile(r'\+(\+\"\.|!\?)')

squarebracketseen = re.compile(r'\[een\]')
squarebracketstwee = re.compile(r'\[twee\]')

interpunction = re.compile(r'([,!?“”"]|\.$)')
whitespace = re.compile(r'\s+')

# nesting = re.compile(r'<([^<>]*(<[^<>]*>(\[>\]|\[<\]|[^<>])*)+)>')
# nesting = re.compile(r'<(([^<>]|\[<\]|\[>\])*)>')

# content = r'(([^<>])|\[<\]|\[>\])*'
# content = r'(([^<>])|(\[<\])|(\[>\]))*'
# content = r'((\[<\])|(\[>\])|([^<>]))*'
# nested = r'(<' + content + r'>' + content + r')+'
# neststr = r'(<' + content + nested + r'>)'
# nesting = re.compile(neststr)


def bracket(str):
    result = '(' + str + ')'
    return(result)


def reor(strlist):
    result1 = '|'.join(strlist)
    result = bracket(result1)
    return(result)


def restar(str):
    result = bracket(str) + '*'
    return(result)


embed = r'(<[^<>]*>)'
other = r'[^<>]'
embedorother = reor([embed, other])
neststr = r'(<' + restar(other) + embed + restar(embedorother) + r'>)'
nesting = re.compile(neststr)

timesstr = r'\[x[^\]]*\]'
times = re.compile(timesstr)
scopedtimes = re.compile(scoped(timesstr))
scopedinlinecom = re.compile(r'<([^<>]*)>\s*\[\% [^\]]*\]')
inlinecom = re.compile(r'\[\% [^\]]*\]')
tripleslash = r'\[///\]'
wtripleslash = chatword + r'\s*' + tripleslash

reformul = re.compile(tripleslash)
scopedreformul = re.compile(scoped(tripleslash))
wreformul = re.compile(wtripleslash)
endquote = re.compile(r'\+"/\.')
# adapted to deal with the codings in CHAT manual p. 103/104
errormarkstr = r'\[\*[^\]]*\]'
errormark2 = re.compile(errormarkstr)
errormark1 = re.compile(scoped(errormarkstr))
dependenttier = re.compile(r'\[%(act|add|gpx|int|sit|spe):[^]]*\]')
postcodes = re.compile(r'\[\+[^]]*\]')
precodes = re.compile(r'\[-[^]]*\]')
bch = re.compile(r'\[\+\s*bch\]')
trn = re.compile(r'\[\+\s*trn\]')
syllablepause = re.compile(r'(\w)\^')
complexlocalevent = re.compile(r'\[\^[^\]]*\]')
cliticlink = re.compile(r'~')
chat_ca_syms = re.compile('[↓↑↑↓⇗↗→↘⇘∞≈≋≡∙⌈⌉⌊⌋∆∇⁎⁇°◉▁▔☺∬Ϋ∮§∾↻Ἡ„‡̣̣ʰ̄ʔ0]')
timealign = re.compile(r'\u0015[0123456789_ ]+\u0015')
segmentrep = re.compile('\u21AB[^\u21AB]*\u21AB')
blocking = re.compile('\u2260')
internalpause = re.compile(r'\^')


def check_suspect_chars(newline):
    invalid = checkpattern.search(newline) or pluspattern.search(newline)
    if invalid:
        return (False, str2codes(newline))
    else:
        return (True, None)


def checkline(line, newline, outfilename, lineno, logfile):
    (valid, thecodes) = check_suspect_chars(newline)
    if not valid:
        print(outfilename, lineno, 'suspect character', file=logfile)
        print('input=<{}>'.format(line[:-1]), file=logfile)
        print('output=<{}>'.format(newline), file=logfile)
        print('charcodes=<{}>'.format(thecodes), file=logfile)


def cleantext(str, repkeep):
    result = str

    # if times.search(result):
    # print('[x ...] found, line={}'.format(result), file=logfile)

# page references are to MacWhinney chat manual version 21 april 2015

# replace [<] and [>]

    result = ltre.sub(ltrepl, result)
    result = gtre.sub(gtrepl, result)

    match = nesting.search(result)
    if match is not None:
        b = match.start(1) + 1
        e = match.end(1) - 1
        midstr = result[b:e]
        newmidstr = cleantext(midstr, repkeep)
        leftstr = result[:b]
        rightstr = result[e:]
        result = leftstr + newmidstr + rightstr


# remove scoped times <...> [x ...] keeping the ... between <> not officially defined
    result = scopedtimes.sub(r'\1', result)

# remove scoped inlinecom <...> [% ...] keeping the ... between <> not officially defined
    result = scopedinlinecom.sub(r'\1', result)

# remove pauses
    result = pauses3.sub(space, result)
    result = pauses2.sub(space, result)
    result = pauses1.sub(space, result)

# remove round brackets
    result = leftbracket.sub(eps, result)
    result = rightbracket.sub(eps, result)

# remove multiple wordmarker p. 43, 73-74
    result = times.sub(eps, result)

# remove @letters+:
    result = atsignletters.sub(eps, result)

# remove inline comments [% ...] p70, 78, 85
    result = inlinecom.sub(eps, result)


# keep or remove scoped reformulation symbols [///] p 73 depending on repkeep
    if repkeep:
        result = scopedreformul.sub(r'\1', result)
    else:
        result = scopedreformul.sub(eps, result)

# keep or remove reformulation symbols [///] p 73 depending on repkeep
    if repkeep:
        result = reformul.sub(space, result)
    else:
        result = wreformul.sub(eps, result)

# remover errormark1 [*] and preceding <>
    result = errormark1.sub(r'\1 ', result)

# remover errormark2 [*]
    result = errormark2.sub(eps, result)

# remove inline dependent tier [%xxx: ...]

    result = dependenttier.sub(eps, result)

# remove    postcodes p. 75-76
    result = postcodes.sub(eps, result)

# remove precodes p.75-76
    result = precodes.sub(eps, result)

# remove bch p. 75-76
    result = bch.sub(eps, result)

# remove trn p.75-76
    result = trn.sub(eps, result)

# remove xxx should we do this? or something else? add xxx as a word in Alpino?
# no we keep this
#    result = re.sub(r'xxx', '', result)

# remove yyy should we do this? or something else? add xxx as a word in Alpino?
# we keep this too
#    result = re.sub(r'yyy', '', result)


# remove +...  p. 63
    result = plusdot3.sub(eps, result)


# remove [<] and preceding <> on purpose before [//]
    result = ltreplre1.sub(r'\1 ', result)

# remove [<]   on purpose before [//]
    result = ltreplre2.sub(space, result)

# remove [>] and preceding <>
    result = gtreplre1.sub(r'\1 ', result)

# remove [>]
    result = gtreplre2.sub(space, result)


# remove [//] keep preceding part between <>, drop <> or delete <...> depending on repkeep
    if repkeep:
        result = doubleslash1.sub(r'\1', result)
    else:
        result = doubleslash1.sub(eps, result)


# remove [//] keep preceding word or delete it depending on repkeep
    if repkeep:
        result = doubleslash2.sub(eps, result)
    else:
        result = wdoubleslash1.sub(eps, result)

# remove [!] and <> around preceding text    p.68
    result = exclam1.sub(r'\1', result)

# remove [!] p.68
    result = exclam2.sub(space, result)


# remove [/] keep or delete preceding part between <> depending on repkeep option this line and following one: crucial order
    if repkeep:
        result = slash2.sub(r'\1', result)
    else:
        result = slash2.sub(eps, result)

# remove [/] keep the word before or delete it depending on repkeep option
    if repkeep:
        result = slash1.sub(eps, result)
    else:
        result = wslash1.sub(eps, result)

#    result = re.sub(r'\[<\]', '', result)


# remove [?] and preceding <>
    result = qre1.sub(r'\1 ', result)

# remove [?]
    result = qre2.sub(space, result)

# remove [=! <text>] and preceding <>
    result = eqexclam.sub(r'\1 ', result)

# remove [= <text> ] and preceding <>  p 68/69 explanation
    result = eqtext1.sub(r'\1 ', result)

# remove [= <text>]
    result = eqtext2.sub(space, result)

# replace word [: text] by text
    result = colonre.sub(r'\1 ', result)

    # remove filled pauses ( &- p. 89)
    result = filledpause.sub(space, result)

    # remove phonological fragments &+
    #    https://talkbank.org/manuals/Clin-CLAN.pdf states &+ for phonological fragments(p. 18)
    result = phonfrag0.sub(space, result)

    # remove phonological fragments p. 61 &=
    result = phonfrag1.sub(eps, result)

    # remove phonological fragments p.61 &
    result = phonfrag2.sub(eps, result)

    # remove www intentionally after phonological fragments
    result = www.sub(eps, result)

    # replace 0[A-z] works ok now, raw replacement string!
    result = zerostr.sub(r'\1', result)

    # delete any remaining 0's
    result = barezero.sub(space, result)

    # remove underscore
    result = re.sub(r'_', eps, result)

    # remove [!!]
    result = doubleexclam.sub(space, result)

# remove +"/. p. 64-65
    result = endquote.sub(eps, result)

# remove +/. +/? +//. +//?
    result = plus3.sub(r' ', result)

# remove +.  +^ +< +, ++ +" (p. 64-66)
    result = plus2.sub(r' ', result)

# remove +".    (p. 65)  +!? (p. 63)
    result = plusquote.sub(r' ', result)

# remove silence marks (.) (..) (...) done above see pauses
#    result = re.sub(r'\(\.(\.)?(\.)?\)', r' ', result)

# remove syllablepauses p. 60
    result = syllablepause.sub(r'\1', result)

# remove complexlocalevent p. 61
    result = complexlocalevent.sub(space, result)

# replace clitic link ~by space
    result = cliticlink.sub(space, result)

# replace chat-ca codes by space p. 86,87
    result = chat_ca_syms.sub(space, result)

# remove time alignment p. 67
    result = timealign.sub(space, result)

# remove segment repetitions p89 Unicode 21AB UTF8 e2 86 ab
    result = segmentrep.sub(eps, result)

# remove blocking Unicode 2260 not-equal sign    p89
    result = blocking.sub(eps, result)

# remove  internal pausing ^  p. 89
    result = internalpause.sub(eps, result)

# next is an ad-hoc extension for Lotti
# replace [een], [twee] by space
    result = squarebracketseen.sub(space, result)
    result = squarebracketstwee.sub(space, result)

# surround interpunction with whitespace
    result = interpunction.sub(lambda m: ' ' + m.group(0) + ' ', result)

# remove superfluous spaces etc. this also removes CR etc
    result = whitespace.sub(' ', result)
    result = result.strip()
    return(result)
# end function cleantext


def isNotEmpty(str):
    if str is None:
        result = False
    elif str == '':
        result = False
    else:
        result = True
    return(result)


def str2codes(str):
    result = []
    for i in range(len(str)):
        curchar = str[i]
        curcode = hexformat.format(ord(str[i]))
        result.append((curchar, curcode))
    return(result)


def removesuspects(str):
    result1 = re.sub(checkpattern, space, str)
    result2 = re.sub(pluspattern1, r'\1', result1)
    result = re.sub(pluspattern2, r'\1', result2)
    return result


checkpattern = re.compile(
    r'[][\(\)&%@/=><_^~↓↑↑↓⇗↗→↘⇘∞≈≋≡∙⌈⌉⌊⌋∆∇⁎⁇°◉▁▔☺∬Ϋ·\u22A5\u00B7\u0001\u2260\u21AB]')
# + should not occur except as compound marker black+board
# next one split up in order to do substitutions
pluspattern = re.compile(r'(\W)\+|\+(\W)')
pluspattern1 = re.compile(r'(\W)\+')
pluspattern2 = re.compile(r'\+(\W)')
