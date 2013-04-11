stem=$(echo $1 | rev | cut -d'/' -f1 | rev | cut -d'.' -f1)

#Handle optional flag args
#eval set -- $(getopt -n $0 -o "-cBdz:" -- "$@")

#declare c B d z
#declare -a files
#while [ $# -gt 0 ] ; do
#        case "$1" in
#                -c) r=1 ; shift ;;
#                -B) v=1 ; shift ;;
#                -d) x=1 ; shift ;;
#                -z) shift ; l="$1" ; shift ;;
#                --) shift ;;
#                -*) echo "bad option '$1'" ; exit 1 ;;
#                *) files=("${files[@]}" "$1") ; shift ;;
#         esac
#done

#if [ ${#files} -eq 0 ] ; then
#        echo No input file specified!
#        exit 1
#fi

resultDir=./moses_out/

mkdir -p $resultDir

#LINK TO DEV VERSION!!
#mExec=moses
#mExec=/home/kurekaoru/opencog/X/opencog/learning/moses/main/moses #Switch to use default
mExec=/home/kurekaoru/kurekaoru-opencog-build/opencog/learning/moses/main/moses

##########################foreach i gen new xval set

datasize=$(($(more $1 | wc -l)-1))
echo 'DATASIZE : '$datasize
binsize=$(($datasize/$2))
echo 'BINSIZE  : '$binsize

remainder=$(($datasize-$binsize*$2))
#echo $remainder

for i in $(seq 1 $2)
	do
		echo "FOLD $i OF $2"
		#Create train file
		head -n1 $1 > $resultDir$stem'_'$i'.train'
		p1=$(($binsize*($2-$i)))
		tail -n "$((datasize-1))" $1 | head -n"$p1" >> $resultDir$stem'_'$i'.train'
		p2=$(($binsize*($i-1)))
		tail -n"$p2" $1 >> $resultDir$stem'_'$i'.train'
		#Create test file
		head -n1 $1 > $resultDir$stem'_'$i'.test'
		head -n"$(($datasize-$p2+1))" $1 | tail -n"$binsize" >> $resultDir$stem'_'$i'.test'
		#Evoke moses to produce out file (N models)
		$mExec --enable-fs=1 -f $resultDir$stem'_'$i'.moses.log' -c 100 -W1 -i $resultDir$stem'_'$i'.train' > $resultDir$stem'_'$i'.out'
		#Analyze out files
		python evalCombo.py $resultDir$stem'_'$i $2
	done
