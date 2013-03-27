#!/bin/env python

# Simple script to provide a list of job IDs for jobs that should be re-submitted.
# The job IDs are obtained from the e-mail reports, discarding all the ones that succeeded.
# One can then use pbook to re-submit all of the jobs that failed, like this:
#
# pbook
# > for x in (mylist) : retry(x)
#
# Based on the example here:
# http://stackoverflow.com/questions/13210737/get-only-new-emails-imaplib-and-python
#
# davide.gerbaudo@cern.ch
#

import email, getpass, imaplib, os, re

user = raw_input("Enter your GMail username:")
pwd = getpass.getpass("Enter your password: ")
m = imaplib.IMAP4_SSL("imap.gmail.com") # connect
m.login(user,pwd)
m.select("atlas/panda") # I have a filter attaching this label to the job reports
resp, items = m.search(None, "ALL")
items = items[0].split() # getting the mails id

subjTemplate = "PANDA notification for JobsetID : 9118 (All Succeeded)"
failedJoidids = []
for emailid in items:
    resp, hdr_subject = m.fetch(emailid, "(BODY.PEEK[HEADER.FIELDS (SUBJECT)])")
    subject = hdr_subject[0][1].strip()
    jobFailed = 'All Succeeded' not in subject
    print ('*' if jobFailed else ' ')+'  '+subject
    if not jobFailed : continue
    # parse something like "JobsetID : NNNN"
    match = re.search('JobsetID : (?P<jobid>\d+) ', subject)
    if match : failedJoidids.append(int(match.group('jobid')))
    else : print "cannot parse ",subject
print failedJoidids
