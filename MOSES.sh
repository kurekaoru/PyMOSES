#python ../PyGEO/geo2moses.py $1
stem=$(echo $1 | rev | cut -d'/' -f1 | rev | cut -d'.' -f1)
resultDir=./mout

mkdir -p $resultDir
mkdir -p $resultDir'/'$stem
rm -rf $resultDir'/temp/'

ifile=

while getopts i:I: opt; do
	case $opt in
		i)
			ifile=$OPTARG
		;;
		I)
			ifile=$OPTARG
		;;
	esac
done

python ../PyGEO/geo2moses.py -i $1 -p 0.2 #-o $resultDir'/temp/'$stem'.moses'
./moses3.sh $1'.moses' $2

