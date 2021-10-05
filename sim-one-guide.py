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
if(len(sys.argv)!=9):
    exit(ProgramName.get()+" <r> <lambda> <mu> <phi> <LibSizeFile> <out-counts> <out-noise> <out-signal>\n")
(r,Lambda,mu,phi,libSizesFile,countsFile,noiseFile,signalFile)=sys.argv[1:]
r=float(r); Lambda=float(Lambda); mu=float(mu); phi=float(phi)

var=mu+mu*mu/phi # from the STAN page
P=(var-mu)/var # probability of success in NB
N=mu*mu/(var-mu) # number of trials in NB

COUNTS=open(countsFile,"wt")
print("%%MatrixMarket matrix coordinate integer general\n3201 56882 13305244",
      file=COUNTS) ### NEED TO CHANGE THIS
NOISE=open(noiseFile,"wt"); SIGNAL=open(signalFile,"wt")
L=loadLibSizes(libSizesFile)
c=None
for i in range(len(L)):
    p=np.random.uniform(0,1)
    if(p<r):
        c=np.random.negative_binomial(N,P) ### NEED TO VERIFY THIS
        print(i+1,file=SIGNAL)
    else:
        c=np.random.poisson(Lambda*L[i])
        print(i+1,file=NOISE)
    print(1,i+1,c,sep="\t",file=COUNTS)

#====================================================================
# sim-lib-sizes.py ../tyler/library-sizes.txt 5000 > lib-sizes1.txt
# sim-mixture.py 0.1 1 10 1 lib-sizes1.txt counts.txt noise.txt signal.txt





