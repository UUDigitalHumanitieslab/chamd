#!/usr/bin/env python3
"""
Created on Wed Dec  7 15:53:51 2016

@author: Odijk101
"""


from optparse import OptionParser
import datetime
import os
import sys
import re
import csv
from chamd import cleanCHILDESMD

#functions

charmap = {}

def clean(line):
    result = line.strip()
    return(result)
    
def combine(str1,str2):
    result = str2 if str1 == "" else space.join([str1[:-1], str2])
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
  if str[0:1]==mdchar:
      result = str[1:0]
  else:
      result is None
  return(result)     

def getcorpus(metadata):
    spkr=metadata['speaker'] if 'speaker' in metadata else ''
    if 'id' in metadata and spkr in metadata['id'] and 'corpus' in metadata['id'][spkr]:
        corpus = metadata['id'][spkr]['corpus']
    else:
        corpus = 'Unknown_corpus'
    return(corpus)    
    
  
def getmonths(age):
    #input format is 3;6.14 (y;m.d)
    #also accept y.m.d and y;m;d and y.m;d with a warning or any separators for that matter
    cleanage=clean(age)
    errorfound=False
    warningneeded=False
    monthstr = ""
    yearstr = ""
    thelist = re.split(seps,cleanage)
    lthelist = len(thelist)
    #print(age, thelist, file=logfile)
    #print(input('continue?'), file=logfile)
    if lthelist >= 1:
        yearstr=thelist[0]
        if not re.match('[0-9]+',yearstr):
           errorfound = True
    if lthelist >= 2:
        monthstr=thelist[1]
        if not re.match('[0-9]{1,2}', monthstr):
            errorfound = True
    if lthelist < 1 or lthelist > 3:
        errorfound = True
    if not errorfound:
        if not re.match(agere,cleanage):
            warningneeded = True
        year=int(yearstr)
        month=0 if monthstr == "" else int(monthstr)
        if month < 0 or month > 11:
            print("Warning: Illegal month value in age(0<=m<=11): {}".format(cleanage), file=logfile)
        result= 12*year + month
    else:
        result = 0
        print("Error: uninterpretable age value: {}. No months attribute computed".format(cleanage), file=logfile)
    if warningneeded:
        print("Warning: Illegal age syntax for {}. Syntax must be y;m.d".format(cleanage), file=logfile)
    return(result)
    
def getoutpaths(fullname, inpath, outpath):
    absinpath = os.path.abspath(inpath)
    absoutpath = os.path.abspath(outpath)
    fullinpath = os.path.dirname(fullname)
    reloutpath = os.path.relpath(fullinpath, start=absinpath)
    fulloutpath = os.path.join(absoutpath, reloutpath)
    return(reloutpath, fulloutpath)
    
def getparsefile(corpus,base,uttid):
    uttidstr = "u{:011d}".format(uttid)
    newbase=underscore.join([corpus,base,uttidstr])
    result = newbase + parseext
    return(result)
    
def isNotEmpty(str):
   if str is None:
       result = False
   elif str=='':
       result=False
   else:
       result=True
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
        normalizeddate = d.isoformat()
        super().__init__(el, "date", str(normalizedate))

class MetaInt(MetaValue):
    def __init__(self, el, metadata):
        super().__init__(el, "int", str(metadata[el]))

class MetaTxt(MetaValue):
    def __init__(self, el, metadata):
        super().__init__(el, "text", metadata[el])    

def normalizedate(str):
    try:
        dt=datetime.datetime.strptime(str, dateformat1)
    except ValueError:
        try:
            dt=datetime.datetime.strptime(str, dateformat2)
            #print("Date {} interpreted as dd-mm-yyyy".format(str), file=logfile)
        except ValueError:
            print("Date {} cannot be interpreted".format(str), file=logfile)
            exit(1)
    d=dt.date()        
    return(d)

   
def print_headermd(metadata, outfile):
    for el in metadata:
        if el in donotprintinheaders:
            pass
        elif el in allheaders:
            curval = metadata[el]
            if type(curval) is str:
                line = MetaTxt(el, metadata)
                print(line, file=outfile)
            elif type(curval) is datetime.date:
                line = MetaDate(el, metadata)
                print(line, file=outfile)
            elif type(curval) is int:
                line = MetaInt(el, metadata)
                print(line, file=outfile)
            if el not in  printinheaders:
                print("unknown metadata element encountered: {}".format(el), file=logfile)

