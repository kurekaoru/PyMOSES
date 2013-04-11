#evalCombo.py

import numpy
import os
import sys
import glob
try:
	import progressbar as P
	pbar_exists = True
except ImportError: 
	pbar_exists = False

STEM = sys.argv[1]
#FILES = glob.glob('./moses_FSout/MF*')
#STEM = 'moses_FSout/MF1'

#open model file
MODELS = open(STEM+'.out').readlines()

#open test file
TEST = open(STEM+'.test').readlines()

def getOut(Data):
	return [int(x.split('\t')[0]) for x in Data[1:]]

OBS = getOut(TEST)
print OBS

os.system('mkdir -p '+STEM+'_EVAL')
os.system('mkdir -p '+STEM+'_RESULT')

def removeScore(comboLine):
	return ' '.join(comboLine.strip().split(' ')[1:])

c = 1
GFILE = open(STEM+'_RESULT/RFINAL.result',"w")
GCONFUSION = [0,0,0,0]

if pbar_exists:
	widgets = ["Evaluating combos: ", P.Percentage(), P.Bar()]
	pbar = P.ProgressBar(maxval=100, widgets=widgets).start()

maxacc = 0
maxprec = 0
maxsens = 0
maxspec = 0

#etExec = '/home/kurekaoru/opencog/X/opencog/comboreduct/main/eval-table'
etExec = 'eval-table'

c = 0
for x in MODELS:
	CONFUSION = [0,0,0,0]
	oneliner = open(STEM+'_EVAL/M'+str(c)+'.model','w')
	M = removeScore(x)
	oneliner.write(M)
	oneliner.close()
	if pbar_exists:
		pbar.update(pbar.currval + 1)
		pass
	os.system(etExec+' -i '+STEM+'.test -f '+STEM+'.eval.log'+' -C '+STEM+'_EVAL/M'+str(c)+'.model -o '+STEM+'_RESULT/R'+"%03d"% c+'.result')
	PRD = [int(x.strip()) for x in open(STEM+'_RESULT/R'+"%03d"% c+'.result').readlines()[1:]]
	if len(PRD) > len(OBS): PRD = PRD[0:len(OBS)] #Work around eval-table bug
	for i in range(len(PRD)):
		if (OBS[i] == 1 and PRD[i] == 1):
			CONFUSION[0]+=1
			GCONFUSION[0]+=1
		elif (OBS[i] == 1 and PRD[i] == 0):
			CONFUSION[1]+=1
			GCONFUSION[1]+=1
		elif (OBS[i] == 1 and PRD[i] == 0):
			CONFUSION[2]+=1
			GCONFUSION[2]+=1
		else:
			CONFUSION[3]+=1
			GCONFUSION[3]+=1
	acc = float((CONFUSION[0]+CONFUSION[3])/float(sum(CONFUSION)))
	if CONFUSION[0]+CONFUSION[1] > 0:
		prec = float((CONFUSION[0])/float(CONFUSION[0]+CONFUSION[1]))
	else:
		prec = 1.0
	if CONFUSION[0]+CONFUSION[2] > 0:
		sens = float((CONFUSION[0])/float(CONFUSION[0]+CONFUSION[2]))
	else:
		sens = 0.0
	if CONFUSION[3]+CONFUSION[1] > 0:
		spec = float((CONFUSION[3])/float(CONFUSION[3]+CONFUSION[1]))
	else:
		spec = 0.0
	if acc > maxacc: maxacc = acc
	if prec > maxprec: maxprec = prec
	if sens > maxsens: maxsens = sens
	if spec > maxspec: maxspec = spec
	RFILE = open(STEM+'_RESULT/R'+"%03d"% c+'.result',"a")
	RFILE.write('CONFUSION MATRIX:\n')
	RFILE.write(str(CONFUSION[0])+'\t'+str(CONFUSION[1])+'\n')
	RFILE.write(str(CONFUSION[2])+'\t'+str(CONFUSION[3])+'\n')
	RFILE.write('ACCURACY: ')
	RFILE.write("%02f"%acc)
	RFILE.write('\n')
	RFILE.write('PRECISION: ')
	RFILE.write("%02f"%prec)
	RFILE.write('SENSITIVITY: ')
	RFILE.write("%02f"%sens)
	RFILE.write('SPECIFICITY: ')
	RFILE.write("%02f"%spec)
	RFILE.write('\nMODEL:\n')
	RFILE.write(M)
	RFILE.close()
	c+=1

if pbar_exists: pbar.finish()

GFILE.write('>>>CONFUSION MATRIX:\n')
GFILE.write(str(GCONFUSION[0])+'\t'+str(GCONFUSION[1])+'\n')
GFILE.write(str(GCONFUSION[2])+'\t'+str(GCONFUSION[3])+'\n\n')
GFILE.write('>>ACCURACY:\tMEAN\tBEST\n')
GFILE.write("%02f"%float((GCONFUSION[0]+GCONFUSION[3])/float(sum(GCONFUSION))))
GFILE.write('\t'+str(maxacc))
print 'ACCURACY:\t'+"%02f"%float((GCONFUSION[0]+GCONFUSION[3])/float(sum(GCONFUSION)))+' ('+str(maxacc)+')'
if GCONFUSION[0]+GCONFUSION[1] > 0:
	GFILE.write('\n\n')
	GFILE.write('>>PRECISION:\tMEAN\tBEST\n')
	GFILE.write("%02f"%float((GCONFUSION[0])/float(GCONFUSION[0]+GCONFUSION[1])))
	print 'PRECISION:\t'+"%02f"%float((GCONFUSION[0])/float(GCONFUSION[0]+GCONFUSION[1]))+' ('+str(maxprec)+')'
	GFILE.write('\t'+str(maxprec))
if GCONFUSION[0]+GCONFUSION[2] > 0:
	GFILE.write('\n\n')
	GFILE.write('>>SENSITIVITY:\tMEAN\tBEST\n')
	GFILE.write("%02f"%float((GCONFUSION[0])/float(GCONFUSION[0]+GCONFUSION[2])))
	print 'SENSITIVITY:\t'+"%02f"%float((GCONFUSION[0])/float(GCONFUSION[0]+GCONFUSION[2]))+' ('+str(maxsens)+')'
	GFILE.write('\t'+str(maxsens))
if GCONFUSION[3]+GCONFUSION[1] > 0:
	GFILE.write('\n\n')
	GFILE.write('>>SPECIFICITY:\tMEAN\tBEST\n')
	GFILE.write("%02f"%float((GCONFUSION[3])/float(GCONFUSION[3]+GCONFUSION[1])))
	print 'SPECIFICITY:\t'+"%02f"%float((GCONFUSION[3])/float(GCONFUSION[3]+GCONFUSION[1]))+' ('+str(maxspec)+')'
	GFILE.write('\t'+str(maxspec))

GFILE.close()

#print TEST
