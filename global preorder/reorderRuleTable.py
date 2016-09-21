# coding=utf-8

def main():
	import sys # argv
	import kenlm # for sentence scoring 
	from readLexicalModelIntoDict import readLex

	# help message
	if len(sys.argv) != 5:
		print '''
	--Help message--
	This program will generate 2 output files
	1. output-name.reorder - the reordered rule-table: all words are reordered by the alignment
		Example:
			input: 0-1 1-0 1-2 1-3 1-5 3-2 4-4
			reorder as: 0-1 1-2 2-2 3-2 4-4\n
	2. output-name.reorder.m - the middle process detail file: including source rule, skip alignment, alignment grouping, final alignment
		Example:
			那些 [IP][VP] 的 人 [NP] ||| the people who [IP][VP] [NP] ||| 0.384615 0.00209331 0.0579154 0.00180345 2.718 ||| 0-0 0-2 1-3 2-0 3-1 ||| 0.325 2.15832 0.125
			[[0, [0, 2]], [1, [3]], [2, [0]], [3, [1]]]
			[[0, 0], [1, 3], [2, 0], [3, 1]]
			0-0 1-3 2-0 3-1\n
	You should use the following command to run this program:
	$ python '''+sys.argv[0]+' input-rule-table input-lexical-name output-name source-kenlm\n'
		exit()

	# open file
	fr_rt = open(sys.argv[1],'r') # for rule-table
	lexical_file = sys.argv[2]
	fw_m = open(sys.argv[3]+'.reorder.m','w') # for writing the result
	fw_out = open(sys.argv[3]+'.reorder','w') # for writing the result

	# read kenlm
	model = kenlm.LanguageModel(sys.argv[4])
	
	# read lexical model
	my_lex_dict = readLex(lexical_file)

	totalCount = 0
	print 'Parsing is started (reorder rule table)'
	for line in fr_rt: # each line in input file
		totalCount += 1
		if totalCount % 10000 == 0:
			sys.stdout.write(str(totalCount)+'\r')
			sys.stdout.flush()
		
		seplll = line.split(' ||| ')
		sep3 = seplll[3].split(' ') # alignment

		# insert X into the alignment of one rule
		left = 0
		alignmentArray = [] # result
		for align in sep3: # each alignment 0-1
			subAlign = align.split('-') # extract 0 1
			if int(subAlign[0]) > left: # if skip appear
				while True: # forever loop
					alignmentArray.append([left, ['X']]) # insert X
					left += 1
					if int(subAlign[0]) == left: # repeat until no skip again
						alignmentArray.append([int(subAlign[0]), [int(subAlign[1])]])
						left += 1
						break; # break forever loop
			elif int(subAlign[0]) == left: # equal, append new list [1, [0]]
				alignmentArray.append([int(subAlign[0]), [int(subAlign[1])]])
				left += 1
			elif int(subAlign[0]) < left: # repeat index, append into sublist of result [1, [0,2]]
				alignmentArray[left-1][1].append(int(subAlign[1]))
		# insert X in the tail
		sourceLength = len(seplll[0].split(' ')) - 1
		if (left < sourceLength):
			for i in range(left, sourceLength):
				alignmentArray.append([i, ['X']])
		# print line, str(alignmentArray)

		# write into file
		resultStr = str(alignmentArray)
		skipResultStr = selectAlign(seplll[0], seplll[1], alignmentArray, my_lex_dict)
		reformAlignStr = reformAlign(seplll[0], skipResultStr, model)
		fw_m.write(line + '	' + resultStr + '\n	' + str(skipResultStr)  + '\n	' + reformAlignStr + '\n')
		
		reformAlignedRuleTable = ''
		for i in range(0, len(seplll)):
			if i == 3:
				reformAlignedRuleTable = reformAlignedRuleTable + reformAlignStr + ' ||| '
			elif i == len(seplll) - 1:
				reformAlignedRuleTable = reformAlignedRuleTable + str(seplll[i])
			else: 
				reformAlignedRuleTable = reformAlignedRuleTable + str(seplll[i]) + ' ||| ' 
		fw_out.write(reformAlignedRuleTable)
		#print str(totalCount) + '\n' + line + '	' + resultStr + '\n	' + str(skipResultStr)  + '\n	' + reformAlignStr + '\n'
		#fw_out.write(str(selectAlign(alignmentArray)))	
				
	print '\nParsing is finished (reorder rule table)'
	#normalCount = totalCount - skipCount
	print '\nTotal parse: ', totalCount, '	( 100% )'

	# close file
	fr_rt.close()
	fw_m.close()
	fw_out.close()

# find the non X alignment, such as 1-0 1-X 2-X 3-X 3-7, it will return 7 
def nonX(i, l):
	if i < len(l)-1:
		if l[i+1][1] != 'X':
			return i
		else:
			return nonX(i+1, l)
	else:
		return i

