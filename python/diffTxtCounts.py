#!/bin/env python

# Simple script to compare the event counts from N txt files
#
# davide.gerbaudo@gmail.com
# Feb 2013

import os
import optparse

usage = ("Usage : %prog [options] args"
         "\n Examples :"
         "\n %prog  -r file1.txt file2.txt ..."
         "\n"
         "\nInput files are expected to have one line per sample, each formatted as"
         "\n <sample> <counts>"
         "\n   or"
         "\n <sample> : <counts>"
         )

parser = optparse.OptionParser(usage = usage)
parser.add_option('-f', "--full-names", dest='fullnames', default=False, action='store_true', help='keep full names as table headers (by default strip common prefix/suffix)')
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true")

(options, args) = parser.parse_args()
inputfiles      = args
fullnames       = options.fullnames
verbose         = options.verbose
assert len(inputfiles)>1, "need at least two files (run with -h)"
if verbose :
    print "Using the following options:"
    print '\n'.join(["%s : %s"%(s, eval(s)) for s in ['inputfiles','fullnames']])


def isComment(line) : return line.strip().startswith('#')
def hasTwoFields(line) : return len(line.replace(' : ',' ').split())==2
def isValidLine(line) : return len(line) and not isComment(line) and hasTwoFields(line)
def parseLine(line) :
    tokens = line.replace(' : ',' ').strip().split()
    return tokens[0].strip(), float(tokens[1])
def countsFromFile(filename) :
    return dict([(s,c) for s,c in [parseLine(l) for l in open(filename).readlines() if isValidLine(l)]])
def commonPrefix(list) : return os.path.commonprefix(list)
def commonSuffix(list) : return os.path.commonprefix([l[::-1] for l in list])[::-1]
def shorten(name, pref, suff) : return name.lstrip(pref).rstrip(suff).rstrip()

counts      = dict([(f, countsFromFile(f)) for f in inputfiles])
allDatasets = [d for cnts in counts.values() for d in cnts.keys()]
fnamePrefix, fnameSuffix = commonPrefix(inputfiles), commonSuffix(inputfiles)
dsetPrefix,  dsetSuffix  = commonPrefix(allDatasets), commonSuffix(allDatasets)

refFname = inputfiles[0]
refCounts = dict([(s, counts[refFname][s] if s in counts[refFname] else None) for s in allDatasets])
colW = 14

header = ''.join([('%'+str(colW)+'s')%v for v in
                  [''] 
                  + [f if fullnames else shorten(f, fnamePrefix, fnameSuffix) for f in [refFname]]
                  + [c for c in # flatten list [(s,delta),...]
                     [[f if fullnames else shorten(f, fnamePrefix, fnameSuffix), 'delta']
                      for f in inputfiles[1:]]]
                  ])

# for stream in Borge.keys() :
#     cntStrB = Borge[stream]
#     cntStrU1 = n0127[stream]
#     cntStrU2 = n0135[stream]
#     print stream
#     for p in sorted(cntStrB.keys()) :
#         cntB = cntStrB[p]
#         cntU1 = sum([c for k,c in cntStrU1.iteritems() if p in k])
#         cntU2 = sum([c for k,c in cntStrU2.iteritems() if p in k])
#         print ''.join([('%'+str(colW)+'s') % v for v in [p, str(cntB),
#                                                          str(cntU1), ("{0:.4f}%".format(100.*(cntU1-cntB)/cntB) if cntU1!=cntB else '--'),
#                                                          str(cntU2), ("{0:.4f}%".format(100.*(cntU2-cntB)/cntB) if cntU2!=cntB else '--'),
#                                                          ]])
