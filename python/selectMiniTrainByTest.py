import sys
if len(sys.argv) != 6:
	print 'Usage: python', sys.argv[0], '[train] [test*] [output] [word-count] [id/line]'
	exit()

# parameters distribute
train_name = sys.argv[1]
test_name = sys.argv[2]
output_name = sys.argv[3]
word_count = int(sys.argv[4])
option = sys.argv[5]

# open files
import codecs
train_file = codecs.open(train_name, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')
file_list = [train_file, output_file]

def readAllTestData(file_name_list):
	result = set()
	for name in file_name_list:
		f = codecs.open(name, 'r', encoding='utf-8')
		for line in f:
			for w in line.strip().split():
				result.add(w)
		f.close()
	return result

sys.stderr.write('Loading words from testing set: ')
test_set = set()
# read all target word, if name contain *, using glob to read all file
if test_name.count('*') > 0:
	import glob
	file_name_list = glob.glob(test_name)
	sys.stderr.write(' '.join(file_name_list) + ' ... ')
	test_set = readAllTestData(file_name_list)
# if name NOT contain *, read by normal way
else:
	test_file = codecs.open(test_name, 'r', encoding='utf-8')
	for line in test_file:
		for w in line.strip().split():
			test_set.add(w)
	test_file.close()
sys.stderr.write('done\n')

# store the test word selected count, each word -1
test_dict = {key:word_count for key in test_set}
result_set = set() # selected training set

# main selection
index = 0
for line in train_file:
	index += 1
	if index % 10000 == 0:
		sys.stderr.write('Parsing training data: %s line %d ... \r' % (train_name, index))
		sys.stderr.flush()

	add_this = False
	words = set(line.strip().split())
	for w in words:
		# when train sentence contain word that remain count > 0, add this sentence
		if test_dict.get(w, 0) > 0:
			add_this = True
			break
	if add_this:
		for w in words:
			if w in test_set:
				test_dict[w] -= 1
				if option == 'line': # add line
					result_set.add(line.strip())
				elif option == 'id': # add id
					result_set.add(index)
sys.stderr.write('done\n')

# map all id into string
if option == 'id':
	result_set = map(str, sorted(result_set))

sys.stderr.write('Exporting data into: %s ... ' % output_name)
for ele in result_set:
	output_file.write(ele + '\n')
sys.stderr.write('done\n')

sys.stderr.write('Exporting OOVs into: %s ... ' % (output_name + '.oov'))
debug = codecs.open(output_name+'.oov', 'w', encoding='utf-8')
for k, v in test_dict.items():
	if v == word_count:
		debug.write(k + '\n')
debug.close()
sys.stderr.write('done\n')

for f in file_list:
	f.close()
