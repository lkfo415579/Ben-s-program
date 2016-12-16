exp_dir=/home/mb45450/GroundHog-master/experiments_pt_zh/nmt/moses-baseline

F=pt
E=zh

WORK_DIR=${exp_dir}/mert
IN_FILE=${exp_dir}/data/dev/dev.${F}
REF_FILE=${exp_dir}/data/dev/dev.${E}
MOSES_INI=${exp_dir}/model/moses.ini

module load gcc

/home/mb45450/mosesdecoder/scripts/training/mert-moses.pl ${IN_FILE} ${REF_FILE} /home/mb45450/mosesdecoder/bin/moses ${MOSES_INI} \
	--mertdir /home/mb45450/mosesdecoder/bin/ \
	--working-dir ${WORK_DIR} \
	--decoder-flags '-threads 8'
	
#mv $WORK_DIR/moses.ini $WORK_DIR/../model/moses.mert.ini
#rm -rf $WORK_DIR
