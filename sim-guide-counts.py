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
import gzip

def loadLibSizes(filename):
    L=[]
    with open(filename,"rt") as IN:
        for line in IN:
            fields=line.rstrip().split()
            if(len(fields)!=2): raise Exception("Wrong number of fields in "+
                                                filename)
            L.append(int(fields[1]))
    mean=float(sum(L))/float(len(L))
    for i in range(len(L)): L[i]/=mean
    return L

#=========================================================================
# main()
#=========================================================================
if(len(sys.argv)!=7):
    exit(ProgramName.get()+" <guide-truth.mtx.gz> <lambda> <mu> <phi> <LibSizeFile> <out-counts>\n")
(truthFile,Lambda,unscaledMu,phi,libSizesFile,countsFile)=sys.argv[1:]
Lambda=float(Lambda); unscaledMu=float(unscaledMu); phi=float(phi)

# Open files:
COUNTS=open(countsFile,"wt")
L=loadLibSizes(libSizesFile)

# Simulate data:
with gzip.open(truthFile,"rt") as IN:
    IN.readline(); IN.readline(); # skip 2 header lines
    count=None
    for line in IN:
        fields=line.rstrip().split()
        (guideID,cellID,present)=[int(x) for x in fields]
        libSize=L[cellID-1]
        if(present>0):
            mu=unscaledMu*libSize
            var=mu+mu*mu/phi # from the STAN page
            P=(var-mu)/var   # probability of success in NB
            N=mu*mu/(var-mu) # number of trials in NB
            count=np.random.negative_binomial(N,P)
        else:
            count=np.random.poisson(Lambda*libSize)
        print(guideID,cellID,count,sep="\t",file=COUNTS)






