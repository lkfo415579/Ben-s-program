# encoding: utf-8

def oprint(string):
	output_file.write(string)

def parse_time(s):
	x = time.strptime(s.split(',')[0],'%H:%M:%S')
	return datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()

def parse_file(f):
	delta = 0
	tmp_object = {'start_time':0, 'end_time':0, 'content': []}
	result = []
	while True:
		line = f.readline()
	
		if not line:
			break
		
		line = line.strip()
		if line == '':
			result.append(tmp_object)
			delta = 0
			tmp_object = {'start_time':0, 'end_time':0, 'content': []}
		else:
			delta += 1
			if delta == 1: # id
				continue
			elif delta == 2: # time
				sep_line = line.split(' --> ')
				start_time, end_time = parse_time(sep_line[0]), parse_time(sep_line[1])
				tmp_object['start_time'] = int(start_time)
				tmp_object['end_time'] = int(end_time)
			elif delta >= 3 and len(line) != 0: # content
				tmp_object['content'].append(line)
			else:
				continue

	return result 

if __name__ == '__main__':
	import sys
	import codecs
	import datetime
	import time
	if len(sys.argv) != 4:
		print 'Usage: python', sys.argv[0], '[input] [output-type] [output]'
		exit()
	
	input_name = sys.argv[1]
	output_type = sys.argv[2]
	output_name = sys.argv[3]
	
	input_file = codecs.open(input_name, 'r', encoding='utf-8')
	
	file_list = [input_file]
	
	
	if output_type == 'json':
		file_content = parse_file(input_file)
		with codecs.open(output_name, 'w', encoding='utf-8') as output_file:
			json.dump(file_content, output_file, indent=2)
	elif output_type == 'line':
		success = True
		output_file = codecs.open(output_name, 'w', encoding='utf-8')
		try:
			file_content = parse_file(input_file)
			for ele in file_content:
				output_file.write(' |||| '.join([str(ele["start_time"]), str(ele["end_time"]), ' ##newline## '.join(ele["content"])]) + '\n')
		except:
			sys.stderr.write('skip ' + input_name + '\n')
			success = False
		output_file.close()

		if not success:
			from os import remove
			remove(output_name)

	for f in file_list:
		f.close()
