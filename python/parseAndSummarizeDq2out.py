#!/bin/env python

# Summarize the information collected with bash/dq2ls_scan.sh
#
# davide.gerbaudo@gmail.com
# 2013-11-25

from collections import defaultdict
inputFile = '/home/gerbaudo/dq2ls_scan.out'

mb2gb = 1.0/1024.0
tb2gb = 1024.0

conversion = {'TB':tb2gb, 'GB':1.0, 'MB':mb2gb}

nFiles = defaultdict(int)
nBites = defaultdict(float)

file = None

for l in open(inputFile).readlines() :
    if not l : continue
    elif 'file :' in l :
        file = l.split(':')[1].strip()
        continue
    elif 'total files:' in l :
        nFiles[file] += int(l.split(':')[1])
        continue
    elif 'total size:' in l :
        size = l.split(':')[1]
        bites, unit = size.split()
        nBites[file] += float(bites)*conversion[unit]
totNfiles, totSize = 0, 0.0
for f in nFiles.keys() :
    print "%s : %d files, %.1fGB"%(f, nFiles[f], nBites[f])
    totNfiles += nFiles[f]
    totSize += nBites[f]
print "total : %d files, %.1fGB"%(totNfiles, totSize)
