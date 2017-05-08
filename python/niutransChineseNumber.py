#-- encoding: utf-8 --#
import sys
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[input] [output]'
	exit()

debug = False

input_name = sys.argv[1]
output_name = sys.argv[2]

import codecs
input_file = codecs.open(input_name, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')
file_list = [input_file, output_file]

# not used, but it is powerful, may use later on
chs_arabic_map = {u'零':0, u'一':1, u'二':2, u'三':3, u'四':4,
        u'五':5, u'六':6, u'七':7, u'八':8, u'九':9,
        u'十':10, u'百':100, u'千':10 ** 3, u'万':10 ** 4,
        u'〇':0, u'壹':1, u'贰':2, u'叁':3, u'肆':4,
        u'伍':5, u'陆':6, u'柒':7, u'捌':8, u'玖':9,
        u'拾':10, u'佰':100, u'仟':10 ** 3, u'萬':10 ** 4,
        u'亿':10 ** 8, u'億':10 ** 8, u'幺': 1,
        u'０':0, u'１':1, u'２':2, u'３':3, u'４':4,
        u'５':5, u'６':6, u'７':7, u'８':8, u'９':9}

# not used, but it is powerful, may use later on
def convertChineseDigitsToArabic (chinese_digits, encoding="utf-8"):
    if isinstance (chinese_digits, str):
        chinese_digits = chinese_digits.decode (encoding)

    result  = 0
    tmp     = 0
    hnd_mln = 0
    for count in range(len(chinese_digits)):
        curr_char  = chinese_digits[count]
        curr_digit = chs_arabic_map.get(curr_char, None)
        # meet 「亿」 or 「億」
        if curr_digit == 10 ** 8:
            result  = result + tmp
            result  = result * curr_digit
            # get result before 「亿」 and store it into hnd_mln
            # reset `result`
            hnd_mln = hnd_mln * 10 ** 8 + result
            result  = 0
            tmp     = 0
        # meet 「万」 or 「萬」
        elif curr_digit == 10 ** 4:
            result = result + tmp
            result = result * curr_digit
            tmp    = 0
        # meet 「十」, 「百」, 「千」 or their traditional version
        elif curr_digit >= 10:
            tmp    = 1 if tmp == 0 else tmp
            result = result + curr_digit * tmp
            tmp    = 0
        # meet single digit
        elif curr_digit is not None:
            tmp = tmp * 10 + curr_digit
        else:
            return result
    result = result + tmp
    result = result + hnd_mln
    return result


def isFloat(element):
	try: 
		float(element)
		return True
	except:
		return False


def toNumber(g, encoding='utf-8'):
	sep_g = g.split(' ||| ')
	gen = sep_g[2] # target
	src = sep_g[4]
	sep_src = src.split(' ')
	if len(sep_src) > 1: # contain number and unit
		num = sep_src[0]
		unit = sep_src[1]
		if isFloat(num): # number part is float
			if unit == 'million': # process million
				result = float(num) * 100
				if result >= 10000:
					return '%g%s' % ((result / 10000), '亿')
				else:
					return '%g%s' % (result, '万')
			elif unit == 'billion': # process billion
				result = float(num) * 10
				return '%g%s' % (result, '亿')
			elif unit == 'trillion': # process tillion
				result = float(num)
				return '%g%s' % (result, '万亿')
			else: # unseen unit
				if debug: print 'unseen unit', g
				return sep_g[2]
		else: # number is not float
			if debug: print 'number is not float', g
			return sep_g[2]
	else: # cannot split
		if debug: print 'cannot split', g
		return sep_g[2]
		

	
#	print '%s\t%s' % (sep_g[2].encode('utf-8'), sep_g[4].encode('utf-8'))

	#print convertChineseDigitsToArabic(number) 

	#number.replace(u'万', 'w').replace(u'亿', 'i')
	#return ' ||| '.join([sep_g[0], sep_g[1], number, sep_g[3], sep_g[4]])
	

index = 0
for line in input_file:
	index += 1
	if index % 10000 == 0:
		sys.stderr.write('\rProcessing line %d' % index)
		sys.stderr.flush()
	
	# main
	line = line.strip()
	sep_line = line.split(' |||| ')
	if len(sep_line) > 1: # has generalization part
		sent = sep_line[0]
		gen = sep_line[1]

		sep_gen = gen[1:-1].split('}{')
		sep_sent = sent.split(' ')

		output_file.write(sent + ' |||| ')

		for g in sep_gen: # for each gen
			sep_g = g.split(' ||| ')
			if sep_g[2] == sep_g[4]: # if source and gen is equal, skip
				output_file.write('{' + g + '}')
				continue
			if sep_g[3][1:] == 'number': # if gen type is number, process
				result = toNumber(g) # get process result
				output_file.write('{' + ' ||| '.join(sep_g[:2]) + ' ||| ')
				if debug: print result
				try: # encoding problem, I don't know why, but it works, lol
					output_file.write('%s' % (result.decode('utf-8')))
				except:
					output_file.write('%s' % (result))
				output_file.write(' ||| ' + ' ||| '.join(sep_g[3:]) + '}')
			else:
				output_file.write('{' + g + '}')
		output_file.write('\n')
	else:
		output_file.write(line + '\n')

sys.stderr.write('\nDone\n')
sys.stderr.flush()

for f in file_list:
	f.close()
