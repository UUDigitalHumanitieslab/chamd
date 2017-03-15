#import collections
import sys
#import pdb
import re
#import getopt
#import csv
from optparse import OptionParser
import os


space = " "
eps = ''

skiplines = 1
header = 1
lctr = 0

pauses3=re.compile(r'\(\.\.\.\)')
pauses2=re.compile(r'\(\.\.\)')
pauses1=re.compile(r'\(\.\)')
leftbracket=re.compile(r'\(')
rightbracket=re.compile(r'\)')
atsignletters = re.compile(r'@[A-z:]+')
www= re.compile(r'www')
phonfrag1 = re.compile(r'&=[A-z:]+')
phonfrag2 = re.compile(r'&[A-z]+')
zerostr = re.compile(r'0([A-z]+)')
plusdotdot = re.compile(r'\+\.\.')
ltre1 = re.compile(r'<([^>]+)>\s*\[<\]')
ltre2 = re.compile(r'\[<\]')
doubleslash1 = re.compile(r'<([^>]*)>\s*\[//\]')
doubleslash2 = re.compile(r'\[//\]')
exclam2 = re.compile(r'\[!\]')
exclam1 = re.compile(r'<([^>]*)>\s*\[!\]')
slash2 = re.compile(r'<([^>]*)>\s*\[/\]')
slash1 = re.compile(r'\[/\]')
gtre1 = re.compile(r'<([^>]+)>\s*\[>\]')
gtre2 = re.compile(r'\[>\]')
qre1 = re.compile(r'<([^>]+)>\s*\[\?\]')
qre2 = re.compile(r'\[\?\]')
eqexclam = re.compile(r'<([^>]+)>\s*\[=![^\]]*\]')
eqtext1 = re.compile(r'<([^>]+)>\s*\[=[^\]]*\]')
eqtext2 = re.compile(r'\[=[^\]]*\]')
colonre = re.compile(r'[^ ]+\s+\[:([^\]]*)\]')
doubleexclam = re.compile(r'\[!!\]')
plus3 = re.compile(r'\+\/(\/)?[\.\?]')
plus2 = re.compile(r'\+[\.\^<,\+"]')
plusquote = re.compile(r'\+(\+\"\.|!\?)')
nesting = re.compile(r'<([^<>]*(<[^<>]*>(\[>\]|\[<\]|[^<>])*)+)>')
times = re.compile(r'\[x[^\]]*\]')
scopedtimes = re.compile('<([^<>]*)>\s*\[x[^\]]*\]')
scopedinlinecom = re.compile(r'<([^<>]*)>\s*\[\% [^\]]*\]')
inlinecom = re.compile(r'\[\% [^\]]*\]')
reformul = re.compile(r'\[///\]')
endquote = re.compile(r'\+"/\.')
errormark = re.compile(r'\[\*\]')
dependenttier = re.compile(r'\[%(act|add|gpx|int|sit|spe):[^]]*\]')
postcodes = re.compile(r'\[\+[^]]*\]')
precodes = re.compile(r'\[-[^]]*\]')
bch = re.compile(r'\[\+\s*bch\]')
trn = re.compile(r'\[\+\s*trn\]')

def checkline(line, newline,outfilename,lineno, logfile):
    if checkpattern.search(newline) or pluspattern.search(newline):
        print(outfilename, lineno, 'suspect character', file=logfile)
        print('input=<{}>'.format(line[:-1]), file=logfile )
        print('output=<{}>'.format(newline[:-1]), file=logfile)


def cleantext(str):
    result = str

    #if times.search(result):
        #print('[x ...] found, line={}'.format(result), file=logfile)
    
# page references are to MacWhinney chat manual version 21 april 2015    
#nesting of <>
    match = nesting.search(result)
    if match is not None:
       b = match.start(1)
       e = match.end(1) +1
       midstr = result[b:e]
       newmidstr = cleantext(midstr)
       result = result[:b]+newmidstr+result[e:]


#remove scoped times <...> [x ...] keeping the ... betwen <> not officially defined
    result = scopedtimes.sub(r'\1',result)
    
#remove scoped inlinecom <...> [% ...] keeping the ... betwen <> not officially defined
    result = scopedinlinecom.sub(r'\1', result)
    
#remove pauses
    result=pauses3.sub(space, result)
    result=pauses2.sub(space, result)
    result=pauses1.sub(space, result)

#remove round brackets
    result = leftbracket.sub(eps, result)
    result = rightbracket.sub(eps, result)
    
# remove multiple wordmarker p. 43, 73-74    
    result = times.sub(eps,result)
    
#remove @letters+:
    result = atsignletters.sub(eps, result)

#remove inline comments [% ...] p70, 78, 85
    result = inlinecom.sub(eps, result)
    
#remove reformulation symbols [///] p 73
    result = reformul.sub(eps, result)

#remover errormark [*]
    result = errormark.sub(eps, result)
    
#remove inline dependent tier [%xxx: ...]

    result = dependenttier.sub(eps, result)
    
#remove    postcodes p. 75-76
    result = postcodes.sub(eps, result)
    
#remove precodes p.75-76
    result = precodes.sub(eps, result)

#remove bch p. 75-76
    result = bch.sub(eps, result)

#remove trn p.75-76
    result = trn.sub(eps, result)
    
#remove xxx should we do this? or something else? add xxx as a word in Alpino?
#no we keep this
#    result = re.sub(r'xxx', '', result)

#remove yyy should we do this? or something else? add xxx as a word in Alpino?
#we keep this too
#    result = re.sub(r'yyy', '', result)

