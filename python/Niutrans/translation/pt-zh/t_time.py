# -*- encoding: utf-8 -*-
isDebug = False

import codecs
import resource.time_translator as t
# translation
preposition = t.preposition
trans_dict = t.direct_trans

class TimeTranslator:
	def __init__(self):
		print ('[time] initialize ... done')
	
	def doTranslate(self, ele_sep):
#		print 'ele_sep', ele_sep
		source = ele_sep[4].strip().lower()
		debug_source = source
		trans = source
		
		try:
			# if exist translation directly, use it
			if source in trans_dict.keys(): 
				trans = trans_dict[source]
			# analyze the translation
			else:
				sp = source.split(' ')
				trans = self.trans_else(sp, source_debug)
#				print 'sp:', sp
				'''if len(sp) == 1:
				else:
					print '\t[date else] len > 5:', debug_source.encode('utf-8'), '-->', trans'''
		except Exception,e:
			trans = self.trans_else(sp, debug_source)
			print '[ERROR] During translating:', e
				
		print (debug_source.encode('utf-8') + '-->' + source.encode('utf-8') + '-->' + trans.encode('utf-8'))
		ele_sep[2] = trans

		return ele_sep

	def isYear(self, s):
		return len(s) == 4 and s.isdigit()
		
	
	def trans_else(self, sp, debug_source):
		result = ''
		tmp_list = []
		for w in sp:
			tmp_list.append(trans_dict.get(w, w))
		result = ' '.join(tmp_list)
		return result
