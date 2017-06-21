#!/bin/bash
#SBATCH --job-name		moses
#SBATCH --partition 		NLP2CT
#SBATCH --nodes		 1	
#SBATCH --tasks-per-node	1
#SBATCH --cpus-per-task		1
#SBATCH --mem			50G
#SBATCH --time			8760:00:00	# Hours
#SBATCH --output        	bjunk.%j.out
#SBATCH --error         	bjunk.%j.err
#SBATCH --mail-type		ALL
#SBATCH --mail-user		lobichai@hotmail.com			# Please specify your email address

source /etc/profile
source /etc/profile.d/modules.sh

module add impi/5.1.3
module add intel/16.0.3
module load gcc

SCRIPT_HOME=`pwd` 
module add java/jdk1.7.0_9 
export LC_ALL=C

exp_dir=/home/mb45450/derek/
setup_folder=wrapper

SCRIPTS_ROOTDIR=/home/mb45450/mosesdecoder/scripts
BIN_DIR=/home/mb45450/mosesdecoder/tools
SUPPORT_DIR=/home/mb15505/Research/toolkits/mosesdecoder/scripts/ems/support
FAST_ALIGN_BIN=/home/mb15505/Research/tmp/Fast_Align/fast_align-master
SYMAL_DIR=/home/mb15505/Research/toolkits/mosesdecoder/bin/symal

F=zh
E=pt

CORPUS=${exp_dir}/wrapper/sentence

ROOT_DIR=${exp_dir}/${setup_folder}
mkdir -p ${exp_dir}/${setup_folder}/model
cd ${ROOT_DIR}

LM_TYPE=9
ORDER=5
LM_MODEL=/home/mb45450/GroundHog-master/experiments_pt_zh/nmt/moses-baseline/data/lm/kblm.zh

#${SUPPORT_DIR}/prepare-fast-align.perl ${CORPUS}.${F} ${CORPUS}.${E} > ${ROOT_DIR}/corpus.pre.${F}-${E}

#${FAST_ALIGN_BIN}/fast_align -i ${ROOT_DIR}/corpus.pre.${F}-${E} -d -o -v > ${ROOT_DIR}/forward.aligned.${F}-${E} &
#${FAST_ALIGN_BIN}/fast_align -i ${ROOT_DIR}/corpus.pre.${F}-${E} -d -o -v -r > ${ROOT_DIR}/inverse.aligned.${F}-${E}
#wait

#rm ${ROOT_DIR}/corpus.pre.${F}-${E}

#${SUPPORT_DIR}/symmetrize-fast-align.perl ${ROOT_DIR}/forward.aligned.${F}-${E} ${ROOT_DIR}/inverse.aligned.${F}-${E} ${CORPUS}.${F} ${CORPUS}.${E} ${ROOT_DIR}/model/aligned grow-diag-final-and ${SYMAL_DIR}

#rm ${ROOT_DIR}/forward.aligned.${F}-${E}
#rm ${ROOT_DIR}/inverse.aligned.${F}-${E}

FIRST=4
LAST=4

${SCRIPTS_ROOTDIR}/training/train-model.perl \
	--first-step ${FIRST} \
	--last-step ${LAST} \
	--corpus ${CORPUS} \
	--f ${F} --e ${E} \
	--root-dir ${ROOT_DIR} \
	--lm 0:${ORDER}:${LM_MODEL}:${LM_TYPE} \
	--reordering-factors 0-0 \
	--alignment grow-diag-final-and \
	--reordering distance,msd-bidirectional-fe

