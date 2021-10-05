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
import numpy as np

def loadGuideInfo(filename):
    guidesInEnhancer={}
    guideWorks=set()
    with open(filename,"rt") as IN:
        for line in IN:
            fields=[int(x) for x in line.rstrip().split()]
            (guideID,enhancerID,works)=fields
            if(works>0): guideWorks.add(guideID)
            if(guidesInEnhancer.get(enhancerID) is None):
                guidesInEnhancer[enhancerID]=set()
            guidesInEnhancer[enhancerID].add(guideID)
    return (guidesInEnhancer,guideWorks)

#=========================================================================
# main()
#=========================================================================
if(len(sys.argv)!=8):
    exit(ProgramName.get()+" <guide-info-file> <guide-truth-file> <mean-RNA-count> <rna-dispersion> <effect-size> <out-rna.txt> <cell-perturbation.txt>\n   NOTE: guide-truth-file must be sorted by guide\n")
(guideEnhancerFile,truthFile,meanRNA,phi,beta,outRNA,perturbationFile)=\
    sys.argv[1:]
meanRNA=int(meanRNA); phi=float(phi); beta=float(beta)

PERTURBATION=open(perturbationFile,"wt")
RNA=open(outRNA,"wt")
(guidesInEnhancer,guideWorks)=loadGuideInfo(guideEnhancerFile)
with gzip.open(truthFile,"rt") as IN:
    IN.readline(); IN.readline(); # skip 2 header lines
    thisEnhancer=1
    geneID=1
    perturbedCells=set()
    numCells=0
    for line in IN:
        fields=[int(x) for x in line.rstrip().split()]
        (guideID,cellID,present)=fields
        if(cellID>numCells): numCells=cellID
        if(guideID not in guideWorks): next
        #print("guideID=",guideID,"enhancerID=",thisEnhancer,
        #      "guidesInEnhancer=",guidesInEnhancer[thisEnhancer])
        if(guideID in guidesInEnhancer[thisEnhancer]):
            perturbedCells.add(cellID)
        else:
            muBeta=meanRNA*beta
            for i in range(numCells):
                cellID=i+1
                mu=muBeta if cellID in perturbedCells else meanRNA
                var=mu+mu*mu/phi
                P=(var-mu)/var
                N=mu*mu/(var-mu)
                count=np.random.negative_binomial(N,P)
                #print("beta=",beta,"mu=",muBeta,"meanRNA=",meanRNA,"var=",
                #      var,"phi=",phi,"P=",P,"N=",N,"count=",count)
                print(geneID,cellID,count,file=RNA)
                status=1 if cellID in perturbedCells else 0
                print(geneID,cellID,status,file=PERTURBATION)
            thisEnhancer+=1
            geneID+=1
            perturbedCells=set()
                
            ### need to push back the previous guide or it will get lost!

                