def print_uttmd(metadata, outfile):
    uttidline = MetaInt('uttid', metadata)
    spkrline = MetaTxt("speaker", metadata)
    #parsefileline = MetaTxt('parsefile', metadata)
    origuttline = MetaTxt("origutt", metadata)
    print(uttidline, file=outfile)
    print(spkrline, file=outfile)
    #print(parsefileline, file=outfile)
    print(origuttline, file=outfile)
    curcode= metadata['speaker']
    if curcode in metadata['participants']:
        for el in metadata['participants'][curcode]:
            if el != 'role':
                theline = MetaTxt(el, metadata['participants'][curcode])
                print(theline, file=outfile)
    if 'id' in metadata:        
        if curcode in metadata['id']:
            for el in metadata['id'][curcode]:
                curval = metadata['id'][curcode][el]

                if type(curval) is str:
                    theline = MetaTxt(el, metadata['id'][curcode])
                    print(theline, file=outfile)
                elif type(curval) is int:
                    theline = MetaInt(el, metadata['id'][curcode])
                    print(theline, file=outfile)
                elif type(curval) is datetime.date:
                    theline = MetaDate(el, metadata['id'][curcode])
                    print(theline, file=outfile)
                else:
                    print('print_uttmd: unknown type for {}={}'.format(el,curval), file=logfile)

def processline(base, cleanfilename, lineno, line, md, uttid, headermodified, outfilename):
    startchar= line[0:1] 
    if startchar == mdchar:
        #to implement
        treat_mdline(lineno, line, metadata)
        headermodified = True
#        print(metadata, file=mdlog)
    else:
        if headermodified: 
            print_headermd(metadata, outfile)
            print('\n\n', file=outfile)
            headermodified = False
        if startchar == uttchar:
            metadata['uttid']=uttid
            treatutt(line, metadata)
            corpus = getcorpus(metadata)
            parsefilename=getparsefile(corpus,base,uttid)
            metadata['parsefile']=parsefilename
            endspk =line.find(':')
            if endspk < 0 : print('error in line: {}'.format(line), file=logfile)
            entry=line[endspk+2:]
            cleanentry=cleanCHILDESMD.cleantext(entry)
            if isNotEmpty(cleanfilename):
                write2cleanfile(entry, cleanentry, cleanfile)
            cleanCHILDESMD.checkline(line, cleanentry,outfilename,lineno, logfile)
            updateCharMap(cleanentry, charmap)

            print_uttmd(metadata,outfile)
            print(cleanentry, file=outfile)
            print('\n',file=outfile)
            uttid += 1
        elif startchar == annochar:
            #to be implemented
            pass
        else:    
            print(line, file=outfile)                    
    return(uttid, headermodified)               
                    
def setatt(entrylist, i):
    lentrylist = len(entrylist)
    if lentrylist > i:
        result=clean(entrylist[i])
    else:
        result = ""
    return(result)

                    
def treat_mdline(lineno, headerline, metadata):
   headernameend= headerline.find(headerlineendsym) 
   if headernameend<0:
       cleanheaderline = clean(headerline).lower()
       if cleanheaderline == "@utf8":
           metadata["charencoding"]="UTF8"
       elif cleanheaderline == "@begin":
          pass
       elif cleanheaderline == "@end":
           pass
       elif cleanheaderline == '@blank':
          pass
       else:
           print("Warning: unknown header {} encountered in line {}".format(headerline, lineno), file=logfile)
          
   else:
       headername= headerline[1:headernameend]
       entry = headerline[headernameend+1:]
       cleanentry= clean(entry)
       entrylist = cleanentry.split(',')
       cleanheadername = clean(headername)
       cleanheadernamebase = clean(cleanheadername[:-3])
       headerparameter = cleanheadername[-3:]
       cleanheadername = cleanheadername.lower()
       cleanheadernamebase = clean(cleanheadername[:-3])
       if cleanheadername == 'font':
           pass
       elif cleanheadername == 'languages':
           metadata['languages']= entrylist
       elif cleanheadername == 'colorwords':
           metadata['colorwords'] = entrylist
       elif cleanheadername == 'options':
           pass
       elif cleanheadername == 'participants':
           treatparticipants(entrylist,metadata)
       elif cleanheadername == 'id':
           treatid(entry, metadata)
       elif cleanheadername == 'date':
           metadata[cleanheadername]=normalizedate(cleanentry)
       elif cleanheadername in simpleheadernames:
           metadata[cleanheadername]= cleanentry
       elif cleanheadername in skipheadernames:
           pass
       elif cleanheadername in simpleintheadernames:
           metadata[cleanheadername] = int(cleanentry)    
       elif cleanheadername in simplecounterheaders:
           counter[cleanheadername] += 1
           metadata[cleanheadername] = counter[cleanheadername] 
       elif cleanheadernamebase in participantspecificheaders:
           if 'id' not  in metadata: metadata['id']={}
           if headerparameter not in metadata['id']: metadata['id'][headerparameter]={}
           if cleanheadernamebase == 'birth of':
               thedate=normalizedate(cleanentry)
               metadata['id'][headerparameter][cleanheadernamebase]=thedate
           elif cleanheadernamebase == 'age of':
               #print('<{}>'.format(cleanentry), file=logfile)
               #print(input('Continue?'), file=logfile) 
               metadata['id'][headerparameter]['age']=cleanentry
               months=getmonths(cleanentry)
               if months != 0: metadata['id'][headerparameter]['months']=months
           else:
               metadata['id'][headerparameter][cleanheadernamebase]=cleanentry

       else:
           print('Warning: unknown metadata element encountered: {}'.format(cleanheadername), file=logfile)


           
