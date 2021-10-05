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
if(len(sys.argv)!=5):
    exit(ProgramName.get()+" <rna.txt> <cell-perturbation.txt> <out-null> <out-perturb>\n")
(rnaFile,perturbationFile,nullOut,perturbOut)=sys.argv[1:]

NULL_OUT=open(nullOut,"wt")
PERTURB_OUT=open(perturbOut,"wt")
RNA=open(rnaFile,"rt")
PERTURB=open(perturbationFile,"rt")
for rnaLine in RNA:
    fields=rnaLine.rstrip().split()
    (rnaGene,rnaCell,rnaCount)=[int(x) for x in fields]
    line=PERTURB.readline()
    fields=line.rstrip().split()
    (perturbGene,perturbCell,perturbed)=[int(x) for x in fields]
    if(rnaGene!=perturbGene): raise Exception("genes don't match")
    if(rnaCell!=perturbCell): raise Exception("cells don't match")
    if(perturbed>0):
        print(rnaCount,file=PERTURB_OUT)
    else:
        print(rnaCount,file=NULL_OUT)




