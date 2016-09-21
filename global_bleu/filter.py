import sys
import os

if len(sys.argv) != 5:
	print 'Usage: python', sys.argv[0], 'input-nbest input-bleu output-nbest output-bleu'
	exit()

fr_nbest = open(sys.argv[1], 'r')
fr_bleu = open(sys.argv[2], 'r')
fw_nbest = open(sys.argv[3], 'w')
fw_bleu = open(sys.argv[4], 'w')

while True:
	nbest_line = fr_nbest.readline()
	bleu_line = fr_bleu.readline()

	if not nbest_line or not bleu_line:
		break
	
	if float(bleu_line.strip()) < 0.5:
		fw_nbest.write(nbest_line)
		fw_bleu.write(bleu_line)

fr_nbest.close()
fr_bleu.close()
fw_nbest.close()
fw_bleu.close()

