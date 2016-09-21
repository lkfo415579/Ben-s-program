# Replace the rule table from source to target according to alignment
# Input:  rule-table
# Output: result, result.html
import sys
from operator import itemgetter # sorting by item id

# help message
if len(sys.argv) != 3:
	print '''
--Help message--
This program will generate 2 output files
1. output-name.replace - the replaced rule table
2. output-name.html - the html file for the replaced rule table: the replacement highlight by red color\n
You should use the following command to run this program:'''
	print '$ python',sys.argv[0],'input-rule-table output-result\n'
	exit()
# open file
f = open(sys.argv[1],'r')
fw = open(sys.argv[2]+'.replace','w')
fwHtml = open(sys.argv[2]+'.html','w')

def realignRule(sp, tp):
	align = []
	collect = []
	for i in range(0, len(sp)-1):
		for a,b in enumerate(tp):
			if (b == sp[i] and not (a in collect)):
				collect.append(a)
				align.append([i, a])
				break
	sorted(align)
	alignStr = ''
	for ele in align:
		alignStr += str(ele[0]) + '-' + str(ele[1]) + ' '
	return alignStr.strip()

# html header including td style
fwHtml.write('<head>\n<meta charset="UTF-8">\n<style>\ntd{ width: 25%; }\n</style>\n</head>\n\n<table style="width: 100%"><tbody>\n<tr><td>source</td><td>target</td><td>alignment</td><td>result</td></tr>\n')
totalCount = 0
print 'Replacement started:'
for line in f: #each rule
	totalCount += 1
	if totalCount % 100000 == 0:
		print totalCount

	seplll = line.split(" ||| ")
	#!!print len(seplll) # = 6
	sep0 = seplll[0].replace('\"', '&quot;').split(' ') # source
	sep1 = seplll[1].split(' ') # target
	sep3 = seplll[3].split(' ') # alignment
	#!!for ele in sep0: print ele+'_'	# ok

	#!!orderedList = [None] * len(sep1) # create empty array
#	orderedList = list(sep1) # copy list for output only
#	writeHtmlList = list(sep1) # copy list for html format
	#!!for ele in orderedList: print ele+' ', #copy success

	# sort alignment
	sep3.append(str(len(sep0)-1) + '-' + str(len(sep1)-1)) # add parent node alignment
#	print str(sep3)	
	alignList = list(sep3)
	for i in range(0, len(alignList)):
		alignList[i] = map(int, alignList[i].split('-'))
	alignList = sorted(alignList, key=itemgetter(1))
#	print str(alignList) # sort success

	orderedList = list(sep0)
	writeHtmlList = list(sep0)
	for i in range(0, len(alignList)):
		if i == len(alignList)-1:
			orderedList[i] = sep1[int(alignList[i][1])]
			writeHtmlList[i] = '<span style="color:red;" title="'+sep0[int(alignList[i][0])]+' -> '+sep1[int(alignList[i][1])]+' ('+str(alignList[i][0])+'-'+str(alignList[i][1])+')">'+sep1[int(alignList[i][1])]+'</span>' # replace word
		else:	
			orderedList[i] = sep0[int(alignList[i][0])]
			if sep0[i] == sep0[int(alignList[i][0])]:
				writeHtmlList[i] = sep0[i]
			else:
				writeHtmlList[i] = '<span style="color:red;" title="'+sep0[i]+' -> '+sep0[int(alignList[i][0])]+' ('+str(alignList[i][0])+'-'+str(alignList[i][1])+')">'+sep0[int(alignList[i][0])]+'</span>' # replace word
		
	# html formating
	writeHtmlLine = '<tr>\n<td>'+seplll[0]+'</td>\n<td>'+seplll[1]+'</td>\n<td>'+seplll[3]+'</td>\n<td>'
	writeHtmlLine += ' '.join(writeHtmlList)
	writeHtmlLine += '</td>\n</tr>\n'	

	# normal output
	writeLine = ' '.join(orderedList)
	seplll[3] = realignRule(sep0, orderedList) # reorder alignment 
	seplll[1] = writeLine
	writeLine = ' ||| '.join(seplll) 
	
	# write into normal file
	fw.write(writeLine.replace('&quot;', '\"'))
	fwHtml.write(writeHtmlLine)

fwHtml.write('</tbody></table>\n')
print '\nReplacement finished'

f.close()
fw.close()
fwHtml.close()
