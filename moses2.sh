stem=$(echo $1 | rev | cut -d'/' -f1 | rev | cut -d'.' -f1)

resultDir=./mout

mkdir -p $resultDir
mkdir -p $resultDir'/'$stem

#LINK TO DEV VERSION!!
#mExec=moses
#mExec=/home/kurekaoru/opencog/X/opencog/learning/moses/main/moses #Switch to use default
mExec=/home/kurekaoru/kurekaoru-opencog-build/opencog/learning/moses/main/moses

mysql -u kaoru -prbdWK2uk -e 'DROP TABLE IF EXISTS MOSES.RESULTS;'

##########################foreach i gen new xval set

datasize=$(($(more $1 | wc -l)-1))
echo 'DATASIZE : '$datasize
binsize=$(($datasize/$2))
echo 'BINSIZE  : '$binsize

remainder=$(($datasize-$binsize*$2))

for i in $(seq 1 $2)
	do
		mkdir -p $resultDir'/'$stem'/FOLD'$i
		echo "FOLD $i OF $2"
		#Create train file
		head -n1 $1 > $resultDir'/'$stem'/FOLD'$i'/FOLD'$i'.train'
		p1=$(($binsize*($2-$i)))
		tail -n "$((datasize-1))" $1 | head -n"$p1" >> $resultDir'/'$stem'/FOLD'$i'/FOLD'$i'.train'
		p2=$(($binsize*($i-1)))
		tail -n"$p2" $1 >> $resultDir'/'$stem'/FOLD'$i'/FOLD'$i'.train'
		#Create test file
		head -n1 $1 > $resultDir'/'$stem'/FOLD'$i'/FOLD'$i'.test'
		head -n"$(($datasize-$p2+1))" $1 | tail -n"$binsize" >> $resultDir'/'$stem'/FOLD'$i'/FOLD'$i'.test'
		#Evoke moses to produce out file (N models)
		$mExec --enable-fs=1 -f $resultDir'/'$stem'/FOLD'$i'/FOLD'$i'.moses.log' -j4 -m 50000 -c 500 -W1 -i $resultDir'/'$stem'/FOLD'$i'/FOLD'$i'.train' > $resultDir'/'$stem'/FOLD'$i'/FOLD'$i'.out'
#		#Analyze out files
		python evalCombo2.py $resultDir'/'$stem'/FOLD'$i'/FOLD'$i $2
		python downstream.py $resultDir'/'$stem'/FOLD'$i'/FOLD'$i
	done
