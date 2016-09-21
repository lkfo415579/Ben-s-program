import sys
import os

if len(sys.argv) != 5:
	print '''--Help message--
Please use the following command to run this program: (for more information, check readme file)'''
	print '$ python', sys.argv[0], 'input-rule-table input-lexical output-name source-kenlm\n'
	exit()

def runcommand(cmdlist):
	cmdStr = ' '.join(cmdlist)
	print 'Running:', cmdStr
	os.system(cmdStr)
	print 'Command', cmdStr, 'finish!'

# program files
reorderName = 'reorderRuleTable.py'
replaceName = 'replaceRuleTable.py'
uniqueName = 'uniqRule.py'

# argv
inputName = sys.argv[1]
lexical_model = sys.argv[2]
outputName = sys.argv[3]
source_klm = sys.argv[4]

# reorder
cmd = ['python', reorderName, inputName, lexical_model, outputName, source_klm]
runcommand(cmd)
os.system('date') # print time
runcommand(['rm', outputName+'.reorder.m'])

# replace
inputName = outputName + '.reorder'

cmd = ['python', replaceName, inputName, outputName]
runcommand(cmd)
os.system('date') # print time
runcommand(['rm', outputName+'.reorder', outputName+'.html'])

# sort
cmd = ['cat', outputName+'.replace', '|', 'sort >', outputName+'.sort']
runcommand(cmd)
runcommand(['rm', outputName+'.replace'])

# unique
inputName = outputName + '.sort'

cmd = ['python', uniqueName, inputName, outputName]
runcommand(cmd)
os.system('date') # print time
runcommand(['rm', outputName+'.sort'])
