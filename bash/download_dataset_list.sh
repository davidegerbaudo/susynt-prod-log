#!/bin/bash


readonly PROGNAME=$(basename $0)
readonly PROGDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function download_filelist {
    local filelist=${1}
    local line
    for line in $( cat ${filelist} | sed '/^\s*$/d' | sed '/^\#/d' )
    do
        ${PROGDIR}/download_dataset.sh ${line}
    done
}

function main {
    if [[ ! ("$#" == 1) ]]
    then
        echo "1 argument required (e.g. user.foo.baz_n0216/), $# provided"
      #  exit 1
    fi
    download_filelist $*

    # remove the "_nt" suffix
    for dsdir in *; do mv "${dsdir}" "${dsdir/_nt/}"; done

    # set permissions on dataset directory
    for dsdir in *; do chmod g+rw ${dsdir}; done

}

#________________
main $*
