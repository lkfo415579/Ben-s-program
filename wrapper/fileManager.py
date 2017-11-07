import codecs

class FileManager():
	__name_list = []
	__file_list = []

	def __init__(self, *args):
		self.__name_list = []
		self.__file_list = []

	def openReadFile(self, name):
		f = codecs.open(name, 'r', encoding='utf-8')
		self.__name_list.append(name)
		self.__file_list.append(f)
		return f
	
	def openWriteFile(self, name):
		f = codecs.open(name, 'w', encoding='utf-8')
		self.__name_list.append(name)
		self.__file_list.append(f)
		return f

	def getFileList(self):
		return self.__file_list
	
	def closeAllFile(self):
		for f in self.__file_list:
			f.close()
		self.name_list = []
		self.file_list = []
	
	def closeFile(self, name):
		if name in self.name_list:
			index = self.name_list.index(name)
			if index >= 0:
				self.__file_list[index].close()
				self.__file_list.remove(index) 
				self.__name_list.remove(index) 
