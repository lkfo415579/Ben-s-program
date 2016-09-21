import sys
import os

if len(sys.argv) != 5:
	print 'Usage: python', sys.argv[0], 'num-nbest in-nbest in-bleu out-name'
	exit()

num_nbest = int(sys.argv[1])
fr_nbest = open(sys.argv[2], 'r')
fr_bleu = open(sys.argv[3], 'r')
fw_out = open(sys.argv[4], 'w')

fw_out.write('sent, line, moses, bleu\n')

nbest_count = 0
nbest_id = 0
while True:
	line_nbest = fr_nbest.readline().strip()
	line_bleu = fr_bleu.readline().strip()

	if not line_nbest or not line_bleu:
		break

	sep_nbest = line_nbest.split(' ||| ') 

	if nbest_id != int(sep_nbest[0]):
		nbest_count = 1
		nbest_id = int(sep_nbest[0])
	else:
		nbest_count += 1

	if nbest_count < num_nbest:
		fw_out.write(','.join([sep_nbest[0], str(nbest_count), sep_nbest[-1], line_bleu]) + '\n')

fr_nbest.close()
fr_bleu.close()
fw_out.close()
