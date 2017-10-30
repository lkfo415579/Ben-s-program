import sys
if len(sys.argv) != 2:
	print 'Usage: python', sys.argv[0], '[movie_info]'
	exit()

input_name = sys.argv[1]

import codecs
input_file = codecs.open(input_name, 'r', encoding='utf-8')

info_dict = {}
index = 0
for line in input_file:
	index += 1
	if index % 1000 == 0:
		sys.stderr.write('\r%d' % index)
		sys.stderr.flush()

	line = line.strip()
	try:
		lang, imdb, id, userrank, dc, totalDisk, disk = line.split('\t')
		if lang in ['chi', 'por']:
			info_dict[imdb] = info_dict.get(imdb, []) + [{'lang':lang, 'imdb':imdb, 'id':id, 'userrank':userrank, 'dc':dc, 'totalDisk':totalDisk, 'disk':disk}]
	except:
		print line

print
selected_imdb = ''
while True:
	selected_imdb = raw_input('select imdb:')
	for movie in info_dict[selected_imdb]:
		print movie
print 'Bye'
