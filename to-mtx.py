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
from Rex import Rex
rex=Rex()

#=========================================================================
# main()
#=========================================================================
if(len(sys.argv)!=3):
    exit(ProgramName.get()+" <in.mtx> <out.mtx.gz>\n")
(infile,outfile)=sys.argv[1:]

field1=set(); field2=set(); field3Sum=0
with open(infile,"rt") as IN:
    for line in IN:
        fields=line.rstrip().split()
        if(len(fields)!=3): raise Exception("Wrong number of fields: "+line)
        #fields=[int(x) for x in fields]
        field1.add(int(fields[0]))
        field2.add(int(fields[1]))
        if(rex.find("\.",fields[2])):
            field3Sum+=float(fields[2])
        else: field3Sum+=int(fields[2])
IN.close()

field1=len(field1); field2=len(field2); field3=int(field3Sum)
with gzip.open(outfile,"wt") as OUT:
    print("%%MatrixMarket matrix coordinate integer general",file=OUT)
    print(field1,field2,field3,file=OUT)
    with open(infile,"rt") as IN:
        for line in IN:
            fields=line.rstrip().split()
            print(fields[0],fields[1],fields[2],file=OUT)

    
