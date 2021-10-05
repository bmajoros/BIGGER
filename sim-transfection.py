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
if(len(sys.argv)!=8):
    exit(ProgramName.get()+" <r> <prob-guide-works> <LibSizeFile> <num-guides-per-enhancer> <num-enhancers> <out-guide-truth> <out-guide-info> : "+str(len(sys.argv))+" parms given\n")
(r,probGuideWorks,libSizesFile,guidesPerEnhancer,numEnhancers,guideTruthFile,
 guideEnhancerFile)=sys.argv[1:]
r=float(r); probGuideWorks=float(probGuideWorks)
guidesPerEnhancer=int(guidesPerEnhancer); numEnhancers=int(numEnhancers)

# Prepare output files
GUIDES_ENHANCERS=open(guideEnhancerFile,"wt")
GUIDE_TRUTH=open(guideTruthFile,"wt")

# Load library sizes
L=loadLibSizes(libSizesFile)
N_CELLS=len(L)

# Simulate data
#count=None
guideID=1; enhancerID=1; geneID=1;
for e in range(numEnhancers):
    for g in range(guidesPerEnhancer):
        guideWorks=1 if np.random.uniform(0,1)<probGuideWorks else 0
        print(guideID,enhancerID,guideWorks,file=GUIDES_ENHANCERS)
        for cell in range(N_CELLS):
            cellID=cell+1
            guidePresent=1 if np.random.uniform(0,1)<r else 0
            print(guideID,cellID,guidePresent,file=GUIDE_TRUTH)
        guideID+=1
    enhancerID+=1
GUIDE_TRUTH.close()
GUIDES_ENHANCERS.close()







