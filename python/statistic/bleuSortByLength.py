import sys
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[input] [sent_bleu]'
	exit()

input_name = sys.argv[1]
bleu_name = sys.argv[2]

import codecs
input_file = codecs.open(input_name, 'r', encoding='utf-8')
bleu_file = codecs.open(bleu_name, 'r', encoding='utf-8')

file_list = [input_file, bleu_file]

static_dict = {}
for line, bleu in zip(input_file, bleu_file):
	line = line.strip()
	bleu = float(bleu.strip())
	length = len(line.split(' '))
	static_dict[length] = static_dict.get(length, []) + [bleu]

curLine = 0
for k, v in static_dict.items():
	while curLine + 1 < k:
		curLine += 1
		#print curLine, 0
		print 0
	curLine = k
	#print k, sum(v)/len(v)
	print sum(v)/len(v)

for f in file_list:
	f.close()
