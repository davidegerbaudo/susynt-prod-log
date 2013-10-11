# Braindump

For the slepton we read the information from the root file provided by
Cristophe.  Of course this is not written in stone (i.e. we can dump
the root file to txt).  This is done in SleptonXsecReader, which in
turn also needs the information from SusyNtuple to map
dsid<-->SleptonPoint (see [1]).

SusyXSReader, reads the txt files from SusyXSReader/data, see [2].
The format of the txt files is not strictly defined or enforced; we
had to adapt the code a couple of times already.

[1] see SleptonXsecReader::getDefaultDsidFilename(), for example here
https://svnweb.cern.ch/trac/atlasinst/browser/Institutes/UCIrvine/SUSYAnalysis/SusyNtuple/trunk/util/test_xsRead.cxx?rev=#L35

[2]
https://svnweb.cern.ch/trac/atlasinst/browser/Institutes/UCIrvine/mrelich/SusyXSReader/trunk/Root/XSReader.cxx