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
parser.add_option('-w', '--col-width', dest='colwidth', default=8, type=int)
parser.add_option('-f', "--full-names", dest='fullnames', default=False, action='store_true', help='keep full names as table headers (by default strip common prefix/suffix)')
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true")

(options, args) = parser.parse_args()
inputfiles      = args
colW            = options.colwidth
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
def formattedPercentDelta(v, vr) :
    return "{0:.2f}%".format(100.*(v-vr)/vr) if v is not None and vr and v!=vr else '--'

counts      = dict([(f, countsFromFile(f)) for f in inputfiles])
allDatasets = sorted(list(set([d for cnts in counts.values() for d in cnts.keys()])))
fnP, fnS    = commonPrefix(inputfiles), commonSuffix(inputfiles)
dsP, dsS    = commonPrefix(allDatasets), commonSuffix(allDatasets)

refFn  = inputfiles[0]
refCnt = dict([(s, counts[refFn][s] if s in counts[refFn] else None) for s in allDatasets])
col0W, colW = 64, colW

hrule = '-'*(col0W + (len(inputfiles)+1)*colW)
cell0, cell = '{0:<'+str(col0W)+'}', '{0:>'+str(colW)+'}'

header = ''.join([cell0.format('')]
                 +[cell.format(v) for v in []
                   + [fr if fullnames else shorten(fr, fnP, fnS) for fr in [refFn]]
                   + [c for c in # flatten list [(s,delta),...]
                      [f if fullnames else shorten(f, fnP, fnS), 'delta']
                      for f in inputfiles[1:]]
                   ])

lines = [''.join([cell0.format(s if fullnames else shorten(s, dsP, dsS))]
                 +[cell.format(v) for v in [refCnt[s] if s in refCnt else '--']
                   +[c for c in # flatten
                    [counts[f][s] if s in counts[f] else '--',
                     formattedPercentDelta(counts[f][s] if s in counts[f] else None,
                                           refCnt[s] if s in refCnt else None)]]])
         for s in allDatasets]

print header
print hrule
print '\n'.join(lines)
print hrule
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
