# encoding: utf-8
import sys
if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], '[input_source] [input_target] [output_name]'
	exit(1)

import math
from codecs import open

input_1 = sys.argv[1]
input_2 = sys.argv[2]
output_name = sys.argv[3]

def readDataToList(fileName):
	f = open(fileName, 'r', encoding='utf-8')
	result = []
	for line in f.readlines():
		result.append(line.strip())
	f.close()
	return result

def buildTfIdf(s1, s2):
#	wordCount = 0
	tfCount = dict()
	idfCount = dict()
	sContain = dict()

	wordSet = set()
	sys.stderr.write('Building tf-idf ...\n')
	index = 0
	for i in range(len(s2)):
		index += 1
		if index % 1000 == 0:
			sys.stderr.write('\rLine: %d, tfCount: %d, idfCount: %d' % (index, len(tfCount), len(idfCount)))
			sys.stderr.flush()
	
		line = s2[i].split(' ')
	
		#tf counting
#		for word in line:
#			tfCount[word] = tfCount.get(word, 0) + 1
#			wordCount = wordCount + 1
	
		#idf counting
		line = set(line) #filter repeated word
		for word in line:
			idfCount[word] = idfCount[word] + 1 if idfCount.has_key(word) else 1
#			if(idfCount.has_key(word)):
#				idfCount[word] = idfCount[word] + 1
#			else:
#				idfCount[word] = 1
			if(not sContain.has_key(word)):
				sContain[word] = set()
			sContain[word].add(i)

	sys.stderr.write('\rdone\n')	
	
	return tfCount, idfCount, sContain
	

#read data
sys.stderr.write('Reading source data ...\n')
s1 = readDataToList(input_1)

sys.stderr.write('Reading target data ...\n')
s2 = readDataToList(input_2)


# collect idf data of language 2 (English)
tfCount, idfCount, sContain = buildTfIdf(s1, s2)

#print sContain
#for key, value in sContain.items():
#	print key, value

#from random import shuffle
#for key, value in sContain.items():
#	if len(value) > 200:
#		tmp = list(value)
#		shuffle(tmp)
#		sContain[key] = tmp[:200]

sys.stderr.write('Main processing ...\n')
sCount = len(s2)
data1 = []
data2 = []
keywordList = []
index = 0
for i in range(len(s2)):
	index += 1
	if index % 1000 == 0:
		sys.stderr.write('\rLine %d' % (index))
		sys.stderr.flush()

	line = s2[i].split(' ')
	idfScore = []

	#calcate idf score
	for word in line:
#		tf = float(tfCount[word]) / float(wordCount)
		idf = math.log(float(sCount) / float(idfCount.get(word, 0) + 1), 2)
		idfScore.append(idf)

#	print ' '.join(line), ' '.join(map(str, [idfCount.get(w, -1) for w in line]))
	sortedWord = list(zip(*sorted(zip(idfScore, line)))[1])
#	print ' '.join(sortedWord), ' '.join(map(str, [idfCount.get(w, -1) for w in sortedWord]))
	
	#only one sentence contains keyword
	while len(sContain.get(sortedWord[-1], set())) <= 1:
		sortedWord.remove(sortedWord[-1])

	keyword = sortedWord[-1]
	cand = sContain.get(keyword, [])

	sortedWord.remove(sortedWord[-1])
	while (len(cand) > 200 or len(cand) < 20) and len(sortedWord) > 0 :
		if len(cand) > 200:
			cand = set(cand) & set(sContain.get(keyword, cand))
		elif len(cand) < 20:
			cand = set(cand) | set(sContain.get(keyword, cand))
		sortedWord.remove(sortedWord[-1])
       
	if len(cand) > 200:
		cand = list(cand)[:200]

#	print len(cand)
	topCoverage = 0
	topCoverageLine = 0
	found = False
	for n in cand:
#	for n in sContain.get(keyword, []):
		if i == n:# or line == ' '.join(s2[n]): 
			continue # skip true answer
		coverage = float(len(set(line) & set(s2[n].split(' ')))) / float(len(line))
		if 0.9 > coverage > topCoverage and 1.3 > float(len(s2[n].split(' ')))/len(line) > 0.7:
			topCoverage = coverage
			topCoverageLine = n
			found = True
	
	if found:
		data1.append(i)
		data2.append(topCoverageLine)
		keywordList.append(keyword)


sys.stderr.write('\rdone\nExporting result ...\n')
output_file = open(output_name, 'w', encoding='utf-8')
for i in range(len(data1)):
	output_file.write(' ||| '.join([keywordList[i], s1[data1[i]], s1[data2[i]], s2[data1[i]], s2[data2[i]]]) + '\n')

output_file.close()
