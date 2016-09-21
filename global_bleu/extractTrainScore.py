import sys
import os
import re

if len(sys.argv) != 6:
	print 'usage: python', sys.argv[0], 'first_nbest input_nbest input_bleu output_score output_bleu'
	sys.exit();
	
n_best = int(sys.argv[1])
fr_nbest = open(sys.argv[2], 'r')
fr_bleu = open(sys.argv[3], 'r')
fw_score = open(sys.argv[4], 'w')
fw_bleu = open(sys.argv[5], 'w')

# input format 
# index ||| translated sentence ||| scores ||| final score
oldIndex=-1
bestCount=1
writeFlag=False

while True:
	line_nbest = fr_nbest.readline()
	line_bleu = fr_bleu.readline()

	if not line_nbest or not line_bleu:
		break

	# separate input
	seplll = line_nbest.split(' ||| ')
	# extract part of input
	index = int(seplll[0])

	# new source sentence
	if index != oldIndex:
		oldIndex = index
		writeFlag = True	
		bestCount = 1

	# meet n-best
	if bestCount > n_best:
		writeFlag = False

	# write to file
	if writeFlag:
		scores = re.sub(r'[a-zA-Z]+0= ', '', seplll[2])
		fw_score.write(scores+'\n')
		fw_bleu.write(line_bleu)
	
	bestCount += 1
fr_nbest.close()
fr_bleu.close()
fw_score.close()
fw_bleu.close()
