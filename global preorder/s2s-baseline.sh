#!  /bin/bash

F=zh
E=en
LANG=zh-en
FLAG=ss2
export LC_ALL=C
work_dir=${HOME}/iwslt_ex
exp_dir=${work_dir}/${LANG}
train_dir=train
dev_dir=dev
cd ${exp_dir}
SCRIPTS_ROOTDIR=/smt/mosesdecoder/scripts
BIN_DIR=/smt/giza-bin-dir/

LM=${work_dir}/${LANG}/data/lm/train.tok.true.kblm.${E}
FIRST=1
LAST=9
ROOT_DIR=${exp_dir}/${FLAG}/iwslt-${LANG}-ss-baseline
CORPUS=${exp_dir}/data/${train_dir}/train.stantok.true.clean

#train
${SCRIPTS_ROOTDIR}/training/train-model.perl \
	--corpus ${CORPUS} \
	--f ${F} --e ${E} \
	--root-dir ${ROOT_DIR} \
	--external-bin-dir ${BIN_DIR} \
	--lm 0:4:${LM}:8 \
	--reordering msd-bidirectional-fe \
	--alignment grow-diag-final-and
#MERT
#MERT_DIR=/smt/mosesdecoder/bin/
#IN_FILE=${exp_dir}/${FLAG}/${dev_dir}/dev.tok.true.clean.${F}
#REF_FILE=${exp_dir}/${FLAG}/${dev_dir}/dev.tok.true.clean.${E}
#MOSES_INI=${ROOT_DIR}/model/moses.ini
#MOSES_EXE=/smt/mosesdecoder/bin/moses


#${SCRIPTS_ROOTDIR}/training/mert-moses.pl ${IN_FILE} ${REF_FILE} ${MOSES_EXE} ${MOSES_INI} --threads 4 --mertdir ${MERT_DIR} > mert.${E}.out
