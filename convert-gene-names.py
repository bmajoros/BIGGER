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

def loadIDs(filename):
    d={}
    with open(filename,"rt") as IN:
        for line in IN:
            fields=line.rstrip().split()
            if(len(fields)!=2): raise Exception("Wrong number of fields")
            (name,ID)=fields
            d[name]=ID
    return d

#=========================================================================
# main()
#=========================================================================
if(len(sys.argv)!=3):
    exit(ProgramName.get()+" <gene-ids.txt> <dhs-gene.txt>\n")
(idFile,dhsGeneFile)=sys.argv[1:]

IDs=loadIDs(idFile)
with open(dhsGeneFile,"rt") as IN:
    for line in IN:
        fields=line.rstrip().split()
        if(len(fields)!=2): raise Exception("Wrong number of fields")
        (dhs,gene)=fields
        gene=IDs.get(gene)
        if(gene is None): raise Exception("ID not found")
        print(dhs,gene,1,sep="\t") # The 1 is for MatrixMarket utils

