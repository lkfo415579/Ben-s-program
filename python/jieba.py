import jieba
import sys
import os

#if len(sys.argv) != 3:
#	print 'Usage: python', sys.argv[0], 'input output'
#	exit()

fr = open(sys.argv[1], 'r')
fw = open(sys.argv[2], 'w')

for line in fr:
	seg_list = jieba.cut(line.strip())
	fw.write(' '.join(seg_list))

fr.close()
fw.close()

