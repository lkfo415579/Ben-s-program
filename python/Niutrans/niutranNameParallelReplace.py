import sys
if len(sys.argv) != 6:
	print 'Usage: python', sys.argv[0], '[input_source] [input_target] [name_pair] [output_source] [output_target]'
	print 'This program suggest chinese as source, other language as target.'
	exit()

import codecs
from operator import itemgetter
source_name, target_name, name_name, source_output_name, target_output_name = sys.argv[1:]

source_file = codecs.open(source_name, 'r', encoding='utf-8')
target_file = codecs.open(target_name, 'r', encoding='utf-8')
name_file = codecs.open(name_name, 'r', encoding='utf-8')
source_output_file = codecs.open(source_output_name, 'w', encoding='utf-8')
target_output_file = codecs.open(target_output_name, 'w', encoding='utf-8')

file_list = [source_file, target_file, name_file, source_output_file, target_output_file]

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


	

# load name pair into dictionary
name_dict = {}
for line in name_file:
	s, t = line.strip().split('\t')
	name_dict[s.lower()] = t

# main scan
while True:
	s_line = source_file.readline()
	t_line = target_file.readline()
	if not s_line or not t_line:
		break

	# if no contain person label, scan next line
	if s_line.count('$person') == 0 or s_line.count(' |||| ') == 0:
		continue
	# else, analyze person translation
	else:
		s_line = s_line.strip()
		t_line = t_line.strip()
		s_sent, s_gen = s_line.split(' |||| ')
		t_sent, t_gen = '', ''
		t_sep = t_line.split(' |||| ')
		if len(t_sep) > 1:
			t_sent, t_gen = t_sep[0], t_sep[1]
		else:
			t_sent, t_gen = t_sep[0], ''

		s_gen_list = gen_to_list(s_gen)
		t_gen_list = gen_to_list(t_gen)

		s_words = s_sent.split(' ')
		for si in range(len(s_words)):
			sw = s_words[si]
			# get name translation, if not exist, get next word
			name_tran = name_dict.get(sw.lower(), '')
			if len(name_tran) == 0:
				continue

			t_start = t_line.find(name_tran.lower())
			if t_start > 0: # target sentence contain translation
				# ---- target sentence -----
				t_end = t_start + len(name_tran)
#				print '|{}|{}|{}|{}|'.format(t_start, t_end, sw, name_tran)

				# replace phrase to label
				t_index = t_sent[:t_start].count(' ') # target word in the sentence index
				t_word = t_sent[t_start:t_end] # target word
				t_word_space = t_word.count(' ') # count space in word

#				print '|{}|{}|'.format(t_word, t_word_space)
				t_sent = t_sent[:t_start] + '$person' + t_sent[t_end:]

				t_gen_list = [[i-t_word_space, t, l, s] if i > t_index else [i, t, l, s] for [i, t, l, s] in t_gen_list]
				t_gen_list.append([t_index, sw, '$person', t_word])

				# ---- source sentence ----
				s_tmp = s_sent.split(' ')
				s_tmp[si] = '$person'
				s_gen_list.append([si, t_word, '$person', sw])
				s_sent = ' '.join(s_tmp)


		# sort by index
		s_gen_list = sorted(s_gen_list, key=itemgetter(0))
		t_gen_list = sorted(t_gen_list, key=itemgetter(0))

		# duplicate id
		s_gen_list = [[i, i, t, l, s] for [i, t, l, s] in s_gen_list]
		t_gen_list = [[i, i, t, l, s] for [i, t, l, s] in t_gen_list]

		# change to niutrans format
		s_gen = '}{'.join([' ||| '.join(map(str, ele)) for ele in s_gen_list])
		t_gen = '}{'.join([' ||| '.join(map(str, ele)) for ele in t_gen_list])
		source_output_file.write(''.join([s_sent, (' |||| {' + s_gen + '}') if len(s_gen) > 0 else '', '\n']))
		target_output_file.write(''.join([t_sent, (' |||| {' + t_gen + '}') if len(t_gen) > 0 else '', '\n']))

for f in file_list:
	f.close()
