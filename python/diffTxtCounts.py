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
    return "{0:.1f}".format(100.*(v-vr)/vr) if v is not None and vr and v!=vr else '--'

counts      = dict([(f, countsFromFile(f)) for f in inputfiles])
allDatasets = sorted(list(set([d for cnts in counts.values() for d in cnts.keys()])))
fnP, fnS    = commonPrefix(inputfiles), commonSuffix(inputfiles)
dsP, dsS    = commonPrefix(allDatasets), commonSuffix(allDatasets)
refFn       = inputfiles[0]
refCnt      = dict([(s, counts[refFn][s] if s in counts[refFn] else None) for s in allDatasets])

defaultCol0W = 64
col0W = max([defaultCol0W, min([len(f if fullnames else shorten(f,fnP, fnS)) for f in allDatasets])])
hrule = '-'*(col0W + (2*len(inputfiles)-1)*colW)
cell0, cell = '{0:<'+str(col0W)+'}', '{0:>'+str(colW)+'}'

# build table
header = cell0.format('')\
         +cell.format(refFn if fullnames else shorten(refFn, fnP, fnS))\
         +''.join([cell.format(s) for sd in [(f if fullnames else shorten(f, fnP, fnS), 'delta[%]')
                                             for f in inputfiles[1:]]
                   for s in sd])
lines = []
for s in allDatasets :
    cds = [(c, formattedPercentDelta(c, cr))
           for c,cr in [(counts[f][s] if s in counts[f] else None,
                         refCnt[s]    if s in refCnt    else None)
                        for f in inputfiles[1:]]]
    cds = [c for cd in cds for c in cd] # flatten
    lines.append(cell0.format(s if fullnames else shorten(s, dsP, dsS))
                 + cell.format(refCnt[s] if s in refCnt else '--')
                 + ''.join([cell.format(c) if c is not None else '--' for c in cds]))
print header
print hrule
print '\n'.join(lines)
print hrule

