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

def to_string(value):
	result = "Unknown"
	try:
		result = str(value)
	except:
		print 'error while conventing to string: ', value
		exit()
	
	return result

def expend_list(input, o, level=0):
	if isinstance(input, list) and len(input) > 0 and isinstance(input[0], list): # if input is not a 1d-list
		for ele in input:
#			expend_list(ele, o, level + 1)
#	else:
			if len(ele) > 0:
				o.write(('\t' * level) + str(len(ele)) + '\n')
				break
		#for ele in input:
		#	o.write(('\t' * level) + str(ele) + '\n')

def expend_dict(input, o, level=0):
	for l,v in input.items():
		print 'Processing key:', l, 'type:', type(v)
		s_key = to_string(l)
		s_size = 'Unknown'
		if type(v) == type(numpy.array([0])): # if that is the numpy array, convert into normal array
			v = v.tolist()
			if type(v) == type(1): # int type
				s_size = '1'
			else:
				s_size = to_string(len(v))
		elif type(v) == type(1): # int type
			s_size = '1'
		else:
			s_size = to_string(len(v))
			
		#try:
		#	s_size = to_string(len(v))
		#except:
		#	print 'for this key:', s_key
		#	print 'what wrong of the type? ' + str(type(v))
		try:
			if type(v) == type({}): # if v type is dict
				o.write(('\t' * level) + 'key=' + s_key + ';type=dict' + ';size=' + s_size + '\n')
				expend_dict(v, o, level + 1)
			elif type(v) == type([]): # if v type is list
				o.write(('\t' * level) + 'key=' + s_key + ';type=list' + ';size=' + s_size + '\n')
				expend_list(v, o, level + 1)
			else:
				o.write(('\t' * level) + 'key=' + s_key + ';type=others' + ';size=' + s_size + '\n')
				o.write(('\t' * level) + to_string(v) + '\n')
				
		except Exception as e:
			print 'having this error:', e
			print 'error on this key:', s_key
			print 'the value is type:', type(v)
			exit()
			print 'error while expending dictonary: ', v
			exit()

	

#expend_dict(npz_model, sys.stdout, 0)
expend_dict(npz_model, output_file, 0)

output_file.close()
