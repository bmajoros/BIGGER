#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function, 
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
# The above imports should allow this program to run in both Python 2 and
# Python 3.  You might need to update your version of module "future".
import os
import sys
import ProgramName
from MatrixMarket import MatrixMarket
from SlurmWriter import SlurmWriter
from Rex import Rex
rex=Rex()

BASE_DIR="/hpc/group/majoroslab/bigger"
JOB_NAME="GUIDES"
MAX_PARALLEL=300
NUM_WARMUP=300
NUM_KEEP=1000

def getGuideID(group):
    if(len(group)==0): raise Exception("no lines in group")
    line=group[0]
    guideID=line[0]
    return guideID

def writeCounts(group,countsFile):
    with open(countsFile,"wt") as OUT:
        for line in group:
            cellID=line[1]
            count=line[2]
            print(cellID,count,sep="\t",file=OUT)

def writeSlurm(countsFile,slurmFile,dataDir,fileIndex,libSizes):
    samplesFile=dataDir+"/samples/"+str(fileIndex)+".txt"
    posteriorsFile=dataDir+"/posteriors/"+str(fileIndex)+".txt"
    cmd="cd "+BASE_DIR+"\n"+\
        "git/guide-mixture.py git/guide-mixture "+countsFile+" "+samplesFile+" "+\
        posteriorsFile+" "+str(NUM_WARMUP)+" "+str(NUM_KEEP)+" "+\
        " "+libSizes
    slurm.addCommand(cmd)

def getTotalCells(M):
    header=M.getHeader()
    if(len(header)!=3): raise Exception("bad header")
    totalCells=header[1]
    return totalCells

#=========================================================================
# main()
#=========================================================================
if(len(sys.argv)!=5):
    exit(ProgramName.get()+" <in:guides.mtg.gz> <in:lib-sizes.txt> <out:slurm-dir> <out:data-dir>\n")
(guideFile,libSizes,slurmDir,dataDir)=sys.argv[1:]
if(rex.find("(.*)/$",dataDir)): dataDir=rex[1]
if(rex.find("(.*)/$",slurmDir)): slurmDir=rex[1]
if(not os.path.exists(dataDir)): os.makedirs(dataDir)
if(not os.path.exists(dataDir+"/counts")): os.makedirs(dataDir+"/counts")
if(not os.path.exists(dataDir+"/samples")): os.makedirs(dataDir+"/samples")
if(not os.path.exists(dataDir+"/posteriors")): os.makedirs(dataDir+"/posteriors")

slurm=SlurmWriter()
M=MatrixMarket(guideFile)
totalCells=None
while(True):
    group=M.nextGroup(0)
    if(group is None): break
    guideID=getGuideID(group)
    if(totalCells is None): totalCells=getTotalCells(M)
    countsFile=dataDir+"/counts/"+str(guideID)+".txt"
    writeCounts(group,countsFile)
    slurmFile=slurmDir+"/slurm-"+str(guideID)+".slurm"
    writeSlurm(countsFile,slurmFile,dataDir,guideID,libSizes)
    
slurm.mem(1500)
slurm.setQueue("scavenger")
slurm.writeArrayScript(slurmDir,JOB_NAME,MAX_PARALLEL);



