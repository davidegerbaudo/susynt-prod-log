#!/bin/bash

# This script updates the data/mc/signal samples lists for a given tag.
# Setup DQ2 and voms proxy before running this.
# There is some duplication with prepareTag.sh (discuss this with Steve and fix it).
#
# davide.gerbaudo@gmail.com
# Feb 2013

function checkTag {
    if [ $# -lt 1 ]
    then
        echo "pass the current tag as argument, e.g. 'n0048'"
        exit 1
    fi
    local tag=$1
}

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

function chmodDestDir {
    local dest_dir=${1}
    chmod -f -R a+rw dest_dir
}

function updateList {
    local tag=$1
    local mode=$2
    local oldfile=""
    local dest_dir=""
    local newfile="/tmp/dq2-ls-tmp.txt"
    local signal_pattern="simplifiedModel|DGnoSL|DGemtR|DGstauR|RPV|pMSSM|_DGN|MSUGRA|GGM|sM_wA|Herwigpp_UEEE3_CTEQ6L1_C1C1|Herwigpp_UEEE3_CTEQ6L1_C1N2"
    local nickname=$USER
    local suffix="${tag}/" # panda style output container
    suffix+="|${tag}.*root/" # new jedi output container

    case "${mode}" in
	data)
	    dest_dir="data12_${tag}"
	    oldfile="${dest_dir}/data12.txt"
	    mkdir -p ${dest_dir}
	    createDummyFileIfMissing ${oldfile}
	    dq2-ls "user.${nickname}.group.phys-susy.data12*physics*.SusyNt.*${tag}*/" | sort | egrep "${suffix}" > ${newfile}
	    exitOnMissingFile ${newfile}
	    mvIfHasMoreLines ${newfile} ${oldfile}
	    chmodDestDir ${dest_dir}
	    ;;
	mc)
	    dest_dir="mc12_${tag}"
	    oldfile="${dest_dir}/mc12.txt"
	    mkdir -p ${dest_dir}
	    createDummyFileIfMissing ${oldfile}
	    dq2-ls "user.${nickname}.mc12_8TeV.*.SusyNt.*${tag}*/" | egrep -v "${signal_pattern}" | sort | egrep "${suffix}" > ${newfile}
	    exitOnMissingFile ${newfile}
	    mvIfHasMoreLines ${newfile} ${oldfile}
	    chmodDestDir ${dest_dir}
	    ;;
	susy)
	    dest_dir="susy_${tag}"
	    oldfile="${dest_dir}/susy.txt"
	    mkdir -p ${dest_dir}
	    createDummyFileIfMissing ${oldfile}
	    dq2-ls "user.${nickname}.mc12_8TeV.*.SusyNt.*${tag}*/" | egrep "${signal_pattern}" | sort | egrep "${suffix}" > ${newfile}
	    exitOnMissingFile ${newfile}
	    mvIfHasMoreLines ${newfile} ${oldfile}
	    chmodDestDir ${dest_dir}
	    ;;
	*)
	    echo "Invalid mode ${mode}. Usage updateLists.sh TAG MODE, where MODE in (data, mc, susy)."
	    ;;
    esac
}

# main script
checkTag $*
updateList $*
