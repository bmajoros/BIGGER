#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function, 
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
# The above imports should allow this program to run in both Python 2 and
# Python 3.  You might need to update your version of module "future".
import sys
import os
import math
import ProgramName
from Rex import Rex
rex=Rex()
import TempFilename
from StanParser import StanParser
from Stan import Stan
from DataFrame import DataFrame
from SummaryStats import SummaryStats
import getopt
import random

DEBUG=False
STDERR=TempFilename.generate(".stderr")
INPUT_FILE=TempFilename.generate(".staninputs")
INIT_FILE=TempFilename.generate(".staninit")
OUTPUT_TEMP=TempFilename.generate(".stanoutputs")

#def writeInitializationFile(filename):
#    OUT=open(filename,"wt")
#    r=random.uniform(0.01,0.99)
#    mu=random.gauss(0,1)
#    sigma=math.exp(random.gauss(0,2))
#    print("r <-",r,file=OUT)
#    print("mu <-",mu,file=OUT)
#    print("sigma <-",sigma,file=OUT)
#    OUT.close()

def writeInputsFile(stan,X,filename,L):
    OUT=open(filename,"wt")
    print("N <-",str(len(X)),file=OUT)
    stan.writeOneDimArray("X",X,len(X),OUT)
    stan.writeOneDimArray("L",L,len(L),OUT)
    OUT.close()

def runSTAN(model,X,numWarmup,numSamples,infile,outfile,L):
    # Create STAN object
    stan=Stan(model)

    # Write input and initialization files
    writeInputsFile(stan,X,INPUT_FILE,L)
    global INIT_FILE
    #writeInitializationFile(INIT_FILE)

    # Run STAN model
    if(DEBUG):
        print(stan.getCmd(numWarmup,numSamples,INPUT_FILE,OUTPUT_TEMP,STDERR,INIT_FILE))
    stan.run(numWarmup,numSamples,INPUT_FILE,OUTPUT_TEMP,STDERR,INIT_FILE)

    # Parse MCMC output
    parser=StanParser(OUTPUT_TEMP)
    r=parser.getVariable("r")
    LAMBDA = parser.getVariable("lambda")
    nbMean=parser.getVariable("nbMean")
    nbDisp = parser.getVariable("nbDisp")
    (med_LAMBDA,a,b) = parser.getMedianAndCI(0.95,"lambda")
    (med_nbMean,a,b)=parser.getMedianAndCI(0.95,"nbMean")
    (assignments) =getAssignments(parser)
    return (r,nbMean, nbDisp, LAMBDA, med_LAMBDA, med_nbMean, assignments)

#pass lambda and nbmean to compare, lambda should be smaller than nbmean 
def getAssignments(parser):
    assignments=[]
    likeli_poisson=[]
    likeli_negbin=[]
    poisson_sum=[]
    negbin_sum=[]
    names=parser.getVarNames()
    for name in names:
        if(len(name)>=4 and name[:4]=="PZi."):
            samples=parser.getVariable(name)
            median=SummaryStats.median(samples)
            assignments.append(median)
    return (assignments)

def writeAssignments(cellIDs,assignments,assignFile, LAMBDA, mu):
    with open(assignFile,"wt") as ASSIGN:
        N=len(assignments)
        z = 0
        if float(LAMBDA) >= float(mu):
            z = 1
        for i in range(N):
            cellID=cellIDs[i]
            x=assignments[i]
            print(cellID,x, sep="\t",file=ASSIGN)

def writeSamples(r,mu,disp,LAMBDA, outfile):
    N=len(r)
    with open(outfile,"wt") as SAMPLES:
        print("r\tsmu\tsDisp\tslambda",file=SAMPLES)
        for i in range(N):
            print(r[i],mu[i], disp[i], LAMBDA[i], sep="\t",file=SAMPLES)

#=========================================================================
# main()
#=========================================================================
(options,args)=getopt.getopt(sys.argv[1:],"s:")
if(len(args)!=7):
    exit(ProgramName.get()+" [-s stanfile] <model> <guide-counts.txt> <r-and-mu.txt> <Zi.txt> <#warmup> <#keep> <library-sizes.txt>\n   -s = save raw STAN file\n")
(model,inFile,outfile,assignFile,numWarmup,numSamples,lib)=args
stanFile=None
for pair in options:
    (key,value)=pair
    if(key=="-s"): stanFile=value

# Read inputs
cell_dict = {}
cellID = []
X = []
L = []

with open(lib, "r") as lib_file:
    for line in lib_file:
        (cell_ID, lib_size) = line.strip().split("\t")
        cell_dict[cell_ID] = lib_size

with open(inFile, "r") as count_file:
    for line in count_file:
        (cell_ID, guide_count) = line.strip().split("\t")
        L.append(cell_dict[cell_ID])
        X.append(guide_count)
        cellID.append(cell_ID)

# Run STAN
(r,mu,disp,LAMBDA, med_LAMBDA, med_mu,  assignments)=runSTAN(model,X,numWarmup,numSamples,INPUT_FILE,INIT_FILE,L)

print("r=",SummaryStats.median(r),
      "\tmu=",SummaryStats.median(mu),"\tlambda=",SummaryStats.median(LAMBDA),sep="")

# Write samples into output file
writeSamples(r,mu,disp, LAMBDA, outfile)
writeAssignments(cellID,assignments,assignFile, med_LAMBDA, med_mu)

# Clean up
if(not DEBUG):
    os.remove(STDERR)
    os.remove(INPUT_FILE)
if(stanFile is None): 
    if(not DEBUG): os.remove(OUTPUT_TEMP)
else: os.system("mv "+OUTPUT_TEMP+" "+stanFile)

