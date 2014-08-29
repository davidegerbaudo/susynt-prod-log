#!/bin/bash

# This script updates the data/mc/signal samples lists for a given tag.
# Setup DQ2 and voms proxy before running it.
#
# davide.gerbaudo@gmail.com
# Feb 2013

readonly PROGNAME=$(basename $0)
# see http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
readonly PROGDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function checkTag {
    if [ $# -lt 1 ]
    then
        echo "pass the current tag as argument, e.g. 'n0048'"
        exit 1
    fi
    local tag=$1
}

# \todo this check should be more accurate (i.e. not just counting lines) DG-2014-08-18
function mvIfHasMoreLines {
    local newfile=$1
    local oldfile=$2
    local numnewlines=$(echo $(wc -l < ${newfile}))
    local numoldlines=$(echo $(wc -l < ${oldfile}))
    local extralines=$(( ${numnewlines} - ${numoldlines} ))
    if [[ ${extralines} -gt 0 ]]
	then
	    mv ${oldfile} ${oldfile}.old
	    mv ${newfile} ${oldfile}
    else
	echo "No new lines"
    fi
}

function createDummyFileIfMissing {
    local files=$*
    for X in ${files}
    do
      if [ ! -f ${X} ]
	  then
	      echo "Missing file ${X}; creating empty placeholder"
          touch ${X}
      fi
    done
}

function exitOnMissingFile {
    local files=$*
    for X in ${files}
    do
      if [ ! -f ${X} ]
	  then
	      echo "Missing file ${X}"
	  exit 1
      fi
    done
}

function check_for_duplicates {
    local filelist=${1}
    ${PROGDIR}/../python/checkForDuplicatesInList.py ${filelist} --overwrite
}

function chmodDestDir {
    local dest_dir=${1}
    chmod -f -R a+rw dest_dir
}

function update_list {
    local tag=$1
    local mode=$2
    local oldfile=""
    local dest_dir=""
    local newfile="/tmp/dq2-ls-tmp.txt"
    local signal_pattern="simplifiedModel|DGnoSL|DGemtR|DGstauR|RPV|pMSSM|_DGN|MSUGRA|GGM|sM_wA|Herwigpp_UEEE3_CTEQ6L1_C1C1|Herwigpp_UEEE3_CTEQ6L1_C1N2"
    local suffix="${tag}/" # panda style output container
    suffix+="|${tag}.*root/" # new jedi output container

    case "${mode}" in
	data)
	    dest_dir="data12_${tag}"
	    oldfile="${dest_dir}/data12.txt"
	    mkdir -p ${dest_dir}
	    createDummyFileIfMissing ${oldfile}
	    dq2-ls "group.phys-susy.*data12*physics*.SusyNt.*${tag}_nt/" | sort | egrep "${suffix}" > ${newfile}
	    exitOnMissingFile ${newfile}
	    mvIfHasMoreLines ${newfile} ${oldfile}
	    check_for_duplicates ${oldfile}
	    chmodDestDir ${dest_dir}
	    ;;
	mc)
	    dest_dir="mc12_${tag}"
	    oldfile="${dest_dir}/mc12.txt"
	    mkdir -p ${dest_dir}
	    createDummyFileIfMissing ${oldfile}
	    dq2-ls "group.phys-susy.mc12_8TeV.*.SusyNt.*${tag}_nt/" | egrep -v "${signal_pattern}" | sort | egrep "${suffix}" > ${newfile}
	    exitOnMissingFile ${newfile}
	    mvIfHasMoreLines ${newfile} ${oldfile}
	    check_for_duplicates ${oldfile}
	    chmodDestDir ${dest_dir}
	    ;;
	susy)
	    dest_dir="susy_${tag}"
	    oldfile="${dest_dir}/susy.txt"
	    mkdir -p ${dest_dir}
	    createDummyFileIfMissing ${oldfile}
	    dq2-ls "group.phys-susy.mc12_8TeV.*.SusyNt.*${tag}_nt/" | egrep "${signal_pattern}" | sort | egrep "${suffix}" > ${newfile}
	    exitOnMissingFile ${newfile}
	    mvIfHasMoreLines ${newfile} ${oldfile}
	    check_for_duplicates ${oldfile}
	    chmodDestDir ${dest_dir}
	    ;;
	*)
	    echo "Invalid mode ${mode}. Usage update_lists.sh TAG MODE, where MODE in (data, mc, susy)."
	    ;;
    esac
}

#___________________________________________________________
checkTag $*
update_list $*
