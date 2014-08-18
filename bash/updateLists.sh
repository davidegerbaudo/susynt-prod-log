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
    TAG=$1
}

function mvIfHasMoreLines {
    NEWFILE=$1
    OLDFILE=$2
    NUMNEWLINES=$(echo $(wc -l < ${NEWFILE}))
    NUMOLDLINES=$(echo $(wc -l < ${OLDFILE}))
    EXTRALINES=$(( ${NUMNEWLINES} - ${NUMOLDLINES} ))
    echo "old : ${OLDFILE} ${NUMOLDLINES}, ${NEWFILE} ${NUMNEWLINES}"
    if [[ ${EXTRALINES} -gt 0 ]]
	then
	    mv ${OLDFILE} ${OLDFILE}.old
	    mv ${NEWFILE} ${OLDFILE}
    else
	echo "No new lines"
    fi
}

function createDummyFileIfMissing {
    FILES=$*
    for X in ${FILES}
    do
      if [ ! -f ${X} ]
	  then
	      echo "Missing file ${X}; creating empty placeholder"
          touch ${X}
      fi
    done
}

function exitOnMissingFile {
    FILES=$*
    for X in ${FILES}
    do
      if [ ! -f ${X} ]
	  then
	      echo "Missing file ${X}"
	  exit 1
      fi
    done
}

function updateList {
    TAG=$1
    MODE=$2
    NEWFILE="/tmp/dq2-ls-tmp.txt"
    SIGNAL_PATTERN="simplifiedModel|DGnoSL|DGemtR|DGstauR|RPV|pMSSM|_DGN|MSUGRA|GGM|sM_wA|Herwigpp_UEEE3_CTEQ6L1_C1C1|Herwigpp_UEEE3_CTEQ6L1_C1N2"
    NICKNAME=$USER
    case "${MODE}" in
	data)
	    OLDFILE="data12_${TAG}/data12.txt"
	    createDummyFileIfMissing ${OLDFILE}
	    dq2-ls "user.${NICKNAME}.group.phys-susy.data12*physics*.SusyNt.*${TAG}/" | sort > ${NEWFILE}
	    exitOnMissingFile ${NEWFILE}
	    mvIfHasMoreLines ${NEWFILE} ${OLDFILE}
	    ;;
	mc)
	    OLDFILE="mc12_${TAG}/mc12.txt"
	    createDummyFileIfMissing ${OLDFILE}
	    dq2-ls "user.${NICKNAME}.mc12_8TeV.*.SusyNt.*${TAG}/" | egrep -v "${SIGNAL_PATTERN}" | sort > ${NEWFILE}
	    exitOnMissingFile ${NEWFILE}
	    mvIfHasMoreLines ${NEWFILE} ${OLDFILE}
	    ;;
	susy)
	    OLDFILE="susy_${TAG}/susy.txt"
	    createDummyFileIfMissing ${OLDFILE}
        dq2-ls "user.${NICKNAME}.mc12_8TeV.*.SusyNt.*${TAG}/" | egrep "${SIGNAL_PATTERN}" | sort > ${NEWFILE}
	    exitOnMissingFile ${NEWFILE}
	    mvIfHasMoreLines ${NEWFILE} ${OLDFILE}
	    ;;
	*)
	    echo "Invalid mode ${MODE}. Usage updateLists.sh TAG MODE, where MODE in (data, mc, susy)."
	    ;;
    esac
}

# main script
checkTag $*
updateList $*
