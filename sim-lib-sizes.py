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

#=========================================================================
# main()
#=========================================================================
if(len(sys.argv)!=3):
    exit(ProgramName.get()+" <real-lib-sizes.txt> <num-cells>\n")
(infile,N)=sys.argv[1:]
N=int(N)

with open(infile,"rt") as IN:
    for i in range(N):
        line=IN.readline()
        fields=line.rstrip().split()
        if(len(fields)!=2): next
        (ignore,count)=fields
        print(i+1,count,sep="\t")

        



