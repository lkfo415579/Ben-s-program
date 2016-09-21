import os
import sys
import optparse
import datetime
import codecs

if len(sys.argv) == 1:
	print 'Some arguments missing, please use --help to check.'
	exit()

def countFileLine(fileName):
	print 'Counting file total line number...'
	fr = codecs.open(fileName, 'r', encoding='utf-8')
	index = 0
	for line in fr:
		index += 1
	fr.close()
	return index

def main():
	parser = optparse.OptionParser('Usage %prog --s <source_file> --t <target_file> [--ms <source_tree_file> --mt <target_tree_file>] --o <output_suffix>')
	
	parser.add_option('--s', dest='source', type='string', help='The file of the source sentence')
	parser.add_option('--t', dest='target', type='string', help='The file of the target sentence')
	parser.add_option('--ms', dest='source_tree', type='string', help='The file of the source tree')
	parser.add_option('--mt', dest='target_tree', type='string', help='The file of the target tree')
	parser.add_option('--o', dest='suffix', type='string', help='The suffix for the output file')
	parser.add_option('--num', dest='num', type='string', help='The extract line number')

	(options, args) = parser.parse_args()
	source = str(options.source)
	target = str(options.target)
	source_tree = str(options.source_tree)
	target_tree = str(options.target_tree)
	suffix = str(options.suffix)
	num = str(options.num)

	flag_source = not (source == 'None')
	flag_target = not (target == 'None')
	flag_source_tree = not (source_tree == 'None')
	flag_target_tree = not (target_tree == 'None')
	flag_suffix = not (suffix == 'None')
	flag_num = not (num == 'None')

	if not flag_source and not flag_target and not flag_source_tree and not flag_target_tree:
		print 'Some arguments missing, please use --help to check.'	
		return

	if not flag_suffix:
		suffix = 'output_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

	if not flag_num:
		num = '1000'

	totalLines = countFileLine(source)
	print 'Total lines number:', totalLines
	test_no = int(num)
	cut_index = float(totalLines) / float(test_no)
	cut_index = cut_index
	print 'Extract lines between', cut_index

	file_list = []
	if flag_source:
		fr_source = codecs.open(source, 'r', encoding='utf-8')
		fw_source = codecs.open(source+'.'+suffix, 'w', encoding='utf-8')
		fw_test_source = codecs.open('test_source.'+suffix, 'w', encoding='utf-8')
		file_list = file_list + [fr_source, fw_source, fw_test_source]

	if flag_target:
		fr_target = codecs.open(target, 'r', encoding='utf-8')
		fw_target = codecs.open(target+'.'+suffix, 'w', encoding='utf-8')
		fw_test_target = codecs.open('test_target.'+suffix, 'w', encoding='utf-8')
		file_list = file_list + [fr_target, fw_target, fw_test_target]

	if flag_source_tree:
		fr_source_tree = codecs.open(source_tree, 'r', encoding='utf-8')
		fw_source_tree = codecs.open(source_tree+'.'+suffix, 'w', encoding='utf-8')
		fw_test_source_tree = codecs.open('test_source_tree.'+suffix, 'w', encoding='utf-8')
		file_list = file_list + [fr_source_tree, fw_source_tree, fw_test_source_tree]

	if flag_target_tree:
		fr_target_tree = codecs.open(target_tree, 'r', encoding='utf-8')
		fw_target_tree = codecs.open(target_tree+'.'+suffix, 'w', encoding='utf-8')
		fw_test_target_tree = codecs.open('test_target_tree.'+suffix, 'w', encoding='utf-8')
		file_list = file_list + [fr_target_tree, fw_target_tree, fw_test_target_tree]

	index = 0
	sum_cut = cut_index
	extractLineNo = 0
	while True:
		line_source = fr_source.readline() if flag_source else ' '
		line_target = fr_target.readline() if flag_target else ' '
		line_source_tree = fr_source_tree.readline() if flag_source_tree else ' '
		line_target_tree = fr_target_tree.readline() if flag_target_tree else ' '

		if index % 10000 == 0:
			sys.stdout.write('Current line: %d, Extracted line: %d\r' % (index, extractLineNo))
			sys.stdout.flush()

		if not line_source or not line_target or not line_source_tree or not line_target_tree:
			break

		index += 1
		if index == int(sum_cut) and extractLineNo < test_no:
			extractLineNo += 1
			sum_cut += cut_index
			if flag_source:
				fw_test_source.write(line_source)
			if flag_target:
				fw_test_target.write(line_target)
			if flag_source_tree:
				fw_test_source_tree.write(line_source_tree)
			if flag_target_tree:
				fw_test_target_tree.write(line_target_tree)
		else:
			if flag_source:
				fw_source.write(line_source)
			if flag_target:
				fw_target.write(line_target)
			if flag_source_tree:
				fw_source_tree.write(line_source_tree)
			if flag_target_tree:
				fw_target_tree.write(line_target_tree)
					
	for f in file_list:
		f.close()

if __name__ == '__main__':
	main()
