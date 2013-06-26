import glob
import numpy
import sys
sys.path.insert(0, '../PyUtils')
from kfuncs import *

#inputDir = '../Test'
inputDir = sys.argv[1]

Files = glob.glob(inputDir+'/*.moses')

def enumerateMap(M):
	OM = {}
	c = 0
	for x in M:
		OM[x] = c
		c+=1
	return OM

def groupMap(Group, M):
	out = []
	for x in Group:
		out.append(M[x])
	return out

def getByIndex(SET, INDECES):
	out = []
	for x in INDECES:
		out.append(SET[x])
	return numpy.array(out)

if __name__ == '__main__':
	if len(Files) > 1:
		F = numpy.array([numpy.array([y.strip().split('\t') for y in open(x).readlines()]) for x in Files])
		Features = [x[0] for x in F]
		iFeatures = groupIntersection(Features)
		FINAL = [['out']+iFeatures]
		for x in F:
			iMap = enumerateMap(x[0])
			indeces = [0]+[iMap[y] for y in iFeatures]
			for z in x[1:]:
				FINAL.append(getByIndex(z,indeces))
	FINAL = numpy.array(FINAL)
	outfile = open(sys.argv[2],'w')
	for x in FINAL:
		outfile.write('\t'.join(x)+'\n')


