import sys
import os
import re

if len(sys.argv) != 5:
	print 'usage: python', sys.argv[0], 'first_nbest input_nbest output_score output_sentence'
	sys.exit();
	
n_best = int(sys.argv[1])
fr = open(sys.argv[2], 'r')
fw = open(sys.argv[3], 'w')
fs = open(sys.argv[4], 'w')


# input format 
# index ||| translated sentence ||| scores ||| final score
oldIndex=-1
bestCount=1
writeFlag=False

for line in fr:
	# separate input
	seplll = line.split(' ||| ')
	# extract part of input
	index = int(seplll[0])
	scores = re.sub(r'[a-zA-Z]+0= ', '', seplll[2])

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
		fw.write(scores+'\n')
		fs.write(str(index)+' ||| '+seplll[1]+'\n')
	
	bestCount += 1
fr.close()
fw.close()
fs.close()
