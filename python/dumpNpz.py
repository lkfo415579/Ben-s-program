import sys

if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[input-npz] [output-dict]'
	exit()

import numpy
import json

input_name = sys.argv[1]
output_name = sys.argv[2]

npz_model = numpy.load(input_name)

import codecs
output_file = codecs.open(output_name, 'w', encoding='utf-8')

for l,v in npz_model.items():
	s_key = 'Unknown'
	s_size = 'Unknown'
	s_value = 'Unknown'
	try:
		s_key = str(l)
	except:
		print 'error: ', l
	try:
		s_size = str(len(v))
	except:
		print 'error: ', l
		
	try:
		s_value = str(v) 
	except:
		print 'error: ', l
		

	output_file.write('key='+s_key+';size='+s_size+';value='+s_value+'\n')
output_file.close()
