#!/bin/bash

# This script downloads all the datasets for a given SusyNtuple production tag.
# Setup DQ2 and voms proxy before running this.
#
# davide.gerbaudo@gmail.com
# Feb 2013

readonly PROGNAME=$(basename $0)
# see http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
readonly PROGDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function prepare {
    local tag=${1}
    echo "Preparing directories and lists for ${tag}"
    ${PROGDIR}/update_lists.sh ${tag} data
    ${PROGDIR}/update_lists.sh ${tag} mc
    ${PROGDIR}/update_lists.sh ${tag} susy
}

function download_tag {
    local tag=${1}
    echo "Downloading ${tag}"
    cd data12_${tag}/
    ${PROGDIR}/download_datasetList.sh data12.txt
    cd ../
    cd mc12_${tag}/
    ${PROGDIR}/download_datasetList.sh mc12.txt
    cd ../
    cd susy_${tag}/
    ${PROGDIR}/download_datasetList.sh susy.txt
    cd ../
    echo "done"
}

#___________________________________________________________
function main {
    if [[ ! ("$#" == 1) ]]
    then
        echo "1 argument required (e.g. n0154), $# provided"
        exit 1
    fi
    prepare $*
    download_tag $*
}
#___________________________________________________________
main $*
