#!/bin/bash

# Script to download a dataset

# This script is just a wrapper around dq2-get to download all the
# root files and put them in a directory with name=dataset_name.

# Based on Steve's (sfarrell@cern.ch) NtDownload.sh
# davide.gerbaudo@gmail.com
# Aug 2014

readonly PROGNAME=$(basename $0)
readonly PROGDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function help {
    echo "Usage: ${PROGNAME} dataset [other-dq2-options]"
}

# Determine from the dataset name the name of the destination directory
function dest_dir_from_datasetname {
    local dataset=${1}
    local jedi_style_suffix="_nt" # dropping the suffix introduced by jedi will make things bk-compatible
    local dest_dir=${dataset/${jedi_style_suffix}/}
    if [[ ${dest_dir} == *":"* ]] # new (rucio?) dset names are user.blah:user.bla.mc13<...>_nt/
        then
        dest_dir=$(echo ${dest_dir} | cut -d ':' -f 2)
    fi
    echo "${dest_dir}"
}

function mkdir_if_needed {
    local dest_dir=${1}
    if [ ! -d ./${dest_dir} ]; then
        echo "Creating output directory"
        mkdir ${dest_dir}
        chmod g+rw ${dest_dir}
    fi
}

function dir_is_emtpy {
    local target=${1}
    if [ -n "$(find ${target} -prune -empty)" ]
    then
        echo "1"
    fi
}

function main {
    if [ $# -lt 1 ]; then { help; exit 1; } fi
    local dataset=${1}
    shift
    local other_options=""
    while [[ $# > 0 ]]
    do
        other_options="${other_options} $1"
        shift
    done
    local destination_dir=$(dest_dir_from_datasetname ${dataset})
    local dq2_default_options=""
    dq2_default_options+=" --threads=3,5" # concurrent datasets,files
    dq2_default_options+=" --no-directories"
    dq2_default_options+=" --files=*.root*"
    dq2_default_options+=" --to-here=./"
    
    mkdir_if_needed ${destination_dir}
    if [ $(dir_is_emtpy ${destination_dir}) ]
    then
        pushd ${destination_dir}
        local cmd="dq2-get ${dq2_default_options} ${other_options} ${dataset}"
        echo ${cmd}
        ${cmd}
        popd
    else
        echo "skipping non-emtpy dir ${destination_dir}"
    fi
}
#___________________________________________________________

main $*
