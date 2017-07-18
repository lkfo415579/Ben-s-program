# -*- encoding: utf-8 -*-
isDebug = False

import codecs
import resource.date_translator as d
# translation
month = d.month
day = d.day
preposition = d.preposition
trans_dict = d.direct_trans

class DateTranslator:
	def __init__(self):
		print ('[date] initialize ... done')
	
	def doTranslate(self, ele_sep):
#		print 'ele_sep', ele_sep
		source = ele_sep[4].strip().lower()
		debug_source = source
		source = source.replace(', ', ' ').replace(' , ', ' ').replace(',', ' ').replace(' de ', ' ').replace(' / ', ' ').replace(' /', ' ').replace('/ ', ' ').replace('/', ' ')
		source = source.replace(' a ', '-').replace(' para ', '-').replace(' - ', '-') # range
		trans = source
		
		try:
			# if exist translation directly, use it
			if source in trans_dict.keys(): 
				trans = trans_dict[source]
			# analyze the translation
			else:
				sp = source.split(' ')
#				print 'sp:', sp
				if len(sp) == 1:
					trans = self.trans_len1(sp, debug_source)
				elif len(sp) == 2:
					trans = self.trans_len2(sp, debug_source)
				elif len(sp) == 3:
					trans = self.trans_len3(sp, debug_source)
				elif len(sp) == 4:
					trans = self.trans_len4(sp, debug_source)
				elif len(sp) == 5:
					trans = self.trans_len5(sp, debug_source)
				else:
					trans = self.trans_else(sp, debug_source)
					print '\t[date else] len > 5:', debug_source.encode('utf-8'), '-->', trans
		except Exception,e:
			trans = self.trans_else(sp, debug_source)
			print '[ERROR] During translating:', e
				
		#print (debug_source.encode('utf-8') + '-->' + source.encode('utf-8') + '-->' + trans.encode('utf-8'))
		ele_sep[2] = trans

		return ele_sep

	def trans_day_month_year(self, d, m, y):
		result = ""
		if len(y) > 0:
			result += y + trans_dict['ano']
		if len(m) > 0:
			result += month[m]
		if len(d) > 0:
			result += day.get(d, d)
		return result

	def trans_rangeday_month_year(self, rd, m, y):
		result = ""
		if len(y) > 0:
			result += y + trans_dict['ano']
		if len(m) > 0:
			result += month.get(m, m)
		if len(rd) > 0:
			rd_from, rd_to = rd.split('-')
			if rd_from in day and rd_to in day:
				result += day.get(rd_from, rd_from) + trans_dict['para'] + day.get(rd_to)
			else:
				result += rd
		return result
	
	def trans_pre_year(self, pre, y):
		return preposition.get(pre, pre) + y + trans_dict['ano']
		
	def trans_pre_rangeyear(self, pre, ry):
		result = ''
		if len(pre) > 0:
			result += preposition.get(pre, pre)
		ry_from, ry_to = ry.split('-')
		if ry_from.isdigit() and ry_to.isdigit():
			result += ry_from + trans_dict['para'] + ry_to + trans_dict['ano']
		else:
			result += ry
		return result
		
	def trans_pre_rangemonth(self, pre, rm):
		result = ''
		if len(pre) > 0:
			result += preposition.get(pre, pre)
		rm_from, rm_to = rm.split('-')
		if rm_from in month and rm_to in month:
			result += month.get(rm_from, rm_from) + trans_dict['para'] + month.get(rm_to, rm_to)
		else:
			result += rm
		return result
	
	def isYear(self, s):
		return len(s) == 4 and s.isdigit()

	def trans_len1(self, sp, debug_source):
		result = debug_source
		if sp[0].count('-') > 0:
			sp0 = sp[0].split('-')
			if len(sp[0]) == 9 and self.isYear(sp0[0]) and self.isYear(sp0[1]): # yyyy-yyyy
				result = self.trans_pre_rangeyear('', sp[0])
			elif len(sp0) == 2 and sp0[0] in month and sp0[1] in month:
				result = self.trans_pre_rangemonth('', sp[0])
			elif len(sp[0]) == 10 and len(sp0) == 3 and sp0[0] in day and sp0[1] in month and self.isYear(sp0[2]): # dd-mm-yyyy
				result = self.trans_day_month_year(sp0[0], sp0[1], sp0[2])
			elif len(sp[0]) == 10 and len(sp0) == 3 and sp0[1] in day and sp0[0] in month and self.isYear(sp0[2]): # mm-dd-yyyy
				result = self.trans_day_month_year(sp0[1], sp0[0], sp0[2])
			elif len(sp[0]) == 19 and len(sp0) == 4 and self.isYear(sp0[0]) and self.isYear(sp0[1]) and self.isYear(sp0[2]) and self.isYear(sp0[3]): # yyyy-yyyy-yyyy-yyyy
				result = sp0[0] + "-" + sp0[1] + trans_dict['ano'] + trans_dict['para'] + sp0[2] + '-' + sp0[3] + trans_dict['ano']
			else:
				print '\t[date else]len = 1:', debug_source.encode('utf-8')
				result = self.trans_else(sp, debug_source)
		return result
		
	def trans_len2(self, sp, debug_source):
		result = debug_source
		if   sp[0] in day and sp[1] in month: # dd mm
			result = self.trans_day_month_year(sp[0], sp[1], '')
		elif sp[1] in day and sp[0] in month: # mm dd
			result = self.trans_day_month_year(sp[1], sp[0], '')
		elif sp[0] in month and self.isYear(sp[1]): # mm yyyy
			result = self.trans_day_month_year('', sp[0], sp[1])
		elif sp[0] in month and sp[1].count('-') > 0: # mm dd-dd
			result = self.trans_rangeday_month_year(sp[1], sp[0], '')
		elif sp[1] in month and sp[0].count('-') > 0: # dd-dd mm
			result = self.trans_rangeday_month_year(sp[0], sp[1], '')
		elif sp[0].count('-') > 0 and sp[0].split('-')[0] in month and sp[0].split('-')[1] in month and self.isYear(sp[1]): # mm-mm yyyy
			result = sp[1] + trans_dict['ano'] + self.trans_pre_rangemonth('', sp[0])
		# em/desde/ate
		elif sp[0] in preposition and self.isYear(sp[1]): # pp yyyy
			result = self.trans_pre_year(sp[0], sp[1])
		elif sp[0] in preposition and len(sp[1]) == 9 and sp[1].count('-') > 0: # pp yyyy-yyyy
			result = self.trans_pre_rangeyear(sp[0], sp[1])
		else:
			print '\t[date else]len = 2:', debug_source.encode('utf-8')
			result = self.trans_else(sp, debug_source)
		return result
	
	def trans_len3(self, sp, debug_source):
		result = debug_source
		if   sp[0] in day and sp[1] in month and self.isYear(sp[2]): # dd mm yyyy
			result = self.trans_day_month_year(sp[0], sp[1], sp[2])
		elif sp[1] in day and sp[0] in month and self.isYear(sp[2]): # mm dd yyyy
			result = self.trans_day_month_year(sp[1], sp[0], sp[2])
		elif sp[0].count('-') > 0 and sp[1] in month and self.isYear(sp[2]): # dd-dd mm yyyy
			result = self.trans_rangeday_month_year(sp[0], sp[1], sp[2])
		elif sp[1].count('-') > 0 and sp[0] in month and self.isYear(sp[2]): # mm dd-dd yyyy
			result = self.trans_rangeday_month_year(sp[1], sp[0], sp[2])
		elif sp[1].count('-') > 0 and sp[0] in day and sp[1].split('-')[0] in month and sp[1].split('-')[1] in day and sp[2] in month: # dd mm-dd mm
			result = self.trans_day_month_year(sp[0], sp[1].split('-')[0], '') + trans_dict['para']
			result += self.trans_day_month_year(sp[1].split('-')[1], sp[2], '')
		elif sp[1].count('-') > 0 and sp[0] in day and sp[1].split('-')[0] in month and sp[1].split('-')[1] in month and self.isYear(sp[2]): # dd mm-mm yyyy
			result = self.trans_day_month_year(sp[0], sp[1].split('-')[0], sp[2]) + trans_dict['para']
			result += self.trans_day_month_year(sp[0], sp[1].split('-')[1], '')
		else:
			print '\t[date else]len = 3:', debug_source.encode('utf-8')
			result = self.trans_else(sp, debug_source)
		return result
	
	def trans_len4(self, sp, debug_source):
		result = debug_source
		if sp[1].count('-') > 0: # xx xx-xx xx xx
			sp1 = sp[1].split('-')
			if 	sp[0] in day and sp1[0] in month and sp1[1] in day and sp[2] in month and self.isYear(sp[3]): # dd mm-dd mm yyyy
				result = sp[3] + trans_dict['ano']
				result += self.trans_len2([sp[0], sp1[0]], sp[0] + " " + sp1[0])
				result += trans_dict['para']
				result += self.trans_len2([sp1[1], sp[2]], sp1[1] + " " + sp[2])
			else:
				print '\t[date else]len = 4, has (-):', debug_source.encode('utf-8')
				result = self.trans_else(sp, debug_source)
		else:
			print '\t[date else]len = 4, no (-):', debug_source.encode('utf-8')
			result = self.trans_else(sp, debug_source)
		return result

	def trans_len5(self, sp, debug_source):
		result = debug_source
		if sp[2].count('-') > 0: # xx xx xx-xx xx xx
			sp2 = sp[2].split('-')
			if 	sp[0] in day and sp[1] in month and self.isYear(sp2[0]) and sp2[1] in day and sp[3] in month and self.isYear(sp[4]): # dd mm yyyy-dd mm yyyy
				result = self.trans_len3([sp[0], sp[1], sp2[0]], ' '.join([sp[0], sp[1], sp2[0]]))
				result += trans_dict['para']
				result += self.trans_len3([sp2[1], sp[3], sp[4]], ' '.join([sp2[1], sp[3], sp[4]]))
			else:
				print '\t[date else]len = 5, has (-):', debug_source.encode('utf-8')
				result = self.trans_else(sp, debug_source)
		elif sp[1] == 'e' or sp[1] == 'ou':
			if sp[0] in day and sp[2] in day and sp[3] in month and self.isYear(sp[4]): # dd e/ou dd mm yyyy
				result = self.trans_day_month_year(sp[0], sp[3], sp[4])
				result += trans_dict[sp[1]] + trans_dict[sp[2]]
		else:
			print '\t[date else]len = 5, no (-):', debug_source.encode('utf-8')
			result = self.trans_else(sp, debug_source)
		return result

	def trans_else(self, sp, debug_source):
		result = ''
		try_split_de = [x.strip() for x in debug_source.split(' de ')]
		try_split_para = [x.strip() for x in debug_source.split(' para ')]
		print try_split_de, try_split_para
		if len(try_split_de) == 2 and try_split_de[0] in day and try_split_de[1] in month: # dd de mm
			result = self.trans_day_month_year(try_split_de[0], try_split_de[1], '')
		elif len(try_split_de) == 3 and try_split_de[0] in day and try_split_de[1] in month and self.isYear(try_split_de[2]): # dd de mm de yyyy
			result = self.trans_day_month_year(try_split_de[0], try_split_de[1], try_split_de[2])
		elif len(try_split_de) == 3 and try_split_de[1] in day and try_split_de[0] in month and self.isYear(try_split_de[2]): # mm de dd de yyyy
			result = self.trans_day_month_year(try_split_de[1], try_split_de[0], try_split_de[2])
		elif len(try_split_para) == 2 and try_split_para[0] in trans_dict and try_split_para[1] in trans_dict:
			result = trans_dict.get(try_split_para[0]) + trans_dict['para'] + trans_dict.get(try_split_para[1])
		else:
			tmp_list = []
			for w in sp:
				tmp_list.append(trans_dict.get(w, w))
			result = ' '.join(tmp_list)
		return result
		
	
