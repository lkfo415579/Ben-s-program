import sys
import os
import re
from optparse import OptionParser

def latexStart(lang):
		
	return r'''
	\documentclass{article}

	\usepackage{tikz}
	\usepackage{tikz-qtree}
	\usepackage{CJKutf8}
	\usepackage{forest}

	\newenvironment{bottompar}{\par\vspace*{\fill}}{\clearpage}

	\begin{document}
	\begin{CJK*}{UTF8}{'''+lang+r'''}
	\pagestyle{empty}
	'''

def latexEnd(lang):
	return r'''
	\end{CJK*}
	% End of code
	\end{document}
	'''
	

def latexNewPage():
	return r'''
	\newpage
	'''

def deepLevel(line):
	level, maxLevel = 0, 0
	for c in line:
		if c == '[':
			level += 1
		elif c == ']':
			level -= 1
		if level > maxLevel:
			maxLevel = level
	return maxLevel

def formatTree(line, side, fontsize, height, y_shift):
	output_list = []
	line = line.replace('&', '\&')
	line = line.replace('$', '\$')
	line = line.replace('%', '\%')
	symbol = ''
	sep_l = line.split(' ')
	if side == 's':
		output_list.append(r'''
	\begin{scope}[frontier/.style={distance from root='''+height+r'''pt}] 
		\Tree ''')
		symbol = 'e'
	else:
		output_list.append(r'''
	\begin{scope}[yshift=-'''+y_shift+r'''pt,grow'=up, frontier/.style={distance from root='''+height+r'''pt}] 
		\Tree ''')
		symbol = 'f'
	
	sep_space = line.split(' ')
	
	for i in range(1,len(sep_space)):
		tmp = sep_space[i]
		tmp = tmp.replace(']', '};]', 1)
		tmp = '\\node(%s%d){\\%s ' % (symbol, i, fontsize) + tmp
		sep_space[i] = tmp
	
	output_list.append('\t\t'+' '.join(sep_space).replace('[.', ' [.\\%s ' % fontsize))
	output_list.append(r'''
	\end{scope}
	''')

	return '\n'.join(output_list)

def formatAlign(align):
	sep_a = align.split(' ')
	output_list = []
		
	output_list.append(r'''\begin{scope}[dotted]''')
	for element in sep_a:
		sep_element = element.split('-')
		source_id = sep_element[0]
		target_id = sep_element[1]
		output_list.append('\t\t\\draw (e%d)--(f%d) [out=south, in=north];' % (int(source_id)+1, int(target_id)+1))

	output_list.append(r'''\end{scope}
	''')
	return '\n'.join(output_list)
	
def writeTreeToTree(options):
	source_file = str(options.source_file)
	target_file = str(options.target_file)
	align_file = str(options.align_file)
	output_file = str(options.output_file)
	mode = options.mode
	lang = options.lang
	verbose = options.verbose
	
	lang_code = 'gbsn' #simplify chinese
	if lang == True:
		lang_code = 'bsmi' #traditional chinese
		
	source_file_pre = '.' + source_file + '.pre'
	target_file_pre = '.' + target_file + '.pre'
	
	os.system("sed -e 's/^(//g' -e 's/)$//g' -e 's/ *( */[./g' -e 's/ *) */]/g' "+source_file+' > '+source_file_pre)
	os.system("sed -e 's/^(//g' -e 's/)$//g' -e 's/ *( */[./g' -e 's/ *) */]/g' "+target_file+' > '+target_file_pre)

	fr_s = open(source_file_pre, 'r')
	fr_t = open(target_file_pre, 'r')
	fr_a = open(align_file, 'r')
	fw_o = open(output_file, 'w')
	
	fw_o.write(latexStart(lang_code))
	
	index = 0
	while True:
		line_s = fr_s.readline().strip()
		line_t = fr_t.readline().strip()
		line_a = fr_a.readline().strip()
		
		if not line_s or not line_t or not line_a:
			print 'Finish', index, 'sentences.'
			break
			
		index += 1
		
		if verbose:
			print '>>>Id:', index
			print '\t'+line_s
			print '\t'+line_t
			print '\t'+line_a
		
		source_height = deepLevel(line_s)*16
		target_height = deepLevel(line_t)*16
		y_shift = source_height + target_height + 70
		
		output_formated_source_tree = formatTree(line_s, 's', 'scriptsize', str(source_height), str(y_shift))
		output_formated_target_tree = formatTree(line_t, 't', 'scriptsize', str(target_height), str(y_shift))
		output_formated_alignment = formatAlign(line_a)
		
		fw_o.write(r'''
	\begin{center}
	\begin{tikzpicture} [level distance=0.55cm, inner sep=1pt]''')
	
		fw_o.write(output_formated_source_tree)
		fw_o.write(output_formated_target_tree)
		fw_o.write(output_formated_alignment)
		
		fw_o.write(r'''
	\end{tikzpicture}
	\end{center}''')
		
	#fw_o.write(latexNewPage())
	
	fw_o.write(latexEnd(lang_code))

	fr_s.close()
	fr_t.close()
	fr_a.close() 
	fw_o.close()
	
	os.system('rm '+source_file_pre)
	os.system('rm '+target_file_pre)
	
