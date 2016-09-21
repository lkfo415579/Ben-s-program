import sys
import os
from operator import itemgetter

if len(sys.argv) != 5:
	print 'Usage: python', sys.argv[0], '[Max|Min] [input-score] [input-id_sent] [output_best]'
	exit()

option = sys.argv[1]
fr_score = open(sys.argv[2], 'r')
fr_sent = open(sys.argv[3], 'r')
fw_best = open(sys.argv[4], 'w')

def saveSentenceIntoFile(resultList, fileWriter):
	if len(resultList) != 0:
		reverseOption = True if option == 'Max' else False
		# sort the result according to score
		sortedList = sorted(resultList, key=itemgetter(0), reverse=reverseOption)
		fileWriter.write(sortedList[0][1]+'\n') # select the best sentence

oldIndex = 0
oldList = []

currentProgram = sys.argv[0]
print currentProgram, ': extracting the best sentences...'
while True:
	line_score = fr_score.readline()
	line_sent = fr_sent.readline()
	if not line_score or not line_sent:
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

	oldList.append([float(line_score.strip()), sent])

# write the last sentence into file
saveSentenceIntoFile(oldList, fw_best)

fr_score.close()
fr_sent.close()
fw_best.close()	
		
print currentProgram, ': end of program'
