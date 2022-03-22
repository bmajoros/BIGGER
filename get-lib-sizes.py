#!/usr/bin/env python
#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Author:Susan Liu
#=========================================================================
from __future__ import (absolute_import, division, print_function, 
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
# The above imports should allow this program to run in both Python 2 and
# Python 3.  You might need to update your version of module "future".
import sys
import statistics
import os
import ProgramName
import gzip

#=========================================================================
# main()
#=========================================================================

if len(sys.argv)!=3:
    exit(ProgramName.get()+" <in:mRNA.mtx.gz> <out:library-sizes.txt>\n")
(mtxFile,outFile)=sys.argv[1:]

d={}
with gzip.open(mtxFile,"r") as matr:
    matr.readline()
    matr.readline()
    matr.readline()
    for line in matr:
        line = line.decode("utf8")
        (guide,cell,lib)=line.strip().split()
        if cell in d:
            d[cell]+=int(lib)
        else:
            d[cell]=int(lib)

OUT=open(outFile,"wt")
for key in d:
    print(key,d[key],sep="\t",file=OUT)
OUT.close()
