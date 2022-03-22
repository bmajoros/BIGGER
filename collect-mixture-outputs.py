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
import os
import sys
import ProgramName
from Rex import Rex
rex=Rex()

def processFile(infile,guideID,OUT):
    with open(infile,"rt") as IN:
        for line in IN:
            fields=line.rstrip().split()
            if(len(fields)!=2): raise Exception("Wrong number of fields")
            (cellID,P)=fields
            P=round(float(P),3)
            print(guideID,cellID,P,sep="\t",file=OUT)

#=========================================================================
# main()
#=========================================================================
if(len(sys.argv)!=3):
    exit(ProgramName.get()+" <mixture-out/popsteriors> <output.mtx.gz>\n")
(posteriorsDir,outFile)=sys.argv[1:]

OUT=open(outFile,"wt")
files=os.listdir(posteriorsDir)
files.sort(key=lambda x: int(x.split(".")[0]))
for filename in files:
    if(not rex.find("(\d+)\.txt$",filename)):
        raise Exception("Can't parse filename: "+filename)
    guideID=rex[1]
    processFile(posteriorsDir+"/"+filename,guideID,OUT)

