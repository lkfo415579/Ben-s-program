import cPickle
import sys
import codecs
import numpy

if len(sys.argv) != 3:
    print 'Usage: python', sys.argv[0], '[input_file] [parse_file] [data_folder]'

unk_sym = 1
null_sym = 50000 
raise_unk = False

def parse_input(word2idx, idx2word, line):
    seqin = line.split()
    seqlen = len(seqin)
    seq = numpy.zeros(seqlen+1, dtype='int64')
    for idx,sx in enumerate(seqin):
        seq[idx] = word2idx.get(sx, unk_sym)
        if seq[idx] >= null_sym + 1:
            seq[idx] = unk_sym
        if seq[idx] == unk_sym and raise_unk:
            raise Exception("Unknown word {}".format(sx))

    seq[-1] = null_sym
    if idx2word:
        idx2word[null_sym] = '<eos>'
        idx2word[unk_sym] = 'UNK'
        parsed_in = [idx2word[sx] for sx in seq]
        return seq, " ".join(parsed_in[:-1])

    return seq, seqin

input_name = sys.argv[1]
output_name = sys.argv[2]
data_folder = sys.argv[3]

input_file = codecs.open(input_name, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')
file_list = [input_file, output_file]
# source
#word_indx_name = './train.source.wordid.pkl'
#indx_word_name = './train.source.idword.pkl'
# target
word_indx_name = data_folder + '/train.target.wordid.pkl'
indx_word_name = data_folder + '/train.target.idword.pkl'

word_indx = cPickle.load(open(word_indx_name,'rb'))
indx_word = cPickle.load(open(indx_word_name,'r'))

index = 0
for line in input_file:
    index += 1
    if index % 1000 == 0:
        sys.stderr.write('%d\r' % index)
        sys.stderr.flush()
    seq, parsed_in = parse_input(word_indx, indx_word, line.strip())
    output_file.write(parsed_in + '\n')

for f in file_list:
    f.close()
