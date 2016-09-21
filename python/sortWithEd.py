import os

fr = open('nbfile.uni','r')
fw = open('nbfile.ed.sort','w')

for line in fr:
	seplll = line.split(' ||| ')
	seplll[0], seplll[-1] = seplll[-1].strip(), seplll[0]
	fw.write(' ||| '.join(seplll) + '\n')
	
fr.close()
fw.close()
