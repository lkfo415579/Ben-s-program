# -*-encoding: UTF-8 -*-
import os
import sys
import math
def main():
	if len(sys.argv) != 2:
		print 'Input: alignment file;\tOutput: *.tau, *.p_value'
		print 'Usage: python', sys.argv[0], 'input-alignment'
		exit()
		
	align_file_name = sys.argv[1]

	avg_tau = calculate_kendall_average(align_file_name)
        print "Final result for kendall's tau: \n", avg_tau
        fw = open(align_file_name+'kendall_tau', 'w')
        fw.write(str(avg_tau)+'\n')
        fw.close()
	
	
def calculate_kendall_average(file_name):
	import scipy.stats as stats

	fr = open(file_name, 'r')
	fw_tau = open(file_name + '.tau', 'w')
	fw_p = open(file_name + '.p_value', 'w')
	
	index = 0
	sum_tau = 0.0
	s_list, t_list = [], []
	for line in fr:
		index += 1
		if index % 100 == 0:
			sys.stdout.write('line: %d\t avg_tau: %f\r' % (index, sum_tau/index))
			#sys.stdout.write('line: %d\t avg_tau: %f\n' % (index, sum_tau/index))
			sys.stdout.flush()

		# initial value			
		s_list, t_list = [], []

		sep_line = line.strip().split(' ')
		for ele in sep_line:
			sep_ele = ele.split('-')
			s_list.append(sep_ele[0])
			t_list.append(sep_ele[1])
	
		if len(t_list) == len(s_list):
			tau, p_value = stats.kendalltau(s_list, t_list)
			if math.isnan(tau):
				tau = 0
			
			fw_tau.write(str(tau) + '\n')
			fw_p.write(str(p_value) + '\n')
			sum_tau += tau
		else:
			print('The size of the source and target is not same: ' + line)
	
	fr.close()
	fw_tau.close()
	fw_p.close()
	
	return sum_tau/index

if __name__ == '__main__':
	main()
