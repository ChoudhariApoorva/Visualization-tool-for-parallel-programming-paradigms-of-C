import re
from datastructures import *		# which defines the line_num list and the local_var default dict
from collections import *		# OrderedDict

line_pat = 'line=\"([0-9]+)\"'
num_pat = 'number=\"([0-9]+)\"'
name_pat = 'name=\"([a-zA-Z_0-9]+)\"'		# () to group only the name
value_pat = 'value=\"(.*?)\"'
depth_pat = 'depth=\"([0-9]+)\"'
frame_pat = 'frame={(.*?)]}'
level_pat = 'level=\"([0-9])+\"'
func_pat = 'func=\"(.*?)\"'
cur_thread_pat = 'current-thread-id=\"([0-9]+)\"'
num_of_threads_pat = 'number-of-threads=\"([0-9]+)\"'
active_threads_pat = 'thread-id=\"([0-9]+)\"'
string_pat = 'value=\"(.*?)}'
printf_pat = '[^*^(-=~]\n([^*^(-=~](.*))\n'
return_val_pat = 'return-value=\"(.*?)\"'

def get_printf_string(sub):
	m = re.search(printf_pat,sub)

	if m:
		printf_list.append(m.group(1))

def get_line_num(pat,sub):
	n = re.search(pat,sub)		
	if n:
		num = int(n.group(1))
		line_num.append(num)

def get_func_name(sub):
	f = re.search(func_pat,sub)
	if f:
		fnc_name = f.group(1)
		return fnc_name

def get_stack_depth(pat,sub):
	m = re.search(pat,sub)	
	if m:
		depth = int(m.group(1))
		return depth

def get_locals(name_pat,val_pat,sub):
	name = re.findall(name_pat,sub)			#finds all matches in the subject
	val = re.findall(val_pat,sub)

	temp = re.findall(string_pat,sub)			#to find string.. HAS TO BE MODIFIED.. CHECK
	temp = str(temp)
	final_string_pat = '\"(.*?)\\\\'
	r = re.search(final_string_pat,temp)
	str_name = ""
	
	if(r):
		str_name = r.group(1)

	if(val):					#if value is a character change it in the local_var_dict
		for i in range(len(val)):
			if '\'' in val[i]:
				pat = '\'(.*?)\''
				r = re.search(pat,val[i])
				char_name = r.group(1)
				val[i] = char_name

			if "0x" in val[i] and str_name:
				val[i] = str_name
		
	if name and val:
		for i in range(len(name)):
			if name[i] not in local_var:	#check if the variable is not in the local_var list already
				local_var.append(name[i])
			local_var_dict[name[i]].append(val[i])


def get_args(sub):
	m = re.findall(frame_pat,sub)				#find all the levels and their corresponding name and value pairs
	
	temp = re.findall(string_pat,sub)			#to find string
	temp = str(temp)
	final_string_pat = '\"(.*?)\\\\'
	r = re.search(final_string_pat,temp)
	str_name = ""
	
	if(r):
		str_name = r.group(1)

	for i in range(len(m)):
		n = re.search(level_pat,m[i])			#find the level
		level  = int(n.group(1))
		name = re.findall(name_pat,m[i])		#find the name
		val = re.findall(value_pat,m[i])		#find corresponding values

		if(val):					#if value is a string change it in the args_dict
			for i in range(len(val)):
				if "0x" in val[i] and str_name:
					val[i] = str_name
				else:
					pass

				if '\'' in val[i]:
					pat = '\'(.*?)\''
					r = re.search(pat,val[i])
					char_name = r.group(1)
					val[i] = char_name

		args_dict[level] = OrderedDict()		#store the name-value pairs in a dictionary indexed by the level
		
		for j in range(len(name)):
			args_dict[level][name[j]] = val[j]

def get_pointer_value(sub):
	p = re.search(value_pat,sub)
	
	if p:
		return p.group(1)

def get_var_value(sub):
	p = re.search(value_pat,sub)
	
	if p:
		return p.group(1)

def get_all_funcs(sub):
	f = re.findall(func_pat,sub)
	for i in range(len(f)):
		func_name_dict[i] = f[i]

def thread_info(sub):
	c = re.search(cur_thread_pat,sub)
	if c:
		c = int(c.group(1))
	
	n = re.search(num_of_threads_pat,sub)
	if n:
		n = int(n.group(1))
	
	info = []
	info.append(c)
	info.append(n)
	return info

def check_prog_end(sub):
	if "The program is not being run." in sub:
		return True
	else:
		return False

def active_threads(sub):
	temp_pat = '{(.*)}'
	temp_sub = re.findall(temp_pat,sub)
	temp_sub = str(temp_sub)
	
	active_thread_list = re.findall(active_threads_pat,temp_sub)
	return active_thread_list

def insert_bkpts_in_dict(sub):
	temp_l = re.search(line_pat,sub)
	temp_n = re.search(num_pat,sub)

	if(temp_l and temp_n):
		l = temp_l.group(1)
		n = temp_n.group(1)
		
		break_point_dict[l] = n
