#!/bin/env python

# Utility functions to manage and navigate samples
#
# davide.gerbaudo@gmail.com
# Mar 2013

import re

def parseSusyntSampleName(samplename='', verbose=False) :
    "Parse a sample name and split it into meaningful parts"
    # template sample name:
    # user.sfarrell.mc12_8TeV.174834.Sherpa_CT10_llll_ZZ.SusyNt.e1721_s1581_s1586_r3658_r3549_p1328_n0127
    rep = re.compile('user\.(?P<user>.*?)\.'   # user (non greedy)
                     +'(?P<sample>.*?)\.'      # sample (non greedy)
                     +'SusyNt\.'
                     +'(?P<tag>.*)') # tag is the last token (greedy), everything that's left
    match = rep.search(samplename)
    if not match :
        if verbose : print "cannot parse '%s'"%samplename
        return
    return dict([(k, match.group(k)) for k in ['user','sample','tag']])

def dsidFromSampleName(samplename='', verbose=False) :
    "extract the dsid from a sample name"
    rep = re.compile('mc12_8TeV\.(?P<dsid>\d+?)\.') # debuggex.com/r/UnMWCf-3lTSOhn0h/0
    match = rep.search(samplename)
    if not match :
        if verbose : print "cannot parse '%s'"%samplename
        return
    return dict([(k, match.group(k)) for k in ['dsid']])

def nttag(alltags) :
    return alltags[alltags.rfind('_n')+1:]

def minimalSampleName(samplename='',verbose=False) :
    return parseSusyntSampleName(samplename,verbose)['sample']
