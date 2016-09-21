import sys
import os
import math
from operator import itemgetter

if len(sys.argv) != 5:
	print 'Usage: python ', sys.argv[0], 'input-nbest input-sentBleu input-ref output-name'
	exit()

power_num = 2
range_num = 10
multi_bleu = '~/mosesdecoder/scripts/generic/multi-bleu.perl'

fr_nbest = open(sys.argv[1])
fr_bleu = open(sys.argv[2])
ref_name = sys.argv[3]
output_name = sys.argv[4]

def write_to_file(subList, fw, bool_reverse):
	if len(subList) == 0: return
	if bool_reverse:
		tmpList = sorted(subList, key=itemgetter(2), reverse=True)
	else:
		tmpList = sorted(subList, key=itemgetter(2))
	fw.write(tmpList[0][1]+'\n')

def calculate_multi_bleu(numBest, output_name, allList):
	best_name = '.'.join([output_name, 'best', str(numBest)])
	worst_name = '.'.join([output_name,'worst', str(numBest)])
	fw_best = open (best_name, 'w')
	fw_worst = open(worst_name, 'w')
	subList = []
	count = 0
	oldIndex = 0
	for ele in allList:
		if oldIndex != int(ele[0]):
			write_to_file(subList, fw_best, True)
			write_to_file(subList, fw_worst, False)
			# clear buffer
			count = 0
			oldIndex = int(ele[0])
			subList = []
		else:
			if count < numBest:
				count += 1
				subList.append(ele)
	# last sentence
	if len(subList) != 0:
		write_to_file(subList, fw_best, True)
		write_to_file(subList, fw_worst, False)

	fw_best.close()
	fw_worst.close()

# main
# read all data into list
all_list = []
while True:
	line_nbest = fr_nbest.readline().strip()
	line_bleu = fr_bleu.readline().strip()

	if not line_nbest or not line_bleu:
		break

	sep_nbest = line_nbest.split(' ||| ')
	
	all_list.append([sep_nbest[0], sep_nbest[1], line_bleu])

fr_nbest.close()
fr_bleu.close()

#print 'all_list', len(all_list)

# calculation
for i in range(0, range_num+1):
	n = int(math.pow(power_num,i))
	#n = int(i+1)
	calculate_multi_bleu(n, output_name, all_list) # 1-best, all_list
	best_name = '.'.join([output_name, 'best', str(n)])
	worst_name = '.'.join([output_name,'worst', str(n)])
	print n, 'best'
	os.system(multi_bleu+' '+ref_name+' < '+best_name)
	os.system(multi_bleu+' '+ref_name+' < '+worst_name)