def writeSingleTree(options):
	source_file = str(options.source_file)
	output_file = str(options.output_file)
	mode = options.mode
	lang = options.lang
	verbose = options.verbose
	
	lang_code = 'gbsn' #simplify chinese
	if lang == True:
		lang_code = 'bsmi' #traditional chinese
		
	source_file_pre = '.' + source_file + '.pre'
	
	os.system("sed -e 's/^(//g' -e 's/)$//g' -e 's/ *( */[./g' -e 's/ *) */]/g' "+source_file+' > '+source_file_pre)

	fr_s = open(source_file_pre, 'r')
	fw_o = open(output_file, 'w')
	
	fw_o.write(latexStart(lang_code))
	
	index = 0
	while True:
		line_s = fr_s.readline().strip()
		
		if not line_s:
			print 'Finish', index, 'sentences.'
			break
			
		index += 1
		
		if verbose:
			print '>>>Id:', index
			print '\t'+line_s
		
		source_height = deepLevel(line_s)*16
		y_shift = source_height
		
		output_formated_source_tree = formatTree(line_s, 's', 'scriptsize', str(source_height), str(y_shift))
		
		fw_o.write(r'''
	\begin{center}
	\begin{tikzpicture} [level distance=0.55cm, inner sep=1pt]''')
	
		fw_o.write(output_formated_source_tree)
		
		fw_o.write(r'''
	\end{tikzpicture}
	\end{center}''')
		
	#fw_o.write(latexNewPage())
	
	fw_o.write(latexEnd(lang_code))

	fr_s.close()
	fw_o.close()
	
	os.system('rm '+source_file_pre)
	
def main():
	parser = OptionParser()
	parser.add_option("-s", "--source", dest="source_file", help="The file contain source parsed tree(s).")
	parser.add_option("-t", "--target", dest="target_file", help="The file contain target parsed tree(s). If not provide, generate source tree only.")
	parser.add_option("-a", "--alignment", dest="align_file", help="The alignment file for the source and target. If not provide, generate source tree only.")
	parser.add_option("-o", "--output", dest="output_file", default="_output", help="The output file with the whole latex syntax.")
	parser.add_option("-l", "--language", action="store_true", dest="lang", default=False, help="<default zh_sim> The default is Simplify Chinese; Enable this flag for using Traditional Chinese.")
	parser.add_option("-m", "--mode", action="store_true", dest="mode", default=False, help="<default no_tag> The default is no starting tag(<s>) and ending tag(</s>); Enable this flag for using the starting tag and ending tag. Depend on your alignment file.")
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="<default no_message> Enable this flag to show the current processing line. ")

	(options, args) = parser.parse_args()
	
	if not options.source_file:
		print "Some options missing, please check the options."
		parser.print_help()
		exit()
	if not options.target_file or not options.align_file:
		print "Draw source tree only..."
		writeSingleTree(options)
	else:
		writeTreeToTree(options)

if __name__ == '__main__':
	main()