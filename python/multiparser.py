import os
import sys
import thread
import threading
import time

path = '/home/mb45450/program/s2t_parser/BerkeleyParser/'

if len(sys.argv) != 5:
	print '$ python', sys.argv[0], 'input sep_no language output'
	sys.exit()
timestart = time.time()

class myThread (threading.Thread):
    def __init__(self, a, b, c):
        threading.Thread.__init__(self)
        self.a = a
        self.b = b
        self.c = c
    def run(self):
        print "Starting " #+ self.name
        # Get lock to synchronize threads
#        threadLock.acquire()
        parseTreeBerkeley(self.a, self.b, self.c)
        # Free lock to release next thread
#        threadLock.release()

def getFileLength(filename):
	tmp = open(filename, 'r')
	count = 0
	while tmp.readline():
		count += 1	
	tmp.close()
	return count

def parseTreeBerkeley(inputName, language, outputName):	
	parser = path+'BerkeleyParser-1.7.jar'
	if language == 'en':
		cmd = 'java -Dfile.encoding=UTF-8 -jar '+parser+' -gr eng_sm6.gr < '+inputName+' > '+outputName+'.tmp'
	elif language == 'cn':
		cmd = 'java -Dfile.encoding=UTF-8 -jar '+parser+' -gr chn_sm5.gr < '+inputName+' > '+outputName+'.tmp'
	elif language == 'de':
		cmd = 'java -Dfile.encoding=UTF-8 -jar '+parser+' -gr ger_sm5.gr < '+inputName+' > '+outputName+'.tmp'
	elif language == 'fr':
		cmd = 'java -Dfile.encoding=UTF-8 -jar '+parser+' -gr fra_sm5.gr < '+inputName+' > '+outputName+'.tmp'
	else:
		print 'not support this language:', language
		exit()

	print 'Running: $ '+cmd
	os.system(cmd)
	os.system('date')
	print 'End of ' +cmd


def parseToMosesForm(outputName):
	cmd = '/smt/mosesdecoder/scripts/training/wrappers/berkeleyparsed2mosesxml.perl < '+outputName+'.tmp > '+outputName
	print 'Running: $ '+cmd
	os.system(cmd)

	print 'Removing '+outputName+'.tmp'
	os.system('rm '+outputName+'.tmp')

#	cmd = ['python', path + 's2t.py', inputName, language, outputName]
#	print ' '.join(cmd)
#	os.system(' '.join(cmd))

inputFile = sys.argv[1]
sepno = int(sys.argv[2])
language = sys.argv[3]
outputFile = sys.argv[4]
fileLength = getFileLength(inputFile)
sepsize = fileLength / sepno + 1

sepInputList = []
sepOutputList = []
threadLock = threading.Lock()
threads = []
for i in range(0, sepno):
	sepInputList.append(inputFile+'.'+str(i))
	sepOutputList.append(outputFile+'.'+str(i))
	cmd = ['head', '-'+str(sepsize), inputFile, '>', sepInputList[i], '&&' , 'sed', '-i', '"1,+'+str(sepsize-1)+'d"', inputFile]
	print ' '.join(cmd)
	os.system(' '.join(cmd))

	t = myThread(sepInputList[i], language, sepOutputList[i])
	t.start()
	threads.append(t)

for t in threads:
	t.join()

#for o in sepOutputList:
#	parseToMosesForm(o)

cmd = ['cat', outputFile+'.* > ', outputFile]
print ' '.join(cmd)
os.system(' '.join(cmd))

cmd = ['rm', outputFile+'.*', inputFile+'*']
print ' '.join(cmd)
os.system(' '.join(cmd))

print "Exit in", time.time() - timestart
'''
	try:
		thread.start_new_thread(parseTreeBerkeley, (sepInputList[i], language, sepOutputList[i],))
	except:
		print 'Error: unable to start thread'
'''
#	pool.apply_async(func = parseTreeBerkeley, args = (sepInputList[i], language, sepOutputList[i]))










