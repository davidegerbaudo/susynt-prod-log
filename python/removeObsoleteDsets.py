#!/bin/env python
#
# Get all sample directories from a given directory, and delete the ones that have multiple tags after prompting for a preferred tag
#
# davide.gerbaudo@gmail.com
# Mar 2013

import collections, glob, os, sys

inputDir = 'None'
#inputDir = '/gdata/atlas/ucintprod/SusyNt/mc12_n0127'
skipEmptyDirs = True

while not os.path.isdir(inputDir) : inputDir = raw_input("Directory to cleanup: ")

def splitBaseTag(s) :
    i = s.rfind('_')
    return s[:i], s[i:]

processedSamples = []
multipleSamples  = dict()
sampleDirs       = [p for p in glob.glob(inputDir+'/*') if os.path.isdir(p)]
samplesWithTags  = collections.defaultdict(list)

for sd in sampleDirs :
    s, t = splitBaseTag(sd)
    if skipEmptyDirs and os.listdir(sd) == [] : continue
    samplesWithTags[s].append(t)
samplesWithMultipleTags = dict([(s,tuple(sorted(t))) for s,t in samplesWithTags.iteritems() if len(t)>1])
possibleTags = set([frozenset(tags) for tags in samplesWithMultipleTags.values()])

def chooseTag(tags) :
    tags = list(tags)
    print "please choose one of the following tags:"
    print '\n'.join("[%d] %s"%(i,t) for i,t in enumerate(tags))
    i = -1
    while i not in range(len(tags)) : i = int(raw_input("choice: "))
    return tags[i]

preferredTags = dict([(tags, chooseTag(tags)) for tags in possibleTags])

for sample, tags in samplesWithMultipleTags.iteritems() :
    chosenTag = preferredTags[frozenset(tags)]
    for t in tags :
        if t!=chosenTag : print "rm -rf %s%s"%(sample,t)
