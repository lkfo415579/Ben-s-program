import sys
import os
import codecs
import re

if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[input_file] [output_file]'
	exit()

input_name = sys.argv[1]
output_name = sys.argv[2]

input_file = codecs.open(input_name, 'r', 'utf-8')
output_file = codecs.open(output_name, 'w', 'utf-8')

file_list = [input_file, output_file]

def substitute(tree_str, sent_head, node_list):
	combine_nodes = ''
	for head, word in reversed(node_list):
		'''
			analyze_head = re.findall('(\d+)\.\.(\d+)', head)[0]
				if len(analyze_head) > 0:
					(start, end) = analyze_head
					if int(start) == int(end):
						combine_nodes += word + ' '
					else:
						combine_nodes += '[' + word + ' ' + head + '] '
				else:
		'''
		combine_nodes += '(' + word + ' _' + head + '_)'
	tree_str = tree_str.replace(sent_head, combine_nodes)
	return tree_str

def normalize(tree_str):
	return re.sub(r'\(([^ ]*) _\d+\.\.\d+_\)', r'(W \1)', tree_str)

tree_str = ''
index = 0
for line in input_file:
	line = line.strip()
	(sent_id, sent_head) = re.findall('^Trans Opt (\d+) \[(\d+\.\.\d+)\]', line)[0]
	node_list = re.findall('\[(\d+\.\.\d+)\]=(.*?)  ', line)
	
	sent_head = '_' + sent_head + '_'
	
	if index != int(sent_id):
		output_file.write(normalize(tree_str) + '\n')
		index = int(sent_id)
		tree_str = ''
	
	if len(tree_str) == 0:
		tree_str = '(S ' + sent_head + ')'
	
	tree_str = substitute(tree_str, sent_head, node_list)

if len(tree_str) > 0:
	output_file.write(normalize(tree_str) + '\n')

for f in file_list:
	f.close()
