# encoding: utf-8
import sys
if len(sys.argv) != 5:
	print 'Usage: python', sys.argv[0], '[lang1] [lang2] [delta] [output]'
	exit()

lang1_name = sys.argv[1]
lang2_name = sys.argv[2]
delta = int(sys.argv[3])
output_name = sys.argv[4]

import codecs

lang1_file = codecs.open(lang1_name, 'r', encoding='utf-8')
lang2_file = codecs.open(lang2_name, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')

file_list = [lang1_file, lang2_file, output_file]

import datetime
import time

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

#	for ele in result:
#		oprint('\t'.join([str(ele['start_time']), str(ele['end_time']), ' '.join(ele['content'])]) + '\n')

	return result 

file1_content = parse_file(lang1_file)
file2_content = parse_file(lang2_file)

oprint('<html> <head> <meta charset="utf-8" /> <style> div{position:absolute} .left{left: 0px; background: #dadaff} .right{padding-left: 50%; background: #deffd6}</style> </head> <body>\n')
for ele in file2_content:
	oprint('<div class="right" style="top:'+str((ele['start_time']+delta) * 10)+'px; height:'+str((ele['end_time'] - ele['start_time'] + 1) * 5)+'px">' + ' ||| '.join(ele['content']) + '</div>' + '\n')
for ele in file1_content:
	oprint('<div class="left" style="top:'+str(ele['start_time'] * 10)+'px; height:'+str((ele['end_time'] - ele['start_time'] + 1) * 5)+'px">' + ' ||| '.join(ele['content']) + '</div>' + '\n')
oprint('</body> </html>\n')


for f in file_list:
	f.close()