def treatparticipants(entrylist, metadata):
   for el in entrylist:
       ellist = el.split()
       ctr = 0
       code = ""
       name = ""
       role = "" 
       if len (ellist)== 3:
           code=ellist[0]
           name = ellist[1]
           role = ellist[2]
       elif len(ellist)==2:
           code = ellist[0]
           name = ""
           role = ellist[1]
       else: print ("error in participants: too few elements {}".format(entrylist), file=logfile)
       if code != "":
           if "participants"not in metadata: metadata["participants"]={}
           if code not in metadata["participants"]: metadata["participants"][code]={}
           if role != "": metadata["participants"][code]["role"]=role   
           if name != "": metadata["participants"][code]["name"]=name



          
def treatid(entry,metadata):
    cleanentry = clean(entry)
    entrylist= cleanentry.split(idsep)
    lentrylist = len(entrylist)
    if lentrylist!=11:
        print ("Warning in id: {} elements instead of 11 in {}".format(lentrylist,entry), file=logfile)
    language= setatt(entrylist,0)
    corpus  = setatt(entrylist,1)
    code = setatt(entrylist,2)
    age = setatt(entrylist,3)
    sex = setatt(entrylist,4)
    group = setatt(entrylist,5)
    SES = setatt(entrylist,6)
    role = setatt(entrylist,7)
    if role == '':
        if code in metadata["participants"] and "role" in metadata["participants"][code]:
            role =metadata["participants"][code]["role"]
    education = setatt(entrylist,8)
    custom = setatt(entrylist,9)
    if code == "":
        print ("error in id: no code element in {}".format(entry), file=logfile)
    else:
        if "id" not in metadata: metadata["id"]={}
        if code not in metadata["id"]: metadata["id"][code]={}    
        if language != "": metadata["id"][code]["language"]=language
        if corpus != "": metadata["id"][code]["corpus"]=corpus
        metadata["id"][code]["age"]=age
        if age != "": 
            months = getmonths(age)
        else:
            months = ''            
        metadata["id"][code]["months"]=months
        metadata["id"][code]["sex"]=sex
        metadata["id"][code]["group"]=group
        metadata["id"][code]["SES"]=SES
        metadata["id"][code]["role"]=role
        metadata["id"][code]["education"]=education
        metadata["id"][code]["custom"]=custom
        
def treatutt(line, metadata):
   endspk= line.find(':') 
   code = line[1:endspk]
   metadata["speaker"]=code
   metadata['origutt']= line[endspk+1:-1]

def updateCharMap(str, charmap):
    for i in range(len(str)):
        curchar = str[i]
        if curchar in charmap:
            charmap[curchar] += 1
        else:
            charmap[curchar] = 1
   

def write2cleanfile(entry, cleanentry, cleanfile):
    if entry != cleanentry:
        print(entry, file=cleanfile, end ='' )
        print(cleanentry, file=cleanfile, end='')
        
#constants

tab = '\t'
myquotechar = '"'
chaexts = [".cha", '.cex']
mdchar = "@"
uttchar ="*"
annochar = "%"
defaultoutext = ".txt"
headerlineendsym =':'
idsep = '|'
metakw = '##META'
space = ' '
parseext= ".xml"
underscore = '_'
dateformat1="%d-%b-%Y"
dateformat2="%d-%m-%Y"


simpleheadernames = ['pid',  "transcriber",  "coder",  "date",  "location", 
                      "situation", 'number', 'interaction type', "activities",
                      'comment', 'bck', 'warning', 'transcription',
                     'time start', 'time duration', 'tape location', 'room layout',
                     'recording quality', 'number', 'media', 'session']
simpleintheadernames = ['g', 'page']
simplecounterheaders = ['new episode']
skipheadernames =['exceptions']
participantspecificheaders = ['birth of', 'birthplace of', 'l1 of', 'age of']
createdmdnames = ['charencoding', 'parsefile', 'speaker', 'origutt']
seps = r'[-.,/;:_!~\\]'
digits=r'[0-9]+'
digit2=r'[0-9]{1,2}'
optdays = r'(' +digits + r')?'
optsepdays = '(\.' + optdays + r')?'
optmonths = '(' + digit2 + optsepdays + ')?'
optsepmonths = '(;'  + optmonths + ')?'
agere = '^' + digits + optsepmonths + '$'
donotprintinheaders = ['id','participants','languages', 'colorwords','options','uttid','parsefile', 'speaker', 'origutt' ]
allheaders = simpleheadernames + simpleintheadernames + simplecounterheaders + createdmdnames + participantspecificheaders 
printinheaders = [headeratt for headeratt in allheaders if headeratt not in donotprintinheaders]

