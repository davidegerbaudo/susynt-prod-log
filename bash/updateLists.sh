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

function updateList {
    local tag=$1
    local mode=$2
    local oldfile=""
    local newfile="/tmp/dq2-ls-tmp.txt"
    local signal_pattern="simplifiedModel|DGnoSL|DGemtR|DGstauR|RPV|pMSSM|_DGN|MSUGRA|GGM|sM_wA|Herwigpp_UEEE3_CTEQ6L1_C1C1|Herwigpp_UEEE3_CTEQ6L1_C1N2"
    local nickname=$USER
    local suffix="${tag}/" # panda style output container
    suffix+="|${tag}.*root/" # new jedi output container

    case "${mode}" in
	data)
	    oldfile="data12_${tag}/data12.txt"
	    createDummyFileIfMissing ${oldfile}
	    dq2-ls "user.${nickname}.group.phys-susy.data12*physics*.SusyNt.*${tag}*/" | sort | egrep "${suffix}" > ${newfile}
	    exitOnMissingFile ${newfile}
	    mvIfHasMoreLines ${newfile} ${oldfile}
	    ;;
	mc)
	    oldfile="mc12_${tag}/mc12.txt"
	    createDummyFileIfMissing ${oldfile}
	    dq2-ls "user.${nickname}.mc12_8TeV.*.SusyNt.*${tag}*/" | egrep -v "${signal_pattern}" | sort | egrep "${suffix}" > ${newfile}
	    exitOnMissingFile ${newfile}
	    mvIfHasMoreLines ${newfile} ${oldfile}
	    ;;
	susy)
	    oldfile="susy_${tag}/susy.txt"
	    createDummyFileIfMissing ${oldfile}
        dq2-ls "user.${nickname}.mc12_8TeV.*.SusyNt.*${tag}*/" | egrep "${signal_pattern}" | sort | egrep "${suffix}" > ${newfile}
	    exitOnMissingFile ${newfile}
	    mvIfHasMoreLines ${newfile} ${oldfile}
	    ;;
	*)
	    echo "Invalid mode ${mode}. Usage updateLists.sh TAG MODE, where MODE in (data, mc, susy)."
	    ;;
    esac
}

# main script
checkTag $*
updateList $*
