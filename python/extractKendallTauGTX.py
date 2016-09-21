import sys
from optparse import OptionParser

parser = OptionParser()

inputFile = ""
outputFile = ""
kendallTau = ""
number = 0

parser.add_option("-i", "--input", default="", dest="inputFile",
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

fr_input = open(inputFile)
fr_kendall = open(kendallTau)
fw_output = open(outputFile)

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

