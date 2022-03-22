#!/usr/bin/env python
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
#=========================================================================
# main()
#=========================================================================
if len(sys.argv)!=3:
    exit(ProgramName.get()+"<in:library-sizes.txt> <out:normalization-factors.txt>\n")
(lib_size,outFile)=sys.argv[1:]

norm_dict = {}
count = 0
tot_size = 0

with open(lib_size, "r") as lib_file:
    for line in lib_file:
        (cell_num, size) = line.rstrip().split("\t")
        count += 1
        tot_size += int(size)
        norm_dict[cell_num] = size

avg_size = float(tot_size)/float(count)

OUT=open(outFile,"wt")
for key_cell in norm_dict:
    lib_size = float(norm_dict[key_cell])
    norm_size = lib_size/avg_size
    print(key_cell, round(norm_size,4), sep = "\t", file=OUT)
OUT.close()


