import sys
if len(sys.argv) != 2:
	print 'Usage: python', sys.argv[0], '[folder_name]'
	exit(0)

from os import listdir
from os.path import isdir as isdir
folder_name = sys.argv[1]
if not isdir(folder_name):
	print folder_name, 'is not folder, skip'
	exit()
file_name_list = [f for f in listdir(folder_name) if isdir(folder_name)]

chi_file_name = [folder_name + '/' + file_name for file_name in file_name_list
	if file_name[:3] == 'chi' and 'out' in file_name]

por_file_name = [folder_name + '/' + file_name for file_name in file_name_list
	if file_name[:3] == 'por' and 'out' in file_name]

from filecmp import cmp
def getRemoveSet(com_file_name_list):
	remove_set = set()
	for n1 in com_file_name_list:
		if n1 in remove_set:
			continue
		for n2 in com_file_name_list:
			if n1 == n2:
				continue
			else:
				isequal = cmp(n1, n2)
				if isequal:
					remove_set.add(n2)
	return remove_set	

chi_remove_set = getRemoveSet(chi_file_name)
por_remove_set = getRemoveSet(por_file_name)

from os import remove
for name in list(chi_remove_set) + list(por_remove_set):
	remove(name)
