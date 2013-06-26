#foldDataset.py

import sys
import random

IFILE = sys.argv[1]
TSFILE = sys.argv[2]
TRFILE = sys.argv[3]
TSSIZE = int(sys.argv[4])

#IFILE = '../data/GDS3688R.soft.moses'
#IFILE = '../data/test.moses'
#TSFILE = 'testtest.moses'
#TRFILE = 'testtrain.moses'

def complement(L1,L2):
	M = {}
	O = {}
	for x in L1:
		M[x] = True
	for x in L2:
		if x not in M: O[x] = True
	return O.keys()

F = open(IFILE).readlines()

NDATA = len(F[1:])

ALLLINES = range(1,len(F))

TESTLINES = [x+1 for x in random.sample(range(NDATA),TSSIZE)]
TRAINLINES = complement(TESTLINES,ALLLINES)

#TESTSET
TSFILE = open(TSFILE,'w')
TSFILE.write(F[0])
for x in TESTLINES:
	TSFILE.write(F[x])

TSFILE.close()

#TRAINSET
TRFILE = open(TRFILE,'w')
TRFILE.write(F[0])
for x in TRAINLINES:
	TRFILE.write(F[x])

TRFILE.close()

