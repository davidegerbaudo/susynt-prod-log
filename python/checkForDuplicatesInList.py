#!/bin/env python

# Given a dataset lists, check for duplicate dsids, and comment them out
#
# davide.gerbaudo@gmail.com
# Aug 2013

import collections
import sys
from sampleUtils import parseSusyntSampleName

def main():
    if len(sys.argv) not in [2, 3]:
        prog = sys.argv[0]
        print "usage:\n {0} filelist.txt [--overwrite]".format(prog)
    else:
        input_file = sys.argv[1]
        overwrite = sys.argv.count('--overwrite')
        counters = collections.defaultdict(int)
        lines = open(input_file).read().split('\n')
        def is_valid_line(l):
            return len(l.strip()) and not l.strip().startswith('#')
        for l in lines:
            if is_valid_line(l):
                match = parseSusyntSampleName(l)
                if match : counters[match['sample']] += 1
        duplicated_samples = [s for s, c in counters.iteritems() if c>1]        
        output = sys.stdout if not overwrite else open(input_file, 'w')
        for l in lines:
            prefix = '# ' if is_valid_line(l) and any(s in l for s in duplicated_samples) else ''
            print >> output, "{0}{1}".format(prefix, l)
        if overwrite:
            output.close()
        if len(duplicated_samples):
            print "found {0} duplicates in {1}, please check".format(len(duplicated_samples), input_file)

#___________________________________________________________
if __name__=='__main__':
    main()

