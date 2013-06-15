#!/bin/env python

# Script to update the counts in 'data' for a specific tag.
#
# A separate branch of this repository is created for each SusyNt
# production.
# This is done in order to facilitate the comparison across
# productions, and to allow updates within each production.
# The production branches are supposed to track only the count
# evolution; the code evolution should be tracked on the master branch.
#
# Requirements:
# - python >=2.6
# - root and pyroot
# - permission to push stuff to github (ssh keys)
#
# Main steps:
# - checkout relevant branch for this tag (create one if needed)
# - count events
# - push to github
#
# Example usage
#   > updateCounts.py n0143
#
# davide.gerbaudo@gmail.com, Jun 2013

import datetime
import os
import subprocess
import shutil
import sys

logRepoUrl="git@github.com:davidegerbaudo/susynt-prod-log.git"
logRepo   = logRepoUrl[logRepoUrl.rfind('/'):logRepoUrl.rfind('.')]
# wiki not needed for now, but might automatize stuff here soon
#WIK_REPO="git@github.com:davidegerbaudo/susynt-prod-log.wiki.git"
tmpDir="/tmp/%s/log-%s"%(os.environ['USER'], datetime.date.today().isoformat())
verbose=True 

if len(sys.argv)<2 :
    print "Usage: updateCounts.py tag"
    sys.exit(0)
tag = sys.argv[1]

class Chdir:
    "safe cd; see http://stackoverflow.com/questions/431684/how-do-i-cd-in-python"
    def __init__( self, newPath ):
        self.savedPath = os.getcwd()
        os.chdir(newPath)
    def __del__( self ):
        os.chdir( self.savedPath )
def getCommandOutput(command):
    "lifted from github.com/elaird/supy/utils/io.py"
    p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    stdout,stderr = p.communicate()
    return {'stdout':stdout, 'stderr':stderr, 'returncode':p.returncode}
def hasRemoteBranch(branch) :
    cmd = 'git branch -r '
    return branch in getCommandOutput(cmd)['stdout']
def checkoutBranch(tag, branchExist) :
    cmd = ("git checkout -b %s origin/%s"%(tag, tag) if branchExist
           else "git checkout -b %s"%tag)
    stdout = getCommandOutput(cmd)['stdout']
    if verbose : print stdout
def commitCounts() :
    cmd = "git commit -m 'autoupdate' data/counts/*txt"
    if verbose : print cmd
    getCommandOutput(cmd)
def pushToRemoteBranch(branch) :
    if verbose : print 'git push origin '+branch
    getCommandOutput('git push origin '+branch)
def count(type, tag, weighted=False) :
    assert type in ['data12','mc12','susy']
    if weighted : assert type in ['mc12', 'susy']
    inputDir = '/gdata/atlas/ucintprod/SusyNt/'+type+'_'+tag
    outFname = './data/counts/'+type+'_'+('gen' if weighted else 'raw')+'.txt'
    cmd  = './python/countEventsPerSample.py'
    cmd += ' --gen' if weighted else ''
    cmd += ' '+inputDir
    cmd += ' > '+outFname
    if verbose : print cmd
    getCommandOutput(cmd)
def isMc(type) : return type in ['mc12', 'susy']

dirs = [] # prevent cd object from being garbage-collected too early
branchName = tag
if os.path.isdir(tmpDir) : shutil.rmtree(tmpDir) # start from a clean directory
os.mkdir(tmpDir)
dirs.append(Chdir(tmpDir))
getCommandOutput('git clone '+logRepoUrl)
dirs.append(Chdir(tmpDir+'/'+logRepo))
checkoutBranch(branchName, hasRemoteBranch(branchName))
for type in ['data12', 'mc12', 'susy'] :
    count(type, tag)
    if isMc(type) : count(type, tag, weighted=True)
if verbose : getCommandOutput('git status')
commitCounts()
pushToRemoteBranch(branchName)
