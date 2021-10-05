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

class GuideInfo:
    def __init__(self,guideID,enhancerID,guideWorks):
        self.guideID=guideID
        self.enhancerID=enhancerID
        self.guideWorks=guideWorks

def addGuide(guideID,enhancerID,guideWorks,array):
    guides=array.get(enhancerID)
    if(guides is None): guides=array[enhancerID]=set()
    guides.add(GuideInfo(guideID,guideWorks))

def loadGuideInfo(filename):
    info={}
    with open(filename,"rt") as IN:
        for line in IN:
            fields=line.rstrip().split()
            (guideID,enhancerID,guideWorks)=fields
            addGuide(guideID,enhancerID,guideWorks,info)
    return processGuideInfo(info)

def processGuideInfo(guideInfo):
    guidesInEnhancer={}
    guideWorks=set()
    for rec in guideInfo:
        if(rec.guideWorks): guideWorks.add(rec.guideID)
        if(guidesInEnhancer.get(rec.enhancerID) is None):
            guidesInEnhancer[rec.enhancerID]=set()
        guidesInEnhancer[rec.enhancerID].add(rec.guideID)
    return (guidesInEnhancer,guideWorks)

#=========================================================================
# main()
#=========================================================================
if(len(sys.argv)!=7):
    exit(ProgramName.get()+" <guide-info-file> <guide-truth-file> <mean-RNA-count> <rna-dispersion> <effect-size> <out-rna.txt>\n   NOTE: guide-truth-file must be sorted by guide\n")
(guideEnhancerFile,truthFile,meanRNA,phi,beta,outRNA)=sys.argv[1:]
meanRNA=int(meanRNA); phi=float(phi); beta=float(beta)

OUT=open(outRNA,"wt")
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
        if(guideID in guidesInEnhancer):
            perturbedCells.add(cellID)
        else:
            muBeta=mu*beta
            for i in range(numCells):
                cellID=i+1
                mu=muBeta if cellID in perturbedCells else meanRNA
                var=mu+mu*mu/phi
                P=(var-mu)/var
                N=mu*mu/(var-mu)
                count=np.random.negative_binomial(N,P)
                print(gendID,cellID,count,file=OUT)
                thisEnhancer+=1
                geneID+=1
                perturbedCells=set()
            