# global variables
metadata = {}
outfile = None
logfile = None

def main(args=None):
    global metadata, outfile, logfile

    """
    Main entry point.
    """
    if args is None:
        args = sys.argv[1:]

    baseversion = "0"
    subversion = "03"
    version = baseversion +  "." + subversion
    exactlynow = datetime.datetime.now()
    now = exactlynow.replace(microsecond=0).isoformat()



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
    parser.add_option( "--cleanfilename",
                    dest="cleanfilename", default="",
                    help="file to write processed utterances to")
    parser.add_option("--exts", dest="exts",  default = chaexts, help="Extensions of the files to be processed")
    parser.add_option("--outext", dest="outext",  default = defaultoutext, help="Extension of the processed files")
    parser.add_option("--verbose", dest="verbose", action="store_true", default=False,  help="show files being processed (default=False)")
    parser.add_option( "--outpath",
                    dest="outpath", default=".",
                    help="path where the processed files will be put")


    (options, args) = parser.parse_args(args)

    if isNotEmpty(options.logfilename):
        logfile = open(options.logfilename, 'w', encoding='utf8')    
    else:
        logfile = sys.stderr

    if isNotEmpty(options.charmapfilename):
        charmapfilename = options.charmapfilename
    else:
        charmapfilename = "charmap.txt"    

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

    if isNotEmpty(options.cleanfilename):
        cleanfile = open(options.cleanfilename,'w',encoding='utf8')

    for fullname in files:
    #    thefile= open(fullname, 'r', encoding='utf8')
    #    charencodingline = thefile[0]
    #    thefile.close()
    #    charencoding = get_charencoding(charencodingline)
    #   if charencoding is None:
    #        print("No character encoding encountered in {}".format(fullname), file=logfile)
        with open(fullname, 'r', encoding='utf8') as thefile:
            if options.verbose: print("processing {}...".format(fullname), file=logfile)
    #        mdlog = open('mdlog.txt', 'w', encoding='utf8')
            baseext = os.path.basename(fullname)
            (base,ext) = os.path.splitext(baseext)
            metadata['session'] = base
            
            absinpath = os.path.abspath(options.path)
            (initpath,lastfolder) = os.path.split(options.path)
            absoutpath = os.path.abspath(options.outpath)
            fullinpath = os.path.dirname(fullname)
            reloutpath = os.path.relpath(fullinpath, start=absinpath)
            outfullpath = os.path.join(absoutpath, lastfolder, reloutpath)

            #print('fullinpath=<{}>'.format(fullinpath), file=sys.stderr)
            #print('outfullpath=<{}>'.format(outfullpath), file=sys.stderr)
            #print('', file=sys.stderr)
            
            if not os.path.isdir(outfullpath):
                os.makedirs(outfullpath)
            outfilename = base + options.outext
            outfullname = os.path.join(outfullpath,outfilename)
            outfile = open(outfullname, 'w', encoding='utf8')
            lineno = 0
            uttid = 0
            counter = {}
            for el in simplecounterheaders: counter[el] = 0
            headermodified = False
            linetoprocess=""
            for line in thefile:
                lineno += 1
                startchar = line[0:1]
                if startchar in ['\t']:
                    linetoprocess = combine(linetoprocess, line)
                elif startchar in [mdchar,uttchar,annochar,space]:
                    if linetoprocess != "":
                        (uttid, headermodified) = processline(base, options.cleanfilename, lineno, linetoprocess, metadata, uttid, headermodified, outfilename)
                    linetoprocess = line
                #print(metadata, file=logfile)
                #print(input('Continue?'), file=logfile)        
            #deal with the last line
            (uttid, headermodified) = processline(base, options.cleanfilename, lineno, linetoprocess, metadata, uttid, headermodified, outfilename)

    hexformat = '{0:#06X}'
    #hexformat = "0x%0.4X"
    charmapfile = open(charmapfilename, 'w', encoding='utf8')
    charmapwriter = csv.writer(charmapfile,delimiter=tab, quotechar=myquotechar, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    for el in charmap:
        ordel = ord(el)
        therow = [el, ordel , hexformat.format(ordel), charmap[el]]    
        charmapwriter.writerow(therow)             
    #read metadata from the CHA file 

    #first read the character encoding

    #and convert it to PaQu style plain text metadata annotations

    #and convert it to LASSY XML meta elements and integrate with a Alpino-parsed  XML-file

    #and convert it to FoliA
if __name__ == "__main__":
    main()
