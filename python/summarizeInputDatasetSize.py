#!/bin/env python

# Collect with pyAMI the info for the SusyNt input datasets
#
# Work in progress; caveats:
# - need to checkout the file lists from SusyCommon/trunk/grid (cached)
# - need both kerberos ticket and voms proxy
# - does not work with data (because they are skimmed? ask ami support)
# - pyAMI can be quite slow; retrieve once, cache to json
#
# davide.gerbaudo@gmail.com
# 2013-11-25

import pyAMI
from pyAMI import endpoint
from pyAMI.client import AMIClient
from pyAMI.endpoint import get_endpoint,get_XSL_URL
from pyAMI.auth import AMI_CONFIG, create_auth_config
import glob
import json
import os
from pyAMI.query import get_dataset_info

import subprocess
import tempfile



def getCommandOutput(command):
    "lifted from supy (https://github.com/elaird/supy/blob/master/utils/io.py)"
    p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    stdout,stderr = p.communicate()
    return {"stdout":stdout, "stderr":stderr, "returncode":p.returncode}                                                                                                                                 
def checkoutDatasetLists() :
    gridDir = tempfile.mkdtemp(suffix='SusyCommon_grid')
    getCommandOutput('svn co svn+ssh://svn.cern.ch/reps/atlasinst/Institutes/UCIrvine/SUSYAnalysis/SusyCommon/trunk/grid '+gridDir)
    return gridDir
def datasetsFromTxtFile(txtfile) :
    def isGoodLine(l) : return 'mc12_8TeV' in l or 'data12_8TeV' in l
    def dsetFromLine(l) :
        tokens = l.split()
        return tokens[0].strip() if len(tokens) else None
    datasets = [dsetFromLine(l) for l in open(txtfile).readlines() if isGoodLine(l)]
    return [d for d in datasets if d is not None]
def json_write(obj, fname) :
    with open(fname, 'w') as out :
        json.dump(obj, out)
def json_read(fname) :
    with open(fname) as inp :
        return json.load(inp)                                                                                                                                                                             
json_dsinfo_file = 'datasets_info.json'
gridDir = '/tmp/tmpaG3qgOSusyCommon_grid'
gridDir = checkoutDatasetLists() if not os.path.exists(gridDir) else gridDir


textFiles = dict()

#textFiles['data'] = [gridDir+'/data12_Egamma.txt', gridDir+'/data12_Muons.txt']
#for g in ['AcerMCPythia',
#           'AlpgenJimmy',
#           'AlpgenPythia',
#           'Herwig',
#           'Jimmy',
#           'MadGraphPythia',
#           'McAtNloJimmy',
#           'PowhegJimmy',
#           'PowhegPythia',
#           'Pythia',
#           'Sherpa',] :
#     textFiles[g] = glob.glob(gridDir+'/'+g+'*txt')
textFiles['susy'] = glob.glob(gridDir+'/p1512/*.txt')

datasets = dict()
for g, ff in textFiles.iteritems() :
    datasets[g] = []
    for f in ff :
        datasets[g].extend(datasetsFromTxtFile(f))

client = AMIClient()
def gdi(ds) :
    di = None
    try:
        di = get_dataset_info(client, ds.strip('/'))
    except Exception, msg:
        # DG 2013-11-25
        # I don't know why it's returning a valid result while throwing an exception
        # Ignore it for now.
        # print Exception
        print 'cannot find ',ds
    return di.info #['totalSize'], di['nFiles'], di['totalEvents']
datasetinfos = dict()
for g, dss in datasets.iteritems() :
    print '---',g,'--- (',len(dss),' datasets)'
    datasetinfos[g] = []
    for ds in dss :
            print ds
            di = gdi(ds)
            datasetinfos[g].append(di)
            print datasetinfos[g]
print datasetinfos
json_write(datasetinfos, json_dsinfo_file)

#         datasetinfos[g] = [gdi(ds) for ds in dss]
#         print datasetinfos[g]

