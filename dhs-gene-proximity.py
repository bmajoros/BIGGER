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
from GffTranscriptReader import GffTranscriptReader
from Gene import Gene
from BedReader import BedReader
from Bed6Record import Bed6Record

def processChrom(chrom,geneHash,dhsHash,maxDist):
    genes=geneHash.get(chrom)
    if(genes is None): return
    dhss=dhsHash.get(chrom)
    if(dhss is None): return
    genes.sort(key=lambda x: x.getBegin())
    dhss.sort(key=lambda x: x.getBegin())
    proximity(genes,dhss,maxDist)

def distance(gene,dhs):
    geneMid=(gene.getBegin()+gene.getEnd())/2
    dhsMid=(dhs.getBegin()+dhs.getEnd())/2
    gene.mid=geneMid; dhs.mid=dhsMid
    d=geneMid-dhsMid
    if(d<0): d=-d
    return d
    
def proximity(genes,dhss,maxDist):
    i=0; j=0
    N_GENES=len(genes); N_DHS=len(dhss)
    while(i<N_GENES and j<N_DHS):
        gene=genes[i]; dhs=dhss[j]
        d=distance(gene,dhs)
        if(d<=maxDist):
            print(dhs.name,gene.getID(),sep="\t")
        if(gene.mid<dhs.mid): i+=1
        else: j+=1
        
#=========================================================================
# main()
#=========================================================================
if(len(sys.argv)!=4):
    exit(ProgramName.get()+" <dhs.bed> <genes.gff> <max-distance>\n")
(dhsFile,genesFile,maxDist)=sys.argv[1:]
maxDist=int(maxDist)

gffReader=GffTranscriptReader()
geneHash=gffReader.hashGenesBySubstrate(genesFile)
dhsHash=BedReader.hashBySubstrate(dhsFile)

keys=geneHash.keys()
for chrom in keys:
    processChrom(chrom,geneHash,dhsHash,maxDist)
    