# given source sentence, start X pos and end X pos, return better alignment
def find2gram(wordStr, start, end, model):
	wordList = wordStr.split(' ')
	if len(wordList) >= 3:
		left = [start - 1, -100.0] # default to min
		right = [end + 1, -100.0] # default to min
		if start == 0: # first word of sentence
			return end + 1 # next word
		elif end == len(wordList) - 2: # last word of sentence
			return start - 1 # previous word
		else:
			left[1] =  model.score(wordList[left[0]] + ' ' + wordList[start])
			right[1] = model.score(wordList[end] + ' ' + wordList[right[0]])
#		print left[1], right[1] # left left and right
		return left[0] if left[1] > right[1] else right[0] #return max log10(pr) index
	return 0 # default return 0

# rerange the alignment from list to str, [[0,'X'], [1,1], [2,2]] to 0-1 1-1 2-0
def reformAlign(wordStr, lists, model):
	wordList = wordStr.split(' ')
	output = '' # reform result
	reformed = 0 # mark the alignment is processed or not

	for i in range(0, len(lists)):
		if i < reformed:
			continue
		if lists[i][1] == 'X':
			nonXPos = nonX(i, lists)
			# return the better alignment for X
			rs = lists[find2gram(wordStr, i, nonXPos, model)][1]
			
			# replace all X to rs if X are continous, such as 1-X 2-X 3-X
			for j in range(i, nonXPos+1):
				output += str(lists[j][0]) + '-' + str(rs) + ' '
			reformed = nonXPos + 1
		else:
			output += str(lists[i][0]) + '-' + str(lists[i][1]) + ' '
	return output.strip() # trim string

# find the pr in lex model
def bi_contains(lst, item):
	""" efficient `item in lst` for sorted lists """
	# if item is larger than the last its not in the list, but the bisect would 
	# find `len(lst)` as the index to insert, so check that first. Else, if the 
	# item is in the list then it has to be at index bisect_left(lst, item)
	return (item <= lst[-1]) and (lst[bisect_left(lst, item)] == item)

# select Alignment from [2, [2,3,4,6,7]] to [2,3]
# my_dict is the dictionary, such my_dict['ola']=[['hello', '0.88'], ['goodbye', '0.0001']]
def selectAlign(source, target, lists, my_dict):
	sep_source = source.split(' ') # split sentences
	sep_target = target.split(' ')
	for ele in lists: # all alignment group [[0, [0,1,2]], [1, [2]], [2, [2,3,4,6,7]]
		if len(ele[1]) > 1: # in case, only 0, 2 satisfy
			candidate_list = []
			try:
				candidate_list = my_dict[sep_source[ele[0]]] # get item from lexical model
			except:
				print 'failed to found candidate since "',sep_source[ele[0]],'" in', source
				candidate_list = []
			# prepare target words list
			target_words = [] 
			for i in ele[1]:
				target_words.append([sep_target[i], i])
			# use target words list to select useful candidates, change format to [align, prob]
			second_candidate_list = []
			for cand in candidate_list:
				for x in target_words:
					if x[0] == cand[0]:
						second_candidate_list.append([x[1], cand[1]])
			# if contains candidate, select alignment by the maximum prob
			if len(second_candidate_list) > 0:
				current = second_candidate_list[0]
				for item in second_candidate_list:
                			if float(item[1]) > float(current[1]):
                       				 current[0], current[1] = item[0], item[1]
				ele[1] = current[0]	
			# if no candidate can be selected by lexical model, use old method
			else:
				i = ele[1][0] # try to match the e
				subsum = 0 # calculate mean
				count = 0 # count the distance of continuous number
				maxCount = 0 # maximum distance
				preSelect = i # default choice is first element
				for e in ele[1]: # go thought all elements
					if i == e: # match
						subsum += e
						count += 1 # distance + 1
					elif i < e: # unmatch: it should summary the result
						if count > maxCount: # the longest continuous number
                                                	preSelect = subsum/count # mean
                                                	maxCount = count # mark maximum count
						subsum = e # reset the sum
						count = 1 # reset count
						i = e # reset i
					i += 1 # try to match next one
                	        if count > maxCount: # the last summary
        	                        preSelect = subsum/count # mean
	                        ele[1] = preSelect # replace original list as summary number

		else: # in case, only 1 satisfy
			ele[1] = ele[1][0] # directly replace list as number
	return lists
	
''' before 2015-06-08: old selection method -> base on maximum group center
	for ele in lists: # all alignment
		if len(ele[1]) > 1: # second list contain 2 elements or more
			i = ele[1][0] # try to match the e
			subsum = 0 # calculate mean
			count = 0 # count the distance of continuous number
			maxCount = 0 # maximum distance
			preSelect = i # default choice is first element
			for e in ele[1]: # go thought all elements
				if i == e: # match
					subsum += e
					count += 1 # distance + 1
				elif i < e: # unmatch: it should summary the result
					if count > maxCount: # the longest continuous number
						preSelect = subsum/count # mean
						maxCount = count # mark maximum count
					subsum = e # reset the sum
					count = 1 # reset count
					i = e # reset i
				i += 1 # try to match next one
			if count > maxCount: # the last summary
				preSelect = subsum/count # mean
			ele[1] = preSelect # replace original list as summary number
		else: # second list contain only one number
			ele[1] = ele[1][0] # directly replace list as number
	return lists # return the processed list					
'''
if __name__ == '__main__':
	main()

