# encoding: utf-8
import sys
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[input] [output]'
	exit()

import codecs
input_name = sys.argv[1]
output_name = sys.argv[2]

input_file = codecs.open(input_name, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')

file_list = [input_file, output_file]


import pickle
import nltk
#import tagger
print 'load tagger'
tagger = pickle.load(open("model/tagger.pkl"))
print 'done'

print 'load tokenizer'
portuguese_sent_tokenizer = nltk.data.load("tokenizers/punkt/portuguese.pickle")
print 'done'

print 'tagging'
index = 0
for line in input_file:
	index += 1
	if index % 1000 == 0:
		sys.stderr.write('\rline {}'.format(index))
		sys.stderr.flush()
	line = line.strip()
	#sent_tok = portuguese_sent_tokenizer.tokenize(line)
	sent_tok = [line]
	for s in sent_tok:
		#words = nltk.word_tokenize(s)
		words = s.split(' ')
		'''split_clitic = []
		for w in words:
			if w.count('-') > 0 and len(w) > 1:
				w_sep = w.split('-')
				split_clitic.append(w_sep[0])
				split_clitic.append('-' + w_sep[1])
			else:
				split_clitic.append(w)
		'''
		tags = [t for (w, t) in tagger.tag(words)]
		words_sent = ' '.join(words)
		tags_sent = ' '.join(tags)
		output_file.write(words_sent + '\n' + tags_sent + '\n')
print 'done'

for f in file_list:
	f.close()
