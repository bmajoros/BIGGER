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
import numpy as np

def loadLibSizes(filename):
    L=[]
    with open(filename,"rt") as IN:
        for line in IN:
            fields=line.rstrip().split()
            if(len(fields)!=2): raise Exception("Wrong number of fields in "+
                                                filename)
            L.append(int(fields[1]))
    #mean=float(sum(L))/float(len(L))
    #for i in range(len(L)): L[i]/=mean
    return L
            
#=========================================================================
# main()
#=========================================================================
if(len(sys.argv)!=11):
    exit(ProgramName.get()+" <r> <lambda> <mu> <phi> <LibSizeFile> <num-guides-per-enhancer> <num-enhancers> <out-guide-truth> <out-guides-enhancers> <out-rna> : "+str(len(sys.argv))+" parms given\n")
(r,Lambda,mu,phi,libSizesFile,guidesPerEnhancer,numEnhancers,
 guideTruthFile,guideEnhancerFile,rnaFile)=sys.argv[1:]
r=float(r); Lambda=float(Lambda); mu=float(mu); phi=float(phi)
guidesPerEnhancer=int(guidesPerEnhancer); numEnhancers=int(numEnhancers)

# Compute NB distribution parameters
var=mu+mu*mu/phi # from the STAN page
P=(var-mu)/var # probability of success in NB
N=mu*mu/(var-mu) # number of trials in NB

# Prepare output files
RNA=open(rnaFile,"wt")
GUIDES_ENHANCERS=open(guideEnhancerFile,"wt")
GUIDE_TRUTH=open(guideTruthFile,"wt")
#print("%%MatrixMarket matrix coordinate integer general\n0 0 0",
#      file=GUIDE_TRUTH) ### NEED TO CHANGE THIS

# Load library sizes
L=loadLibSizes(libSizesFile)
N_CELLS=len(L)

# Simulate data
#count=None
guideID=1; enhancerID=1; geneID=1;
for e in range(numEnhancers):
    for g in range(guidesPerEnhancer):
        print(guideID,enhancerID,sep="\t",file=GUIDES_ENHANCERS)
        for cell in range(N_CELLS):
            cellID=cell+1
            p=np.random.uniform(0,1)
            guidePresent=1 if p<r else 0
            print(guideID,cellID,guidePresent,sep="\t",file=GUIDE_TRUTH)
        guideID+=1
    enhancerID+=1
GUIDE_TRUTH.close()
GUIDES_ENHANCERS.close()







