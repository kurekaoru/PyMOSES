#Downstream.py

import glob
import sys
import numpy

sys.path.insert(0, '../PyUtils')
from sqlutils import *
from kfuncs import *
from matchCombo import *

OF = sys.argv[1]

def SQL_translateList(IDS):
	out = []
	for x in IDS:
		GN = doQuery('SELECT Gene_symbol FROM xref.U133 WHERE mid = \''+x+'\'')[0][0]
		print GN
		if GN != "":
			out.append(GN)
		else:
			out.append(x)
	return out

MODELS = doQuery('SELECT * FROM MOSES.RESULTS WHERE MODEL !=\'true\' AND MODEL NOT LIKE \'%out%\' AND (_11+_10)/(_11+_10+_01+_10) > 0.8')

M = {}

markertype = 'gene'
signiture = ''

if markertype == 'gene':
	signiture = '\$\S*[\s|$|)|(]'

if markertype == 'snp':
	signiture = '\$\d{6}(_.{1,2})?_at'


for x in MODELS:
	Markers = [x.replace('$','').replace(' ','').replace(')','') for x in getAllMatches(x[3], signiture)]
	for y in Markers:
		insertOrCount(M,y.replace('$',''))

sortedM = sortMap(M)

if markertype == 'snp':
	genes = [numpy.array([x[0] for x in SQL_translateList(sortedM[0])]),sortedM[1]]

if markertype == 'gene':
	genes = sortedM[:]

outfile = open(OF,"w")

for i in range(len(genes[0])):
	genename = genes[0][i]
	if genename == '':
		genename = sortedM[0][i]
	outfile.write(genename+'\t'+genes[1][i]+'\n')

outfile.close()
