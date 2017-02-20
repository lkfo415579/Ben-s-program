import sys
if len(sys.argv) != 5:
	print 'Usage: python', sys.argv[0], '[input] [score] [number] [output]'
	exit()
#from optparse import OptionParser

#parser = OptionParser()

inputFile = sys.argv[1]
kendallTau = sys.argv[2]
number = float(sys.argv[3])
outputFile = sys.argv[4]

'''parser.add_option("-i", "--input", default="", dest="inputFile",
		help="Input the file for extracting.")
parser.add_option("-t", "--tau", default="", dest="kendallTau",
		help="Input the kendall tau score file.")
parser.add_option("-n", "--number", type="float", default=0, dest="number",
		help="The number for extracting if kendall tau larger than this.")
parser.add_option("-o", "--output", dest="outputFile",
		help="Input the output file after extracted.")

(options, args) = parser.parse_args()

if not inputFile or not kendallTau or not number or not outputFile:
	print "Some options missing, please check the options."
	parser.print_help()
	exit()
'''
import codecs

fr_input = codecs.open(inputFile, 'r', encoding='utf-8')
fr_kendall = codecs.open(kendallTau, 'r', encoding='utf-8')
fw_output = codecs.open(outputFile, 'w', encoding='utf-8')

while (True):
	line_input = fr_input.readline()
	line_kendall = fr_kendall.readline()
	if not line_input or not line_kendall:
		break

	if float(line_kendall.strip()) > number:
		fw_output.write(line_input)	

fr_input.close()
fr_kendall.close()
fw_output.close()

