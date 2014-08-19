#!/bin/bash

# This script downloads all the datasets from a list.txt
# It just wraps download_dataset.sh
#
# davide.gerbaudo@gmail.com
# Aug 2014

readonly PROGNAME=$(basename $0)
readonly PROGDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function download_filelist {
    local filelist=${1}
    local line
    # drop empty and comment lines
    for line in $( cat ${filelist} | sed '/^\s*$/d' | sed '/^\#/d' )
    do
        ${PROGDIR}/download_dataset.sh ${line}
    done
}

function main {
    if [[ ! ("$#" == 1) ]]
    then
        echo "1 argument required (e.g. user.foo.baz_n0154/), $# provided"
        exit 1
    fi
    download_filelist $*
}

#___________________________________________________________
main $*
