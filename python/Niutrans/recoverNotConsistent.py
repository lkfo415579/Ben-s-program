import sys
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[source] [target]'
	exit()

source_name = sys.argv[1]
target_name = sys.argv[2]

output_source_name = source_name + '.con'
output_target_name = target_name + '.con'

import codecs
source_file = codecs.open(source_name, 'r', encoding='utf-8')
target_file = codecs.open(target_name, 'r', encoding='utf-8')
output_source_file = codecs.open(output_source_name, 'w', encoding='utf-8')
output_target_file = codecs.open(output_target_name, 'w', encoding='utf-8')

file_list = [source_file, target_file, output_source_file, output_target_file]

def countGen(gen):
	result = {}
	gen_sep = gen.split('}{')
	gen_sep[0] = gen_sep[0][1:]
	gen_sep[-1] = gen_sep[-1][:-1]
	for ele in gen_sep:
		ele_sep = ele.split(' ||| ')
		gen_symbol = ele_sep[3]
		result[gen_symbol] = result.get(gen_symbol, 0) + 1
	return result

def recover(sent, gen):
	sent_sep = sent.split(' ')
	gen_sep = gen.split('}{')
	gen_sep[0] = gen_sep[0][1:]
	gen_sep[-1] = gen_sep[-1][:-1]
	for ele in gen_sep:
		ele_sep = ele.split(' ||| ')
		sent_sep[int(ele_sep[0])] = ele_sep[-1]
	return ' '.join(sent_sep) 
	
index = 0
keepCount = 0
recoverCount = 0
while True:
	source_line = source_file.readline()
	target_line = target_file.readline()

	if not source_line and not target_line:
		sys.stderr.write('Finish!\n')
		sys.stderr.write('Total line %d, keep:%d, recover:%d\n' % (index, keepCount, recoverCount))
		sys.stderr.flush()
		break
	elif not source_line or not target_line:
		sys.stderr.write('Early finish! reason: unbalance lines\n')
		sys.stderr.write('Total line %d, keep:%d, recover:%d\n' % (index, keepCount, recoverCount))
		sys.stderr.flush()
		break

	index += 1
	if index % 100 == 0:
		sys.stderr.write('\rParsing line %d, keep:%d, recover:%d' % (index, keepCount, recoverCount))
		sys.stderr.flush()

	source_line = source_line.strip()
	target_line = target_line.strip()

	source_line_sep = source_line.split(' |||| ')
	target_line_sep = target_line.split(' |||| ')

	# check gen part if it contains gen
	if len(source_line_sep) > 1 or len(target_line_sep) > 1:
		# get dict of gen symbol
		source_count = countGen(source_line_sep[1]) 
		target_count = countGen(target_line_sep[1])
		if source_count == target_count:
			keepCount += 1
			output_source_file.write(source_line + '\n')
			output_target_file.write(target_line + '\n')
		else:
			recoverCount += 1
			output_source_file.write(recover(source_line_sep[0], source_line_sep[1]) + '\n')
			output_target_file.write(recover(target_line_sep[0], target_line_sep[1]) + '\n')
	# direct output if it not contains gen
	else:
		keepCount += 1
		output_source_file.write(source_line_sep[0] + '\n')
		output_target_file.write(target_line_sep[0] + '\n')

for f in file_list:
	f.close()
