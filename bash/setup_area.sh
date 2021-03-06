#!/bin/sh

# Script to setup the area for submission of the SusyNt jobs.
#
# Based on Steve's instructions.
# Requirements:
# - access to the svn.cern.ch repositories
# - have 'localSetuPandaClient' defined.
#   This depends on your specifi setup; on gpatlas* these commands are defined with
#   > export ATLAS_LOCAL_ROOT_BASE=/export/home/atlasadmin/ATLASLocalRootBase
#   > source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
# - voms proxy
#
# Main steps:
# - source this script with a tag, for example
#   > source setup_area.sh n0135
# - this will create two directories :
#   - 'prod_n0135' (with all the packages)
#   - 'subm_n0135' (to submit the jobs)
# - check that everything compiled (if not, fix it and 'create_tarball.sh'), then submit the jobs:
#   > ./submit.py mc  -t n0135 --met Default -f <a-sample-list.txt> --nickname <my-nickname>
#
# davide.gerbaudo@gmail.com, Mar 2013

TAG="n0150"

PROD_DIR="prod_${TAG}"
SUBM_DIR="subm_${TAG}"

echo "Starting                          -- `date`"

mkdir ${PROD_DIR}
cd    ${PROD_DIR}

svn co svn+ssh://svn.cern.ch/reps/atlasoff/PhysicsAnalysis/SUSYPhys/SUSYTools/tags/SUSYTools-00-03-14               SUSYTools
svn co svn+ssh://svn.cern.ch/reps/atlasphys/Physics/SUSY/Analyses/WeakProduction/MultiLep/tags/MultiLep-01-06-04    MultiLep
svn co svn+ssh://svn.cern.ch/reps/atlasinst/Institutes/UCIrvine/SUSYAnalysis/SusyNtuple/tags/SusyNtuple-00-01-06    SusyNtuple
svn co svn+ssh://svn.cern.ch/reps/atlasinst/Institutes/UCIrvine/SUSYAnalysis/SusyCommon/tags/SusyCommon-00-01-04    SusyCommon

sed -i '/asetup/s/setup/slc5\,setup/1' MultiLep/installscripts/setup_area.sh # needed for slc6 nodes

if [ "$ROOTSYS" = "" ]
then
    echo "ROOTSYS not defined, please setup root"
    return
fi

>>>>>>> 76f1f11... bugfix, move root check after localSetupROOT
source MultiLep/installscripts/install_script.sh

echo "Done compiling                    -- `date`"

cd ..
svn co svn+ssh://svn.cern.ch/reps/atlasinst/Institutes/UCIrvine/SUSYAnalysis/SusyCommon/trunk/grid ${SUBM_DIR}
cd    ${SUBM_DIR}

localSetupPandaClient
./create_tarball.sh

echo "Done, ready to submit jobs        -- `date`"

