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
from MatrixMarket import MatrixMarket

# NOTE: the guide-dhs and dhs-gene files must both be sorted by dhs

#=========================================================================
# main()
#=========================================================================
if(len(sys.argv)!=3):
    exit(ProgramName.get()+" <guide-dhs.sorted.mtx.gz> <dhs-gene.sorted.mtx.gz>\n")
(guideDhsFile,dhsGeneFile)=sys.argv[1:]

guideDhsMM=MatrixMarket(guideDhsFile)
dhsGeneMM=MatrixMarket(dhsGeneFile)
guideDhs=guideDhsMM.nextGroup(1)
dhsGene=dhsGeneMM.nextGroup(0)
while(guideDhs is not None and dhsGene is not None):
    if(len(guideDhs)==0 or len(dhsGene)==0): break
    dhs1=guideDhs[0][1]; dhs2=dhsGene[0][0]
    while(dhs1 is not None and dhs1<dhs2):
        guideDhs=guideDhsMM.nextGroup(1)
        dhs1=guideDhs[0][1]
    while(dhs2 is not None and dhs2<dhs1):
        dhsGene=dhsGeneMM.nextGroup(0)
        dhs2=dhsGene[0][0]
    if(dhs1==dhs2):
        for rec1 in guideDhs:
            for rec2 in dhsGene:
                print(rec1[0],rec2[1],1,sep="\t")
        guideDhs=guideDhsMM.nextGroup(1)
        dhsGene=dhsGeneMM.nextGroup(0)
                
