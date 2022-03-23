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

GENE_INDEX=0 # gene column in mtx file
CELL_INDEX=1
COUNTS_INDEX=2

#=========================================================================
# main()
#=========================================================================
if(len(sys.argv)!=4):
    exit(ProgramName.get()+" <rna.sorted.mtx.gz> <min-#cells> <min-ave-read-counts>\n")
(infile,minCells,minReads)=sys.argv[1:]
minCells=int(minCells)
minReads=int(minReads)

mtx=MatrixMarket(infile)
while(True):
    recs=mtx.nextGroup(GENE_INDEX)
    if(recs is None): break
    numCellsExpress=len(recs)
    if(numCellsExpress<minCells): continue
    #print(numCellsExpress)
    #if(numCellsExpress<150000): continue
    array=[int(rec[COUNTS_INDEX]) for rec in recs]
    #for rec in recs:
    #    array.append(int(rec[COUNTS_INDEX]))
    ave=float(sum(array))/float(len(array))
    #print(ave)
    if(ave<minReads): continue
    print(recs[0][0])



