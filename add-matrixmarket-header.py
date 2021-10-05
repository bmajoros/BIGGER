#!/usr/bin/env python
#=========================================================================
# Copyright (C)William H. Majoros (bmajoros@alumni.duke.edu)
#=========================================================================
from __future__ import (absolute_import, division, print_function, 
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
# The above imports should allow this program to run in both Python 2 and
# Python 3.  You might need to update your version of module "future".
import sys
import ProgramName
import gzip

#=========================================================================
# main()
#=========================================================================
if(len(sys.argv)!=3):
    exit(ProgramName.get()+" <in.mtx.gz> <out.mtx.gz>\n")
(infile,outfile)=sys.argv[1:]

field1=set(); field2=set(); field3Sum=0
with open(infile,"rt") as IN:
    for line in IN:
        fields=line.rstrip().split()
        if(len(fields)!=3): raise Exception("Wrong number of fields: "+line)
        fields=[int(x) for x in fields]
        field1.insert(fields[0])
        field2.insert(fields[1])
        field3+=fields[2]
IN.close()
#with gzip.open(outfile,"wt") as OUT:
    