#remove www 
    result = www.sub(eps, result)

#remove phonological fragments p. 61
    result = phonfrag1.sub(eps, result)


    
#remove phonological fragments p.61
    result = phonfrag2.sub(eps, result)
    
#replace 0[A-z] works ok now, raw replacement string!
    result = zerostr.sub(r'\1', result)

#remove underscore
    result = re.sub(r'_', eps, result)
    
#remove +..
    result = plusdotdot.sub(eps, result)
    
    
#remove [<] and preceding <> on purpose before [//]
    result = ltre1.sub( r'\1 ', result)

#remove [<]   on purpose before [//]
    result = ltre2.sub( space, result)

#remove [>] and preceding <> 
    result = gtre1.sub(r'\1 ', result)
    
#remove [>]   
    result = gtre2.sub(space, result)
    
    
#remove [//] keep preceding part between <>, drop <> 
    result = doubleslash1.sub( r'\1', result)
    
#remove [//] keep preceding word 
    result = doubleslash2.sub(eps, result)
    
# remove [!] and <> around preceding text    p.68
    result = exclam1.sub(r'\1', result)
    
#remove [!] p.68
    result = exclam2.sub(space, result)


#remove [/] keep preceding part between <> this line and following one: crucial order
    result = slash2.sub( r'\1', result)

#remove [/] keep the word before
    result = slash1.sub(eps, result)
#    result = re.sub(r'\[<\]', '', result)


#remove [?] and preceding <>
    result = qre1.sub(r'\1 ', result)
    
# remove [?]
    result = qre2.sub(space, result)
    
#remove [=! <text>] and preceding <>
    result = eqexclam.sub(r'\1 ', result)

#remove [= <text> ] and preceding <> 
    result = eqtext1.sub(r'\1 ', result)

#remove [= <text>] 
    result = eqtext2.sub(space, result)

#replace word [: text] by text
    result = colonre.sub(r'\1 ', result)

#remove [!!]
    result = doubleexclam.sub(space, result)

#remove +"/. p. 64-65    
    result = endquote.sub(eps, result)

#remove +/. +/? +//. +//?
    result = plus3.sub(r' ', result)
    
#remove +.  +^ +< +, ++ +" (p. 64-66)    
    result = plus2.sub(r' ', result)

#remove +".    (p. 65)  +!? (p. 63)
    result = plusquote.sub(r' ', result)
    
#remove silence marks (.) (..) (...) done above see pauses
#    result = re.sub(r'\(\.(\.)?(\.)?\)', r' ', result)

#remove superfluous spaces etc. this also removes CR etc
#    result = result.strip() 
    return(result)
#end function cleantext

def isNotEmpty(str):
   if str is None:
       result = False
   elif str=='':
       result=False
   else:
       result=True
   return(result)    

chaexts=['.txt']
defaultoutext = '.txt'
checkpattern = re.compile(r'[][\(\)&%@/=><_]')
# + should not occur except as compund marker black+board
pluspattern = re.compile(r'\W\+|\+\W')
    
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", default="",
                  help="process the given file (default: None)")
parser.add_option("-l", "--logfile", dest="logfilename", 
                  help="logfile (default sys.stderr)")
parser.add_option("-p", "--path",
                   dest="path", default=".",
                  help="path of the files to be processed")
parser.add_option("--exts", dest="exts",  default = chaexts, help="Extensions of the files to be processed")
parser.add_option("--outext", dest="outext",  default = defaultoutext, help="Extension of the processed files")
parser.add_option("--verbose", dest="verbose", action="store_true", default=False,  help="show files being processed (default=False)")
parser.add_option( "--outpath",
                   dest="outpath", default=".",
                  help="(relative path where the processed files will be put")


(options, args) = parser.parse_args()


if isNotEmpty(options.logfilename):
    logfile = open(options.logfilename, 'w', encoding='utf8')    
else:
    logfile = sys.stderr

#read metadata from the cdc file

#determine the CHA files to be processed

if isNotEmpty(options.filename) :
    files = [options.filename]
elif isNotEmpty(options.path):
    files=[]
    for root, dirs, thefiles in os.walk(options.path):
        for file in thefiles: 
            fullname=os.path.join(root,file)
            (base, ext) = os.path.splitext(file)
            if ext in options.exts: files.append(fullname)


for fullname in files:
    with open(fullname, 'r', encoding='utf8') as thefile:
        if options.verbose: print("processing {}...".format(fullname), file=logfile)
        baseext = os.path.basename(fullname)
        (base,ext) = os.path.splitext(baseext)
        inpath = os.path.dirname(fullname)
        outfullpath= os.path.join(os.getcwd(), options.outpath, inpath)
        if not os.path.isdir(outfullpath):
            os.makedirs(outfullpath)
        outfilename = base + options.outext
        outfullname = os.path.join(outfullpath,outfilename)
        outfile = open(outfullname, 'w', encoding='utf8')  

        lineno = 0
        for line in thefile:
            lineno += 1
            strippedline = line.strip()
            if strippedline[0:6].lower()=='##meta':
                newline= line
            else:
                newline = cleantext(line)
                checkline(newline,outfilename,lineno, logfile)
                if checkpattern.search(newline) or pluspattern.search(newline):
                    print(outfilename, lineno, 'suspect character', file=logfile)
                    print('input=<{}>'.format(line[:-1]), file=logfile )
                    print('output=<{}>'.format(newline[:-1]), file=logfile)

            print(newline, file=outfile, end='') 

#main loop



#end main loop

