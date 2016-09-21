[ $# -eq 0 ] && { 
	echo "Usage: sh $0 [source] [target] [output_tmp_folder]";
	echo "	Source and target file should not contain line with 0-length."
	echo "	Otherwise, the alignment will stop earlier."
	exit -1;
}

program_path=/home/mb45450/program
source=$1
target=$2
output_directory=$3

mkdir -p $output_directory

perl $program_path/fastAlign/prepare-fast-align.perl $source $target > $output_directory/corpus.pre.zh-pt

$program_path/fastAlign/fast_align-master/fast_align -i $output_directory/corpus.pre.zh-pt -d -o -v > $output_directory/forward.aligned.zh-pt &

$program_path/fastAlign/fast_align-master/fast_align -i $output_directory/corpus.pre.zh-pt -d -o -v -r > $output_directory/inverse.aligned.zh-pt

wait

$program_path/fastAlign/symmetrize-fast-align.perl $output_directory/forward.aligned.zh-pt $output_directory/inverse.aligned.zh-pt $source $target $output_directory/aligned grow-diag-final-and $program_path/fastAlign/symal > $output_directory/aligned.grow-diag-final-and 

