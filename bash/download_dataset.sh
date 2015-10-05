#!/bin/bash

readonly PROGNAME=$(basename $0)
readonly PROGDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function dest_dir_from_datasetname {
    local dataset=${1}
    local jedi_style_suffix="_nt"
    local dest_dir=${dataset/${jedi_style_suffix}/}
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

function dir_is_empty {
    local target=${1}
    if [ -n "$(find ${target} -prune -empty)" ]
    then
        echo "1"
    fi
}

function main {
    if [ $# -lt 1 ]; then { exit 1; } fi

    local dataset=${1}
    shift
    local other_options=""
    while [[ $# > 0 ]]
    do
        other_options="${other_options} $1"
        shift
    done

    local destination_dir=$(dest_dir_from_datasetname ${dataset})
    local rucio_options=""
    rucio_options+=" --ndownloader=5" # need to test this

    mkdir_if_needed ${destination_dir}
    if [ $(dir_is_empty ${destination_dir}) ]
    then
        local cmd="rucio download ${rucio_options} ${dataset}"
        echo ${cmd}
        ${cmd}
    else
        echo "skipping non-empty dir ${desination_dir}"
    fi

    # remove empty directories produced by rucio (these have the <scope>:<dataset-name> structure)--> could this be safer (damn bash)!
    find . -type d -empty -exec rmdir {} \;
}

#__________________
main $*
