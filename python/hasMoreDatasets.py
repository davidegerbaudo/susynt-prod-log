#!/bin/env python

# Given two dataset lists, print the datasets that are only in the second list
#
# davide.gerbaudo@gmail.com
# Sept 2014

import datetime
import sys

def main():
    if len(sys.argv) not in [3]:
        prog = sys.argv[0]
        print "usage:\n {0} dslist_old.txt dslist_new.txt".format(prog)
        print 'Called as:\n '+' '.join(sys.argv)
    else:
        input_old = sys.argv[1]
        input_new = sys.argv[2]
        def dset_from_line(l):
            "just strip #, so that if a dset is already there, but commented out, we don't pick it up"
            return l.strip().replace('#','').strip()
        datasets_old = [dset_from_line(l) for l in open(input_old).readlines()]
        lines_to_append = []
        for l in open(input_new).readlines():
            l = l.strip()
            if dset_from_line(l) not in datasets_old:
                lines_to_append.append(l)
        if len(lines_to_append):
            timestamp = datetime.date.today().isoformat()
            print '\n'.join(["# [begin] -- appended on {0}".format(timestamp)]
                            +lines_to_append
                            +["# [end]   -- appended on {0}".format(timestamp)])


if __name__=='__main__':
    main()
