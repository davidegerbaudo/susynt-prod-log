#!/bin/env python
#
# Count the number of events processed producing SusyNtuple for a given set of samples
# Run without arguments to get the help message.
#
# davide.gerbaudo@gmail.com
# 2013-03

import glob, optparse, os, re, sys
import sampleUtils

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True # don't let root steal your cmd-line options
r.gROOT.SetBatch(1)                        # go batch!
r.gErrorIgnoreLevel = 9999                 # suppress messages about missing dict
                                           # (can't get rid of the 'duplicate' ones?)



defaultBinLabel = 'Initial'
rawHistoName, genHistoName = 'rawCutFlow', 'genCutFlow'
usage = ("Usage : %prog [options] args"
         "\n Examples :"
         "\n %prog  -r 'Sherpa_CT10.*(WW|VV)' /gdata/atlas/ucintprod/SusyNt/mc12_n0127/"
         "\n %prog  -r 'n0127b' /gdata/atlas/ucintprod/SusyNt/*_n0127/"
         )

parser = optparse.OptionParser(usage = usage)

parser.add_option("--gen", dest="gen", default=False, action="store_true", help='weighted counts (default raw counts)')
parser.add_option("-b", "--bin-label", dest="binlabel", default=defaultBinLabel)
parser.add_option("-r", "--regex", dest="regex", default=None)
parser.add_option("--print-bin-labels", dest="printbinlabels", default=False, action="store_true")
parser.add_option("--full-names", dest="fullnames", default=False, action="store_true")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true")

(options, args) = parser.parse_args()
inputdirs       = args
gen             = options.gen
histoName       = genHistoName if gen else rawHistoName
binLabel        = options.binlabel
printBinLabels  = options.printbinlabels
regex           = options.regex
fullnames       = options.fullnames
verbose         = options.verbose

if verbose :
    print "Using the following options:"
    print '\n'.join(["%s : %s"%(s, eval(s)) for s in ['inputdirs','histoName','binLabel','printBinLabels','regex','fullnames']])

sampleDirs = sorted([t for t in [d  for inputdir in inputdirs for d in glob.glob(inputdir+'/*')]
                     if os.path.isdir(t) and (re.search(regex, t) if regex else True)])

def getProcessedEvents(filename, histoName='', binLabel='', printBinLabels=False) :
    f = r.TFile.Open(filename)
    histo = f.Get(histoName)
    h = histo
    if printBinLabels : print [h.GetXaxis().GetBinLabel(i) for i in range(1,1+h.GetNbinsX())]
    processedEvents = histo.GetBinContent(histo.GetXaxis().FindBin(binLabel))
    f.Close()
    return processedEvents

shortname = sampleUtils.minimalSampleName

if verbose : print '-'*60
for sd in sampleDirs :
    container = os.path.basename(sd)
    files = glob.glob(sd+'/'+'*.root*')
    nEntries = sum([getProcessedEvents(f, histoName, binLabel, printBinLabels) for f in files])
    print (container if fullnames else shortname(container)) + ' : '+str(nEntries)
    continue
