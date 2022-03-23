#!/usr/bin/env python
#=========================================================================
# Copyright (C)2021 William H. Majoros <bmajoros@alumni.duke.edu> and
# Susan Liu.
#
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
#=========================================================================
from __future__ import (absolute_import, division, print_function, 
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
# The above imports should allow this program to run in both Python 2 and
# Python 3.  You might need to update your version of module "future".
import pandas as pd
import numpy as np
import scipy
from scipy.optimize import minimize
import sys
import statistics
import os
import ProgramName
import gzip
import csv

#=========================================================================
# main()
#=========================================================================

if len(sys.argv)!=3:
    exit(ProgramName.get()+"<sorted-mrna.mtx.gz> <normalization-file>\n")
(mrna_file, norm_file) = sys.argv[1:]

umi_list = []
cellid_list = []
norm_list = []
norm_dict ={} # cell -> normalization factor

with gzip.open(mrna_file, "r") as mtx:
    mtx.readline()
    mtx.readline()
    mtx.readline()
    for line in mtx:
        line = line.decode("utf8")
        if "\t" in line:
            (gene,cell,lib) = line.strip().split("\t")
        else:
            (gene,cell,lib) = line.strip().split(" ")
        ###################################
        if gene == "7": #################
            umi_list.append(int(lib))
            cellid_list.append(cell)
        ####################################

with open(norm_file, "r") as norm_file:
    for line in norm_file:
        (cell, norm) = line.strip().split("\t")
        norm_dict[cell] = float(norm)

for cellid in cellid_list:
    norm_list.append(norm_dict[cellid])

umi_array = np.array(umi_list)
cellid_array = np.array(cellid_list)
norm_array = np.array(norm_list)
input_data = [umi_array, norm_array]

def neg_bin(input_data, args):
    s=0
    umis = input_data[0]
    norms = input_data[1]
    (mu,phi) = args
    for i in range(len(umis)):
        mu_norm = mu*norms[i]
        var = mu_norm*(1+(mu_norm/phi))
        p = (var-mu_norm)/var
        n = mu_norm**2/(var-mu_norm)
        likelihood = nbinom.pmf(umis[i], n, p)
        s+= -log(likelihood)
    final = s    
    return final
res = minimize(neg_bin, input_data, args, method='BFGS', options={'disp': True})





    



