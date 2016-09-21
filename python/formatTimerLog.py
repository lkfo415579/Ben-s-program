import sys
import os
import re

def main():
	if len(sys.argv) != 3:
		print 'Usage: python', sys.argv[0], 'input_log output_csv'
		exit()

	input_log_file = sys.argv[1]
	output_csv_file = sys.argv[2]

	fr_log = open(input_log_file, 'r')
	fw_csv = open(output_csv_file, 'w')

	format_dict = {}
	format_dict['running_date'] = []
	key_set = set()

	# parse all result into dict
	for line in fr_log:
		if not line[0].isdigit(): # first character is not digit, is date
			format_dict['running_date'].append(line.strip()) #append
		else: # first character is digit
			line_no, file_name = line.strip().split(' ')
			if file_name in key_set:
				format_dict[file_name].append(line_no) #append
			else:
				format_dict[file_name] = [line_no] #init
				key_set.add(file_name)
			
	# write file from dict
	key_list = sorted(key_set)
	for i in range(0, len(format_dict['running_date'])): # for each time
		if i == 0: # write header
			fw_csv.write('running_date,'+','.join(key_list)+'\n')
		tmp_list = [format_dict['running_date'][i]] # that time
		for key in key_list:
			tmp_list.append(format_dict[key][i]) # all file lines
		fw_csv.write(','.join(tmp_list)+'\n')

	fr_log.close()
	fw_csv.close()

if __name__ == '__main__':
	main()
