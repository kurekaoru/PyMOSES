#python ../PyGEO/geo2moses.py $1
resultDir=./mout

mkdir -p $resultDir
rm -rf $resultDir'/temp/'
mkdir -p $resultDir'/temp/'

ifile=
nFolds=

while getopts i:I:n: opt; do
	case $opt in
		i)
			ifile=$OPTARG
			stem=$(echo $ifile | rev | cut -d'/' -f1 | rev | cut -d'.' -f1)
			python ../PyGEO/geo2moses.py -i $ifile -p 0.5 -o $stem'.moses'
			ifile=$stem'.moses';;
		I)
			F=$OPTARG
			python mergeMoses.py $F $resultDir'/temp/COMBINED.moses'
			ifile=$resultDir'/temp/COMBINED.moses'
			echo '-I Flag on, Created combined file '$ifile
		;;
		n) nFolds=$OPTARG;;
	esac
done

stem=$(echo $ifile | rev | cut -d'/' -f1 | rev | cut -d'.' -f1)
mkdir -p $resultDir'/'$stem

echo ./moses3.sh $ifile $nFolds

./moses3.sh $ifile $nFolds


