import sys
import os

if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[conll_file] [summary|detail]'
	print 'The statistic for conll file will print out on the screen.'
	exit()

# in-file setting
statistic_dict = {'Y':0, 'N':0}
seperator = '\t'
label_index = -1

# main
conll_name = sys.argv[1]
option = sys.argv[2]

conll_file = open(conll_name, 'r')

file_list = [conll_file]

token_num = 0
sentence_num = 1
statistic_result = []
for line in conll_file:
	line = line.strip()
	sep_line = line.split()

	if len(line) > 0: # not empty line
		label = sep_line[label_index]
		statistic_dict[label] = statistic_dict[label] + 1
		token_num += 1
	else: #empty line
		statistic_result.append([sentence_num, statistic_dict, token_num])
		sentence_num += 1
		statistic_dict = {'Y':0, 'N':0}
		token_num = 0 # reset token

# print for each line
if option == 'detail':
	for element in statistic_result:
		sentence_id = element[0]
		label_dict = element[1]
		sentence_token = float(element[2])
		print_layout = [	str(sentence_id), 
					'{0:.0f}'.format(sentence_token), 
					'{0:.2f}'.format(label_dict['Y']/sentence_token * 100) + '%', 
					'{0:.2f}'.format(label_dict['N']/sentence_token * 100) + '%']
		print "\t".join(print_layout)
else:

	# prepare summary statistic
	dict_Y = {'0':0, '1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0}
	dict_N = {'0':0, '1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0}
	for element in statistic_result:
		label_dict = element[1]
		sentence_token = float(element[2])
	
		rate_Y, rate_N = label_dict['Y']/sentence_token * 100, label_dict['N']/sentence_token * 100
		dict_Y[str(int(rate_Y/10))] += 1
		dict_N[str(int(rate_N/10))] += 1
	
	
	print 'Y label %:'
	for i in range(0, 10):
		number = dict_Y[str(i)] if i < 9 else dict_Y['9']+dict_Y['10']
		endRange = ')' if i < 9 else ']'
		print '[%d, %d%s: %d (%f %s)' % (i*10, (i+1)*10, endRange, number, number/float(sentence_num) * 100, '%')
	
	print 'N label %:'
	for i in range(0, 10):
		number = dict_N[str(i)] if i < 9 else dict_N['9']+dict_N['10']
		endRange = ')' if i < 9 else ']'
		print '[%d, %d%s: %d (%f %s)' % (i*10, (i+1)*10, endRange, number, number/float(sentence_num) * 100, '%')

for f in file_list:
	f.close()
