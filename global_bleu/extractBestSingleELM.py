import sys
import os
from operator import itemgetter

if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], 'input-guess input-id_sent output_best'
	exit()

fr_bleu = open(sys.argv[1], 'r')
fr_sent = open(sys.argv[2], 'r')
fw_best = open(sys.argv[3], 'w')

def saveSentenceIntoFile(resultList, fileWriter):
	if len(resultList) != 0:
		# sort the result according to bleu score
		sortedList = sorted(resultList, key=itemgetter(0), reverse=True)
		fileWriter.write(sortedList[0][1]+'\n') # select the best sentence

oldIndex = 0
oldList = []

while True:
	line_bleu = fr_bleu.readline()
	line_sent = fr_sent.readline()
	if not line_bleu or not line_sent:
		break
	
	# take out id and sentence
	sep = line_sent.strip().split(' ||| ')	

	index = int(sep[0])
	sent = sep[1]

	# new sentence found
	if index != oldIndex:
		saveSentenceIntoFile(oldList, fw_best)
		oldList = []
		oldIndex = index

	oldList.append([float(line_bleu.strip()), sent])

# write the last sentence into file
saveSentenceIntoFile(oldList, fw_best)

fr_bleu.close()
fr_sent.close()
fw_best.close()	
		
