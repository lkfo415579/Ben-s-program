# encoding: utf-8
import sys
from operator import itemgetter
import re
import codecs

# input gen: {id ||| id ||| tran ||| label ||| source}{...}
def gen_to_list(gen):
	result = []
	if len(gen) > 0:
		gen = gen[1:-1] # remove begin and end
		gens = gen.split('}{')
		for g in gens:
			g_sep = g.split(' ||| ')
			id, tran, label, source = int(g_sep[0]), g_sep[2], g_sep[3], g_sep[4]
			result.append([id, tran, label, source])
	return result
	
def read_dict(file_name, lang):
	f = codecs.open(file_name, 'r', encoding='utf-8')
	result = {}
	for line in f:
		s, t = '', ''
		if lang == 'zh':
			t, s = line.strip().split('\t')
		else:
			s, t = line.strip().split('\t')
		#if lang == 'zh':
		#	result[s.lower()] = [[s, t]]
		#	result[t] = [[t, s]]

		# when it is pt, read the line and store in special structure
		# for example: s=ben ao, t=BEN ==> {'ben':['ben ao','BEN']}
		#elif lang == 'pt':
		#	w = s.split(' ')[0].lower()

		w = s.split(' ')[0]
		tmp = result.get(w, [])
		tmp.append([s,t])
		result[w] = tmp
	f.close()
	return result

def doReplace(s_line, name_dict, label):
	s_sent, s_gen = '', ''
	if s_line.find(' |||| ') >= 0:
		s_sent, s_gen = s_line.split(' |||| ')
	else:
		s_sent = s_line

	s_gen_list = gen_to_list(s_gen)

	pre_space = 0
	s_words = s_sent.split(' ')
	for si in range(len(s_words)):
		sw = s_words[si]
		# get name translation, if not exist, get next word
		#name_tran = name_dict.get(sw.lower(), [])
		name_tran = name_dict.get(sw, [])
		if len(name_tran) == 0:
			continue
		
		for candidate in name_tran:
			#wid = s_sent.find(candidate[0].lower())
			wid = s_sent.find(candidate[0])
			eid = wid + len(candidate[0])

			#if wid >= 0 and (wid + len(candidate[0]) == ' ' or wid + len(candidate[0]) - 1 == len(s_sent)):
			if wid >= 0:
				wid_char, eid_char = '', ''
				if wid == 0:
					wid_char = ' '
				elif wid > 0:
					wid_char = s_sent[wid-1]

				if eid == len(s_sent):
					eid_char = ' '
				else:
					eid_char = s_sent[eid]
					
	#			print wid_char, eid_char		

				if wid_char == ' ' and eid_char == ' ':
	#				print s_sent[wid-1], s_sent[eid]
	#				print 'get it', s_sent[wid:wid+len(candidate[0])]
					s_index = s_sent[:wid].count(' ') # target word in the sentence index
					s_word_space = candidate[0].count(' ')
					pre_space += s_word_space
	#				print s_word_space, pre_space
					s_gen_list = [[i-s_word_space, t, l, s] if i > s_index else [i, t, l, s] for [i, t, l, s] in s_gen_list]
					s_gen_list.append([s_index, candidate[1], label, candidate[0]])
					s_sent = s_sent[:wid] + label + s_sent[eid:]

	# sort by index
	s_gen_list = sorted(s_gen_list, key=itemgetter(0))

	# duplicate id
	s_gen_list = [[i, i, t, l, s] for [i, t, l, s] in s_gen_list]

	# change to niutrans format
	#print s_gen_list
	#print t_gen_list
	s_gen = '}{'.join([' ||| '.join([str(ele[0]), str(ele[1]), ele[2], ele[3], ele[4]]) for ele in s_gen_list])
	return ''.join([s_sent, (' |||| {' + s_gen + '}') if len(s_gen) > 0 else ''])
	
def main():
	input_name, name_name, source_output_name, lang, label = sys.argv[1:]
	
	input_file = codecs.open(input_name, 'r', encoding='utf-8')
	output_file = codecs.open(source_output_name, 'w', encoding='utf-8')
	
	file_list = [input_file, output_file]
	
	print 'load name pair into dictionary'
	name_dict = read_dict(name_name, lang)
	
	print 'main scan'
	index = 0
	while True:
		index += 1
		if index % 1000 == 0:
			sys.stderr.write('\r%d' % index)
			sys.stderr.flush()
		
		s_line = input_file.readline()
		if not s_line:
			break
	
		s_line = s_line.strip()
		result = doReplace(s_line, name_dict, '$'+label)
		output_file.write(result + '\n')
	
	for f in file_list:
		f.close()

if __name__ == '__main__':
	if len(sys.argv) != 6:
		print 'Usage: python', sys.argv[0], '[input] [name_pair] [output] [lang:zh/pt] [label]'
		exit()
	main()
