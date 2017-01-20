import sys
import os

if len(sys.argv) != 5:
	print 'Usage: python', sys.argv[0], '[input] [output] [pr_from] [pr_to]'
	exit()

inputFile = sys.argv[1]
outputFile = sys.argv[2]
pr_from = float(sys.argv[3])
pr_to = float(sys.argv[4])

fr = open(inputFile, 'r')
fw = open(outputFile, 'w')

index = 0
for line in fr:
	index += 1
	if index % 100 == 0:
		sys.stdout.write('%d \r' % index)
		sys.stdout.flush()

	pr = float(line.strip().split(' ')[2])
	if pr > pr_from and pr < pr_to:
		fw.write(line)

fr.close()
fw.close()
