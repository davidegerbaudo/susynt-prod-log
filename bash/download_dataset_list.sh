#!/bin/bash

###############################################
# Script to download datasets provided by an
# input filelist.
#
# The input filelist should contain on each line
# a dataset container that can be accessed byrucio
# in the format
#    <scope>:<logical-dataset-name>
# e.g.,
#    group.phys:group.phys.data15_13TeV.foo.SusyNt.n0216_nt/
#
# Davide.Gerbaudo@cern.ch
# daniel.joseph.antrim@cern.ch
# October 2015
###############################################

readonly PROGNAME=$(basename $0)
readonly PROGDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function help {
    echo "Usage: ${PROGNAME} filelist.txt"
}

function download_filelist {
    local filelist=${1}
    local line
    for line in $( cat ${filelist} | sed '/^\s*$/d' | sed '/^\#/d' )
    do
        ${PROGDIR}/download_dataset.sh ${line}
    done
}

function remove_nt_suffix {
    find . -type d -name "*SusyNt*" -print | while read -rd $'\0' file;
    do
        mv "${file}" "${file/_nt/}"
    done
}

function set_permissions {
    find . -type d -name "*SusyNt*" -print | while read -rd $'\0' file;
    do
        chmod g+rw ${file}
    done
}

function main {
    if [ $# -lt 1 ]; then { help; exit 1; } fi
    download_filelist $*

    # remove the jedi-style _nt suffix from the output containers
    remove_nt_suffix

    # set permissions on datasets in the directory
    set_permissions

}

#________________
main $*
