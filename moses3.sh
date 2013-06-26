stem=$(echo $1 | rev | cut -d'/' -f1 | rev | cut -d'.' -f1)

resultDir=./mout

#mkdir -p $resultDir
#mkdir -p $resultDir'/'$stem

#LINK TO DEV VERSION!!
#mExec=moses
mExec=/home/kurekaoru/kurekaoru-opencog-build/opencog/learning/moses/main/moses
#mExec=/home/kaoru/uopencog/opencog/learning/moses/main/moses #For poly ubuntu machine

mysql -u kaoru -prbdWK2uk -e 'DROP TABLE IF EXISTS MOSES.RESULTS;'

##########################foreach i gen new xval set

datasize=$(($(more $1 | wc -l)-1))
echo 'DATASIZE : '$datasize
tsize=$(($datasize/2))
echo 'RANDOMIZED TEST DATASET SIZE: '$tsize

for i in $(seq 1 $2)
	do
		mkdir -p $resultDir'/'$stem'/FOLD'$i
		echo "FOLD $i OF $2"
		python foldDataset.py $1 $resultDir'/'$stem'/FOLD'$i'/FOLD'$i'.test' $resultDir'/'$stem'/FOLD'$i'/FOLD'$i'.train' $tsize
		#Evoke moses to produce out file (N models)
		$mExec --enable-fs=1 -f $resultDir'/'$stem'/FOLD'$i'/FOLD'$i'.moses.log' -j4 -m 1000000 -c 500 -W1 -i $resultDir'/'$stem'/FOLD'$i'/FOLD'$i'.train' > $resultDir'/'$stem'/FOLD'$i'/FOLD'$i'.out'
		#Analyze out files
		python evalCombo2.py $resultDir'/'$stem'/FOLD'$i'/FOLD'$i $2
		python downstream.py $resultDir'/'$stem'/FOLD'$i'/FOLD'$i
	done
