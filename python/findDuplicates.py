#!/bin/env python

# Find samples that have been processed and copied multiple times.
#
# Details:
#Samples are identified by their dataset id. This will catch samples
#that have been multiply processed by different users or with
#different tags.
#
# davide.gerbaudo@gmail.com
# July 2013

import collections
import os
import sys

from sampleUtils import dsidFromSampleName

def findDuplicates(basedir, printDuplicates=True) :
    dsidDirs = collections.defaultdict(list)
    dirs = [basedir+'/'+d for d in os.listdir(basedir) if os.path.isdir(basedir+'/'+d)]
    for d in dirs : dsidDirs[dsidFromSampleName(d)['dsid']].append(d)
    multiple = dict((k, v) for k, v in dsidDirs.items() if len(v)>1)
    lines = ["%s -> %d : \n\t%s"%(k, len(v), '\n\t'.join(v))
             for k, v in multiple.items()]
    if printDuplicates : print '\n'.join(lines)
    return multiple

if __name__=='__main__' :
    assert len(sys.argv)>1, "Usage: %s dir1 [dir2 ...]"%sys.argv[0]
    dirs = [p for p in sys.argv[1:] if os.path.isdir(p)]
    for d in dirs : findDuplicates(d)
