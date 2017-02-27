import sys
if len(sys.argv) != 5:
	print 'Usage: python', sys.argv[0], '[input] [tmp_folder] [top-k] [phrase-length]'
	exit()

import codecs
input_name = sys.argv[1]
dir_name = sys.argv[2]
if dir_name[-1] != '/':
	dir_name += '/'
output = dir_name + 'phrase-table'
topk = int(sys.argv[3])
phraseLen = int(sys.argv[4])

import os
os.system('mkdir -p ' + dir_name)

input_file = codecs.open(input_name, 'r', encoding='utf-8')
output_file = codecs.open(output, 'w', encoding='utf-8')

file_list = [input_file, output_file]

def export_to_file(l, f, t):
	if len(l) == 0: return 0
	l = sorted(l, key=lambda x: x[0], reverse=True)[:t]
	for e in l:
		f.write(e[1] + '\n')
	return 1
	

# read content into dict
old_source= ''
line_list = []
index = 0
extracted = 0
for line in input_file:
	index += 1
	if extracted % 10000 == 0:
		sys.stderr.write('\rReading phrase table: %d, extracted: %d' % (index, extracted))
		sys.stderr.flush()

	line = line.strip()
	sep = line.split(' ||| ')

	# filter - phrase length
	if len(sep[0].split()) > phraseLen or len(sep[1].split()) > phraseLen:
		continue

	source = sep[0]
	if old_source != source:
		extracted += export_to_file(line_list, output_file, topk)
		line_list = []
		old_source = source

	count_part = sep[4]
	source = sep[0]
	together_count = float(sep[4].split()[2])
	line_list.append([together_count, line])

print '\nGenerating done at %d' % index

for f in file_list:
	f.close()
