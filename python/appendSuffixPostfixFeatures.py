#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import codecs

if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], 'input_word output_features'
	exit()

input_delimited = '\t'
input_name = sys.argv[1]
output_name = sys.argv[2]

input_file = codecs.open(input_name, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')

file_list = [input_file, output_file]

def createFeature(word):
	output = []
	suffix1 = word[:1]
	suffix2 = word[:2]
	suffix3 = word[:3]
	postfix1 = word[-1:]
	postfix2 = word[-2:]
	postfix3 = word[-3:]
	first_case = 'Y' if word[:1].isupper() else 'N'
	
	output = [suffix1, suffix2, suffix3, postfix1, postfix2, postfix3, first_case]
	return output


for line in input_file:
	line = line.strip()
	if len(line) == 0:
		output_file.write('\n')
		continue

	sep_line = line.split(input_delimited, 1)

	word = sep_line[0]
	other = sep_line[1] if len(sep_line) > 1 else ''

	feature_list = createFeature(word)

	result = [word] + feature_list + [other]

	output_file.write(input_delimited.join(result).strip()+'\n')

for f in file_list:
	f.close()
