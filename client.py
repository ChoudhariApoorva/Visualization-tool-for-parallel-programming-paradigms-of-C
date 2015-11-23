import pexpect
import time
from get_info import *	

child = 0

def spawn():
	global child
	child = pexpect.spawn('gdb -q -i mi')
	
def init():
	global child
	time.sleep(0.01)
	child.expect('.*\r\n')
	child.sendline('-file-exec-and-symbols a.out')
	time.sleep(0.01)
	child.expect('.*\r\n')

def main():
	global child
	child.sendline('-break-insert main')
	time.sleep(0.05)
	child.expect('.*\r\n')
	get_line_num(line_pat,child.after)

def exec_run():
	global child
	child.sendline('-exec-run')
	time.sleep(1)
	child.expect('.*\r\n')

def insert_bkpt(bkptno):
	global child
	child.sendline('-break-insert '+bkptno)
	time.sleep(0.01)
	child.expect('.*\r\n')
	insert_bkpts_in_dict(child.after)

def remove_bkpt(bkptno):
	global child
	child.sendline('-break-delete '+bkptno)
	time.sleep(0.01)
	child.expect('.*\r\n')

def exec_step():
	global child
	child.sendline('-exec-step')
	time.sleep(0.01)
	child.expect('.*\r\n')
	end = check_prog_end(child.after)
	
	if end:
		return "end of program"	

	get_printf_string(child.after)
	get_line_num(line_pat,child.after)
	return get_func_name(child.after)

def exec_cont():
	global child
	child.sendline('-exec-continue')
	time.sleep(0.02)
	child.expect('.*\r\n')
	end = check_prog_end(child.after)
	
	if end:
		return "end of program"	

	get_printf_string(child.after)
	get_line_num(line_pat,child.after)
	return get_func_name(child.after)

def stack_list_locals():
	global child
	child.sendline('-stack-list-locals 1')
	time.sleep(0.01)
	child.expect('.*\r\n')
	get_locals(name_pat,value_pat,child.after)
	
def stack_list_args():
	global child
	child.sendline('-stack-list-arguments 1')
	time.sleep(0.01)
	child.expect('.*\r\n')
	get_args(child.after)

def gdb_exit():
	global child
	child.sendline('-gdb-exit')
	time.sleep(0.01)
	child.expect('.*\r\n')

def stack_info_depth():
	global child
	child.sendline('-stack-info-depth')
	time.sleep(0.01)
	child.expect('.*\r\n')
	return get_stack_depth(depth_pat,child.after)

def stack_select_frame(depth):
	global child
	child.sendline('-stack-select-frame '+str(depth))
	time.sleep(0.01)
	child.expect('.*\r\n')

def data_evaluate_expression(key):
	global child
	child.sendline('-data-evaluate-expression *'+key)
	time.sleep(0.01)
	child.expect('.*\r\n')
	return get_pointer_value(child.after)

def data_evaluate_expression_var(key):
	global child
	child.sendline('-data-evaluate-expression '+key)
	time.sleep(0.01)
	child.expect('.*\r\n')
	return get_var_value(child.after)		

def stack_list_frames():
	global child
	child.sendline('-stack-list-frames')
	time.sleep(0.01)
	child.expect('.*\r\n')
	func_name_dict.clear()
	get_all_funcs(child.after)

def thread_list_ids():
	global child
	child.sendline('-thread-list-ids')
	time.sleep(0.01)
	child.expect('.*\r\n')
	return thread_info(child.after)

def select_thread(num):
	global child
	child.sendline('-thread-select '+str(num))
	time.sleep(0.01)
	child.expect('.*\r\n')

def get_active_threads():
	global child
	child.sendline('-thread-list-ids')
	time.sleep(0.01)
	child.expect('.*\r\n')
	return active_threads(child.after)
