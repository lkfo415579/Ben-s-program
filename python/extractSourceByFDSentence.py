import sys
import os
import codecs
import re

if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], '[source-sent] [target-sent] [force-decoding-sent]'
	exit()

source_name = sys.argv[1]
target_name = sys.argv[2]
fd_name = sys.argv[3]
out_s_name = fd_name+'.s'
out_t_name = fd_name+'.t'

source_file = codecs.open(source_name, 'r', encoding='UTF-8')
target_file = codecs.open(target_name, 'r', encoding='UTF-8')
fd_file = codecs.open(fd_name, 'r', encoding='UTF-8')
out_s_file = codecs.open(out_s_name, 'w', encoding='UTF-8')
out_t_file = codecs.open(out_t_name, 'w', encoding='UTF-8')


file_list = [source_file, target_file, fd_file, out_s_file, out_t_file]

#main
index = 0
for line in fd_file:
	index += 1
	if index % 100 == 0:
		sys.stdout.write(str(index)+'\r')
		sys.stdout.flush()

	fd_sent = re.sub(r' \|\d+-\d+\| ', ' ', line.strip().split('|||')[0]).strip()
	s_sent = source_file.readline().strip()
	t_sent = target_file.readline().strip()
#	print fd_sent, '|', t_sent, cmp(fd_sent, t_sent)
	while cmp(fd_sent, t_sent):
		s_sent = source_file.readline().strip()
		t_sent = target_file.readline().strip()

	out_s_file.write(s_sent+'\n')
	out_t_file.write(t_sent+'\n')

#close all file
for f in file_list:
	f.close()
