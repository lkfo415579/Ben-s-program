import sys
import os
from optparse import OptionParser

def latexStart(lang):
		
	return r'''
	\documentclass{article}

	\usepackage{tikz}
	\usepackage{CJKutf8}
	\usepackage{forest}

	\newenvironment{bottompar}{\par\vspace*{\fill}}{\clearpage}

	\begin{document}
	\begin{CJK*}{UTF8}{'''+lang+r'''}
	\pagestyle{empty}
	'''

def latexEnd(lang):
	return r'''
	\end{CJK*}{UTF8}{'''+lang+r'''}
	% End of code
	\end{document}
	'''
	
def latexForestStart():
	return r'''
		\begin{tikzpicture}[shorten >=1pt,->,draw=black!50, node distance=0]
			\tikzstyle{every pin edge}=[<-,shorten <=1pt]
			\tikzstyle{neuron}=[circle,fill=black!2,minimum size=14pt,inner sep=0pt]
			\tikzstyle{input neuron}=[neuron, fill=green!50];
			\tikzstyle{output neuron}=[neuron, fill=red!50];
			\tikzstyle{hidden neuron}=[neuron, fill=blue!50];
	'''
	
def latexForestEnd():
	return r'''
		\end{tikzpicture}
	'''
	
def latexNewPage():
	return r'''
		\newpage
	'''

def latexElementAlignTree(element_set):
	return r'''
			\foreach \sa / \ta in {'''+element_set+r'''} {
				\path (I-\sa) edge (O-\ta);
			}
		'''
	
def latexElementTree(element_set, side):
	if side == 's':
		return r'''
			\foreach \s / \sw in {'''+element_set+r'''} {
				\node[input neuron, pin=left:\sw] (I-\s) at (0, -\s*0.5) {\scriptsize $s_{\s}$};
			}
		'''
	else:
		return r'''
			\foreach \t / \tw in {'''+element_set+r'''} {
				\node[output neuron,pin={[pin edge={->}]right:\tw}, right of=O-\t] (O-\t) at (4, -\t*0.5) {\scriptsize $t_{\t}$};
			}
		'''

def latexNodeSet(line, mode):
	output_list = []
	if mode:
		line = '<s> ' + line + ' </s>'
	sep_l = line.replace('&', '\&').split(' ')
	for i in range(len(sep_l)):
		output_list.append('/'.join([str(i), '\\textit{'+sep_l[i]+'}']))
		
	return ', '.join(output_list)

# given the trimmed source, target, alignment sentence for generating the latex element set
def latexElementAlignSet(align):
	sep_a = align.split(' ')
	output_list = []
		
	for element in sep_a:
		sep_element = element.split('-')
		source_id = sep_element[0]
		target_id = sep_element[1]
		output_list.append('/'.join([
			source_id, 
			target_id]))

	return ', '.join(output_list)

def main():
	parser = OptionParser()
	parser.add_option("-s", "--source", dest="source_file", help="The file contain source language sentence(s).")
	parser.add_option("-t", "--target", dest="target_file", help="The file contain target language sentence(s).")
	parser.add_option("-a", "--alignment", dest="align_file", help="The alignment file for the source and target.")
	parser.add_option("-o", "--output", dest="output_file", help="The output file with the whole latex syntax.")
	parser.add_option("-l", "--language", action="store_true", dest="lang", default=False, help="<default zh_sim> The default is Simplify Chinese; Enable this flag for using Traditional Chinese.")
	parser.add_option("-m", "--mode", action="store_true", dest="mode", default=False, help="<default no_tag> The default is no starting tag(<s>) and ending tag(</s>); Enable this flag for using the starting tag and ending tag. Depend on your alignment file.")
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="<default no_message> Enable this flag to show the current processing line. ")

	(options, args) = parser.parse_args()
	
	if not options.source_file or not options.target_file or not options.align_file:
		print "Some options missing, please check the options."
		parser.print_help()
		exit()
	
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

	fr_s = open(source_file, 'r')
	fr_t = open(target_file, 'r')
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
			
		element_align_set = latexElementAlignSet(line_a)
		source_element_set = latexNodeSet(line_s, mode)
		target_element_set = latexNodeSet(line_t, mode)
		
		fw_o.write(latexForestStart())
		fw_o.write(latexElementTree(source_element_set, 's'))
		fw_o.write(latexElementTree(target_element_set, 't'))
		fw_o.write(latexElementAlignTree(element_align_set))
		fw_o.write(latexForestEnd())
		fw_o.write(latexNewPage())
	
	fw_o.write(latexEnd(lang_code))

	fr_s.close()
	fr_t.close()
	fr_a.close() 
	fw_o.close()

if __name__ == '__main__':
	main()