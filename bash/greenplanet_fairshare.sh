#!/bin/env sh

# A script to summarize the atlas fairshare on the greenplanet queue.
#
# davide.gerbaudo@gmail.com
# Oct 2013

ATLAS_USERS=$(grep ^atlas /etc/group | cut -d ':' -f 4)
ATLAS_USERS=$(echo ${ATLAS_USERS} | sed 's/,/|/g') # regexp or
ATLAS_USERS="atlas|${ATLAS_USERS}"
HEADERS="FSInterval|FSWeight|TotalUsage"
diagnose -f | egrep "(${HEADERS}|${ATLAS_USERS})"
