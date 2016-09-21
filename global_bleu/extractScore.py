import sys
import os
import re

if len(sys.argv) != 3:
	print 'usage: python', sys.argv[0], 'input_nbest output_score'
	sys.exit();
	
fr = open(sys.argv[1], 'r')
fw = open(sys.argv[2], 'w')


# input format 
# index ||| translated sentence ||| scores ||| final score
for line in fr:
	seplll = line.split(' ||| ')
	index = seplll[0]
	scores = re.sub(r'[a-zA-Z]+0= ', '', seplll[2])
	fw.write(scores+'\n')
	
fr.close()
fw.close()
	
