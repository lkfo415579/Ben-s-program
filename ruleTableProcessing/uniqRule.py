# this program will generate 1 output file
import os # for running the linux command
import sys

# help message
if len(sys.argv) != 3:
	print '''
--Help message--
This program will generate 1 output file
1. output-name.uni - unique rule-table file: remove all rule that contain some source and target\n
You should use the following command to run this program:'''
	print '$ python', sys.argv[0],'sorted-rule-table output-name\n'
	exit()

# open file
fr = open(sys.argv[1],'r') # read the sort file as input
fw = open(sys.argv[2]+'.uni','w')

# the rule table format:
# source_sentence ||| target_sentence ||| pr0 pr1 pr2 pr3 2.718 ||| alignment ||| c0 c1 c2
prevs = ['',''] # s,t sentence
prevpr = [0.0,0.0,0.0,0.0] # probability
prevc = [0.0,0.0,0.0] # frequency
preva = '' # alignment
repeatNum = 1 # sum the repeat times
totalCount = 0
totalUniq = 0
totalRepeat = 0
for line in fr:
	totalCount += 1
	if totalCount % 100000 == 0:
		print totalCount
	
	seplll = line.split(' ||| ')
	seplll[4] = seplll[4].replace(' |||','')

	if (totalCount == 1): # init the varible to avoid writting emptry rule into result file
		prevs = seplll[0:2]
		prevpr = map(float, seplll[2].split(' ')) # take the first four probabilities
		prevc = map(float, seplll[4].split(' ')) # take the count
		preva = seplll[3] # save alignment >>> note: it save the first alignment now, it may need to update in the future
		continue # skip the following process		

	# if it is unqiue rule that difference from the previous one
	if (prevs[0] != seplll[0] or prevs[1] != seplll[1]):
		# save the previous record
#		prevprLine = ' '.join(str(e/float(repeatNum)) for e in prevpr) # change list to string
#		prevcLine = ' '.join(str(int(e/repeatNum) if e/repeatNum > 1 else 1) for e in prevc) # change list to string, fix all count with minimum 1
		#prevpr = [float(prevc[2])/prevc[0], 1.0, float(prevc[2])/prevc[1], 1.0, 2.718] # recalculate the pr
		prevpr = [float(prevc[2])/prevc[0], 1.0, float(prevc[2])/prevc[1], 1.0] # recalculate the pr
		prevprLine = ' '.join(str(e) for e in prevpr) # change list to string
		prevcLine = ' '.join(str(e) for e in prevc) # change list to string

		fw.write(' ||| '.join([prevs[0], prevs[1], prevprLine, preva, prevcLine])+' |||\n')
		#fw.write(prevs[0] + ' ||| ' + prevs[1] + ' ||| ' + prevprLine + ' ||| ' + preva + ' ||| ' + prevcLine +'\n')
		totalRepeat += 1 if repeatNum != 1 else 0
		# reset the previous record
		prevs = seplll[0:2]
		prevpr = map(float, seplll[2].split(' ')) # take the first four probabilities
		prevc = map(float, seplll[4].split(' ')) # take the count
		preva = seplll[3] # save alignment >>> note: it save the first alignment now, it may need to update in the future
		repeatNum = 1 # reset to 1
		totalUniq += 1
	else: # repeat found
		pr = map(float, seplll[2].split(' ')) # map the list into float
		c = map(float, seplll[4].split(' ')) # map the list into float
		prevpr = [x+y for x,y in zip(prevpr, pr)] # add two list
		prevc = [x+y for x,y in zip(prevc, c)] # add two list
		repeatNum += 1

print '\nTotal parse: ', totalCount, '	( 100 % )'
print 'Unique: ', totalUniq, '		(',totalUniq*100.0/totalCount,'% )'
print 'Repeat: ', totalRepeat, '		(', totalRepeat*100.0/totalCount, '% )'
fr.close()
fw.close()
