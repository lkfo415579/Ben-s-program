import jieba
import sys
import os
import codecs

if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[input] [output]'
	exit()

fr = codecs.open(sys.argv[1], 'r', encoding='utf-8')
fw = codecs.open(sys.argv[2], 'w', encoding='utf-8')

index = 0
for line in fr:
	index += 1
	if index % 10000 == 0:
		sys.stderr.write('\rProcessing line %d' % index)
		sys.stderr.flush()
	seg_list = jieba.cut(line.strip())
	fw.write(' '.join(seg_list) + '\n')

sys.stderr.write('\nDone at %d \n' % index)

fr.close()
fw.close()

