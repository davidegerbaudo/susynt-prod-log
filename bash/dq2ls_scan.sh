#!/bin/sh

# Loop over the SusyCommon/trunk/grid filelists, query the dataset info with dq2.
#
# davide.gerbaudo@gmail.com
# 2013-11-25

INDIRS="/tmp/tmpaG3qgOSusyCommon_grid/ /tmp/tmpaG3qgOSusyCommon_grid/p1512/"
OUT="/home/gerbaudo/dq2ls_scan.out"

for X in $(find ${INDIRS} -maxdepth 1 -name \*txt )
do
  echo "file : $X -- `date`"
  echo "file : $X" >> ${OUT}   
  for S in $(egrep '(data12_8TeV|mc12_8TeV)' ${X} | awk '{print $1}')
  do
    echo "${S}" >> ${OUT}
    dq2-ls -fH  ${S} | tail -4 >> ${OUT}
  done
done
