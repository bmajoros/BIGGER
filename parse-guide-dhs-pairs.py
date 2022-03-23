#!/usr/bin/env python
#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2021 William H. Majoros <bmajoros@alumni.duke.edu>
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
if(len(sys.argv)!=2):
    exit(ProgramName.get()+" <guide_DHS_pairs.csv>\n")
(infile,)=sys.argv[1:]

with open(infile,"rt") as IN:
    IN.readline() # discard header
    for line in IN:
        fields=line.rstrip().split(",")
        (guide,dhs)=fields[0:2]
        if(dhs=="0"): continue # non-targeting guide
        print(guide,dhs,1,sep="\t") # the 1 allows us to use MatrixMarket utils
        



