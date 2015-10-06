#!/bin/bash

#########################################
# Rucio prints to standard out a progress
# bar which destroys any utility of logging
# the download. Rucio also uses color
# for its text. This script will take in
# a log of a rucio download and remove
# the progress bars and color codes.
#
# daniel.joseph.antrim@cern.ch
# October 2015
#########################################

set -eu

function help {
    echo "Usage: ${PROGNAME} download.log"
}

function remove_progress_bar {
    echo "Removing progress bar"
    local log_=${1}
    sed -i '/%/d' ${1}
}

function remove_color_codes {
    echo "Removing color codes"
    local log_=${1}
    sed -i "s/\x1B\[[0-9;]*[JKmsu]//g" ${1}
}

function main {
    if [ ! $# == 1 ]; then { help; exit 1; } fi

    remove_progress_bar ${1}

    remove_color_codes ${1}

}



#___________________
main $*



