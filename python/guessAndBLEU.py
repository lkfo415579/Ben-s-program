import sys
import os
import time

if len(sys.argv) != 5:
	print '$ python', sys.argv[0], 'translate_method path input true'
	exit()

if sys.argv[1] != 'ss' and sys.argv[1] != 'tt':
	print 'translate_method only support ss and tt'
	exit()

translate_method = sys.argv[1]
path = sys.argv[2]
inputFile = sys.argv[3]
true = sys.argv[4]

start = time.time()

print 'Start translating'
if translate_method == 'ss':
	cmd = ['/smt/mosesdecoder/bin/moses', '-f', path+'model/moses.ini', '<', inputFile, '>', path+'guess']
	os.system(' '.join(cmd))
elif translate_method == 'tt':
	cmd = ['/smt/mosesdecoder/bin/moses_chart', '-f', path+'model/moses.ini', '<', inputFile, '>', path+'guess']
	os.system(' '.join(cmd))
print 'End translating'

'''
print 'Start scoring'
cmd = ['/smt/mosesdecoder/scripts/generic/multi-bleu.perl', path + true, '<', path+'guess']
os.system(' '.join(cmd))

print 'End scoring'
print 'Whole process used', time.time() - start, 'seconds.'
'''

	
