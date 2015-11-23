from ttk import *
from Tkinter import *
import tkFileDialog
import tkFont
import tkSimpleDialog
from datastructures import *	
from client import *
from subprocess import call
from os import system
import sys
import copy

class GUI(Frame):
	editors = []
	def __init__(self,parent):
		Frame.__init__(self, parent) 
		self.__class__.editors.append(self)  
		self.customFont = tkFont.Font(family="Helvetica",size="10")
		self.lbFont = tkFont.Font(family="Helvetica", size="12")
		self.parent = parent
		self.init_vars()
		self.init_dict()
		self.initUI()		
	
	def init_vars(self):
		self.k = 0
		self.run_program = 0
		self.main_draw = 0
		self.draw = 0
		self.main_lb_draw = 0
		self.txval_main = 10
		self.tyval_main = 20
		self.txval = 145
		self.tyval = 20
		self.txval_listbox = [10, 145, 280, 415, 10, 145, 280, 415]
		self.tyval_listbox = [20, 20, 20, 20, 240, 240, 240, 240]
		
		self.thread_colors = ['blue','yellow','light sea green','deep pink','tomato','DeepSkyBlue','Chocolate','lightcoral', 'peach puff', 'royal blue', 'gold', 'tan', 'orange', 'pink', 'cyan', 'lime green', 'azure', 'purple', 'coral', 'magenta', 'red', 'PeachPuff2', 'peru', 'olive drab', 'thistle','yellow','light sea green','deep pink','tomato','DeepSkyBlue','Chocolate','lightcoral', 'peach puff', 'royal blue', 'gold', 'tan', 'orange', 'pink', 'cyan', 'lime green', 'azure', 'purple', 'coral', 'magenta', 'red', 'PeachPuff2', 'peru', 'olive drab', 'thistle','yellow','light sea green','deep pink','tomato','DeepSkyBlue','Chocolate','lightcoral']

		self.filename = ""
		self.new = 0
		self.lb = []
		self.globals = 0
		self.place_global_canvas = 0
		self.space = 17
		self.UPDATE_PERIOD = 100 #ms
		self.updateId = None
		self.noOfLines = 1000
		self.info_in_lb = []
		self.main_frame_in_lb = []
		self.startLine = 1
		self.global_var_list = []
		
		self.info_in_lb_threads = defaultdict(list)
		self.main_frame_in_lb_threads = defaultdict(list)
		
		self.notebook_openmp = None
		self.notebook_seq = None
		self.global_listbox = None
		
	def init_dict(self):
		self.d = {'1':1, '2':1, '3':1, '4':2, '5':2, '6':2, '7':3, '8':3, '9':3, '10':4, '11':4, '12':4, '13':5, '14':5, '15':5, '16':6, '17':6, '18':6, '19':7, '20':7, '21':7, '22':8, '23':8, '24':8, '25':9, '26':9, '27':9, '28':10, '29':10, '30':10, '31':11, '32':11, '33':12, '34':12, '35':12, '36':13, '37':13, '38':13, '39':14, '40':14, '41':14, '42':15, '43':15, '44':15, '45':16, '46':16, '47':16, '48':17, '49':17, '50':17, '51':18, '52':18, '53':18, '54':19, '55':19, '56':19, '57':20, '58':20, '59':20, '60':21, '61':21, '62':21, '63':22, '64':22, '65':22, '66':23, '67':23, '68':23, '69':24, '70':24, '71':24, '72':25, '73':25, '74':25, '75':26, '76':26, '77':26, '78':27, '79':27, '80':27, '81':28, '82':28, '83':28, '84':29, '85':29, '86':29, '87':30, '88':30, '89':30, '90':31, '91':31, '92':31, '93':32, '94':32, '95':32, '96':33, '97':33, '98':33, '99':34, '100':34, '101':34, '102':35, '103':35, '104':35, '105':36, '106':36, '107':36, '108':37, '109':37, '110':37}
		
		
	def initUI(self):				#creates all the elements of the GUI
      		self.pack(fill=BOTH, expand=1)
		self.create_text_area()
		self.create_buttons()
		self.textbox1.bind("<Key>", self.check_text_modified)
		self.create_printf_console()

	def create_text_area(self):
		self.lineNumbers = ''

		# A frame to hold the three components of the widget.
		self.frame = Frame(self, bd=2, relief=SUNKEN)

		# The widgets vertical scrollbar
		self.vScrollbar = Scrollbar(self.frame, orient=VERTICAL)
		self.vScrollbar.pack(fill='y', side=RIGHT)

		# The Text widget holding the line numbers.
		self.lnText = Text(self.frame, width=4, padx=4, highlightthickness=0, takefocus=0, cursor='hand2', bd=0, background='lightgrey', foreground='magenta', state='disabled')
		self.lnText.bind("<Button-1>", self.callback_lnText)
		self.lnText.pack(side=LEFT, fill='y')

		# The Main Text Widget
		self.textbox1 = Text(self.frame,width=82,height=35,bd=0,padx = 4,undo=True,background = 'white')
		self.textbox1.pack(side=LEFT, fill=BOTH, expand=1)

		self.textbox1.config(yscrollcommand=self.vScrollbar.set)
		self.vScrollbar.config(command=self.getStartLineNumber)
		
		self.frame.place(x=100, y=30)
		
		self.updateAllLineNumbers()

	def updateAllLineNumbers(self):
		if len(self.editors) < 1:
			self.updateId = None
			return

		for ed in self.editors:
			self.updateLineNumbers()

		self.updateId = ed.textbox1.after(self.UPDATE_PERIOD, self.updateAllLineNumbers)

	def updateLineNumbers(self):
		tt = self.lnText
		ln = self.getLineNumbers()
		if self.lineNumbers != ln:
			self.lineNumbers = ln
			tt.config(state='normal')
			tt.delete('1.0', END)
			tt.insert('1.0', self.lineNumbers)
			tt.config(state='disabled')

	def getStartLineNumber(self, scroll, step, what):
		step = int(step)

		temp = (self.end_limit + 1) - 34
		
		if(step == 1 and self.startLine < temp):
			self.startLine += 1
		elif(step == -1 and self.startLine > 1):
			self.startLine -= 1

		if(self.run_program == 1):
			if(self.seq):
				self.move_pointer(line_num[-2],line_num[-1])
			else:
				thread_info = thread_list_ids()
				if thread_info:
					cur_thread_id = thread_info[0]	
					num_of_threads = thread_info[1]
					self.create_arrows_for_threads(num_of_threads,cur_thread_id,line_num[-1])
    		self.textbox1.yview(scroll, step, what)
		
	def callback_lnText(self, event):
		#set breakpoint
		self.bkpt_line = (event.y / 5)
		bkpt = str(self.bkpt_line)
		for key, value in self.d.iteritems():
			if(key == bkpt):
				value = value + self.startLine - 1
				value = str(value)
				self.disp_breakpoint(value)
		
	def disp_breakpoint(self, bkpt):
		if(bkpt in break_point_dict):
			remove_bkpt(break_point_dict[bkpt])
			del break_point_dict[bkpt]
			
			bkpt = float(bkpt)
			bkpt_end = bkpt + 0.99
		
			self.textbox1.tag_remove("breakpoint", bkpt, bkpt_end)
			
		else:
			insert_bkpt(bkpt)
		
			bkpt = float(bkpt)
			bkpt_end = bkpt + 0.99
				
			self.textbox1.tag_add("breakpoint", bkpt, bkpt_end)
			self.textbox1.tag_config("breakpoint", background="salmon", foreground="purple")
		
	def getLineNumbers(self):
		x = 0
		line = '0'
		col= ''
		ln = ''

		# assume each line is at least 5 pixels high
		step = 5

		nl = '\n'
		lineMask = '    %s\n'
		indexMask = '@0,%d'

		for i in range(0, self.textbox1.winfo_height(), step):
			ll, cc = self.textbox1.index( indexMask % i).split('.')

			if line == ll:
				if col != cc:
					col = cc
					ln += nl
			else:
				line, col = ll, cc
				ln += (lineMask % line)[-5:]

		return ln
	
	def create_buttons(self):
		x = 110
		y = 590

		self.btn1 = Button(self, text ="Choose",command=self.program_option)
		self.btn1.pack()
		self.btn1.place(x=x,y=y)

		self.btn2 = Button(self, text ="Execute",command=self.run)
		self.btn2.pack()
		self.btn2.place(x=x+100,y=y)

		self.btn3 = Button(self, text ="Step",command=self.step)
		self.btn3.pack()
		self.btn3.place(x=x+210,y=y)

		self.btn4 = Button(self, text ="Continue",command=self.cont)
		self.btn4.pack()
		self.btn4.place(x=x+300,y=y)
		
		self.btn5 = Button(self, text="Save", state='disabled', command=self.program_option_user)
		self.btn5.pack()
		self.btn5.place(x=x+410, y=y)

		self.btn6 = Button(self, text ="Clear",command=self.clear)
		self.btn6.pack()
		self.btn6.place(x=x+500,y=y)

		#for radio buttons		
		self.label_rad = Label(self.parent)
	
	def create_printf_console(self):		
		printfFont = tkFont.Font(family="Times",weight=tkFont.BOLD)
		self.printf_area = Text(self.parent,height=5,width=62,bg='LightCoral',font=(printfFont, 12))
		self.printf_area.configure(state='disabled')
		x = 100
		y = 630
		self.printf_area.place(x=x,y=y)
					
	def clear(self):
		self.textbox1.delete("1.0",END)			#clear the textbox
		gdb_exit()  					#end the previous gdb session
		line_num_for_threads.clear()

		if(self.notebook_openmp is not None):
			self.notebook_openmp.destroy()
		if(self.notebook_seq is not None):
			self.notebook_seq.destroy()
		if(self.global_listbox is not None):
			self.global_listbox.delete(0,END)	

		self.mycan = Canvas(self,width=95,height=560, bg="honeydew",bd=0)
		self.mycan.pack()
		self.mycan.place(x=0,y=0)

		self.printf_area.configure(state='normal')
		self.printf_area.delete(1.0,END) 		#clear printf console

		self.init_dict()
		self.init_vars()
					
	def save_as(self):
		self.msgbox_user.destroy()
        	self.msgbox1 = Toplevel()
		self.msgbox1.title('Save File')
		
		self.label0 = Label(self.msgbox1,text='Save as')
		self.label0.pack()

		self.entry1 = Entry(self.msgbox1)
		self.entry1.pack()

		if(self.filename):		
			temp = self.filename.split('/')		#default name will be the same program name
			self.new_file_name = temp[-2] + "/" + temp[-1]
			self.entry1.insert(0, temp[-1])

		self.btn = Button(self.msgbox1,text='Submit',command=self.save)
		self.btn.pack()
		
	def save(self):
		self.new_file_name = self.entry1.get()	
		data = self.textbox1.get("1.0",END)
	
		self.printf_area.configure(state='normal')
		self.printf_area.delete(1.0,END) 		#clear printf console
		
		if(self.seq == 1):
			self.new_file_name = "Sequential/"+self.new_file_name
		elif(self.openmp_prog):
			self.new_file_name = "Openmp/"+self.new_file_name
		else:
			self.new_file_name = "Pthreads/"+self.new_file_name	

		with open(self.new_file_name, "w") as f:
        		f.write(data)
	
        	self.msgbox1.destroy()

		for bkpt in break_point_dict:
			remove_bkpt(break_point_dict[bkpt])
			
		break_point_dict.clear()
		
		self.get_line_count()
		
		for line in range(self.end_limit):
			line = float(line)
			line_end = line + 0.99
			
			self.textbox1.tag_remove("breakpoint", line, line_end)
		
		if(self.seq == 1):
        		self.err_check = call(["gcc","-g",self.new_file_name])
        		if(self.err_check):
				self.error_check()
				return
			self.clear_frames()

		elif(self.openmp_prog):
			self.err_check = call(["gcc","-g",self.new_file_name,"-fopenmp"])
			if(self.err_check):
				self.error_check()
				return
			self.clear_frames()
		
		else:
			self.err_check = call(["gcc","-g",self.new_file_name,"-lpthread"])
			if(self.err_check):
				self.error_check()
				return
			self.clear_frames()


		self.btn5.config(state='disabled')
	
	def clear_frames(self):	
		line_num_for_threads.clear()

		if(self.notebook_openmp is not None):
			self.notebook_openmp.destroy()
		if(self.notebook_seq is not None):
			self.notebook_seq.destroy()
		if(self.global_listbox is not None):
			self.global_listbox.delete(0,END)	
			
		self.mycan = Canvas(self,width=95,height=600, bg="honeydew",bd=0)
		self.mycan.pack()
		self.mycan.place(x=0,y=0)
		
		f = open('global_vars.txt','w') #clear the file
		f.close()
		self.init_dict()
		self.init_vars()
		
		spawn()
		init()				#should be called after the chosen file is executed and a.out generated
		main()
		exec_run()
	
	def program_option_user(self):		
		self.msgbox_user = Toplevel()
		self.msgbox_user.title('Program Option')
		self.label_rad_user = Label(self.msgbox_user,text='Choose the type of program')
		self.label_rad_user.pack()
		
		self.radiovar_user = IntVar()
		self.button_rad1_user = Radiobutton(self.msgbox_user,text="Sequential",variable=self.radiovar_user,value=1,command=self.seq_user)
		self.button_rad2_user = Radiobutton(self.msgbox_user,text="Openmp",variable=self.radiovar_user,value=2,command=self.openmp_user)
		self.button_rad3_user = Radiobutton(self.msgbox_user,text="Pthreads",variable=self.radiovar_user,value=3,command=self.pthreads_user)

		self.button_rad1_user.pack()
		self.button_rad2_user.pack()
		self.button_rad3_user.pack()
	
	def seq_user(self):
		self.seq = 1
		self.save_as()
	
	def openmp_user(self):
		self.openmp_prog = 1
		self.save_as()

	def pthreads_user(self):
		self.pthreads_prog = 1
		self.save_as()
	
   	def program_option(self):
		self.msgbox = Toplevel()
		self.msgbox.title('Program Option')
		self.label_rad = Label(self.msgbox,text='Choose the type of program')
		self.label_rad.pack()
		
		self.radiovar = IntVar()
		self.button_rad1 = Radiobutton(self.msgbox,text="Sequential",variable=self.radiovar,value=1,command=self.seq_prog)
		self.button_rad2 = Radiobutton(self.msgbox,text="Openmp",variable=self.radiovar,value=2,command=self.openmp)
		self.button_rad3 = Radiobutton(self.msgbox,text="Pthreads",variable=self.radiovar,value=3,command=self.pthreads)
		self.button_rad1.pack()
		self.button_rad2.pack()
		self.button_rad3.pack()

	def get_line_count(self):
		if(self.filename):
			f = open(self.filename, "r")
		else:
			f = open(self.new_file_name, "r")

		count = 0
		for lines in f:
			count += 1
		
		self.start_limit = 1
		self.end_limit = count
		
	def seq_prog(self):
		self.msgbox.destroy()
		self.choose_file()
		self.err_check = call(["gcc","-g",self.filename])
		if(self.err_check):
			self.error_check()
			return
		self.get_line_count()
		self.seq = 1			#change flag to indicate that the chosen program is sequential
		self.openmp_prog = 0
		self.pthreads_prog = 0
		spawn()
		init()				#should be called after the chosen file is executed and a.out generated
		main()
		exec_run()

	def openmp(self):
		self.msgbox.destroy()
		self.choose_file()
		self.err_check = call(["gcc","-g",self.filename,"-fopenmp"])
		if(self.err_check):
			self.error_check()
			return
		self.get_line_count()
		self.openmp_prog = 1			#change flag to indicate that the chosen program is an openmp program
		self.seq = 0
		self.pthreads_prog = 0
		spawn()
		init()			
		main()
		exec_run()

	def pthreads(self):
		self.msgbox.destroy()
		self.choose_file()
		self.err_check = call(["gcc","-g",self.filename,"-lpthread"])
		if(self.err_check):
			self.error_check()
			return
		self.get_line_count()
		self.pthreads_prog = 1			#change flag to indicate that the chosen program is a pthreads program
		self.seq = 0
		self.openmp_prog = 0
		spawn()
		init()			
		main()
		exec_run()

	def get_global_vars(self):
		f = open("global_vars.txt","r")
		line = f.readline()

		while line:
			line = line.strip()
			line = line.split()
			self.global_var_list.append(line[-1])
			line = f.readline()
		f.close()
	
	def error_check(self):
		self.msgbox = Toplevel()
		self.msgbox.title('Error')
		self.label_err = Label(self.msgbox,text='The program you have chosen contains errors!!')
		self.label_err.pack()
		self.btn_err = Button(self.msgbox, text="Ok", command=self.msgbox_destroy)
		self.btn_err.pack()
		
	def msgbox_destroy(self):
		self.msgbox.destroy()
		
	def choose_file(self):
		f = tkFileDialog.askopenfile(parent=self,mode='r',title='Choose a file')
		self.filename = f.name
		
		for line in f:
			self.textbox1.insert(END,line)
		
		if f.name:
			self.new = 1
		self.textbox1.bind("<Key>", self.check_text_modified)

	def step(self):
		self.new = 0
		self.textbox1.bind("<Key>", self.check_text_modified)
		fnc_name = exec_step()
		
		if self.seq and fnc_name == "end of program":
			self.lb_main.delete(0,END)
		else:
			self.check_printf()
			self.disp_globals()
			self.call_apt_disp(fnc_name)
		
	def cont(self):
		self.new = 0
		self.textbox1.bind("<Key>", self.check_text_modified)
		fnc_name = exec_cont()
		
		if self.seq and fnc_name == "end of program":
			self.lb_main.delete(0,END)	
		else:
			self.check_printf()
			self.disp_globals()
			self.call_apt_disp(fnc_name)
		
	def disp_globals(self):
		if(self.global_var_list):
			self.globals = 1
			self.place_global_canvas = 1
		else:
			self.globals = 0
			self.place_global_canvas = 0

	def check_printf(self):
		if(printf_list):
			self.printf_area.configure(state='normal')
			self.printf_area.insert(INSERT,printf_list[0][0:-1])
			self.printf_area.insert(INSERT,"\n")
			self.printf_area.configure(state='disabled')
			del printf_list[:]
		
	def check_text_modified(self, event):
		if(self.textbox1.edit_modified):
			self.btn5.config(state='normal')
	
	def call_apt_disp(self,fnc_name):		#call apt display - either sequential display or parallel display
		depth = stack_info_depth()

		if self.seq:				#if it is a sequential program
			self.disp(depth,fnc_name)

		elif self.openmp_prog:
			thread_info = thread_list_ids()

			if thread_info:
				cur_thread_id = thread_info[0]
				num_of_threads = thread_info[1]

				if num_of_threads == 0:
					self.clear_listboxes()

				if num_of_threads == 1:
					self.create_arrows_for_threads(num_of_threads,cur_thread_id,line_num[-1])
					if(self.main_draw == 0):
						self.create_notebook(num_of_threads, cur_thread_id)
						self.create_main_listbox(num_of_threads, cur_thread_id)
						self.main_draw = 1
					self.disp_thread_openmp(depth,num_of_threads,cur_thread_id, fnc_name)
		
				if (num_of_threads > 1) and (num_of_threads < 49):
					self.create_arrows_for_threads(num_of_threads,cur_thread_id,line_num[-1])
					if(self.draw == 0):
						self.create_thread_listbox(num_of_threads, cur_thread_id)
						self.draw = 1
					self.disp_thread_openmp(depth,num_of_threads,cur_thread_id, fnc_name)

		elif self.pthreads_prog:
			thread_info = thread_list_ids()
			
			if thread_info:
				cur_thread_id = thread_info[0]	
				num_of_threads = thread_info[1]
					
				if (num_of_threads == 0):
					self.clear_listboxes()
				
				if(self.main_draw == 0 and self.draw == 0):
					self.create_notebook(num_of_threads, cur_thread_id)
					self.create_main_listbox(num_of_threads, cur_thread_id)
					self.main_draw = 1

					self.create_thread_listbox_pthreads(8, cur_thread_id)	
					self.draw = 1

				if num_of_threads == 1:
					self.create_arrows_for_threads(num_of_threads,cur_thread_id,line_num[-1])
					self.disp_thread_pthreads(depth,num_of_threads,cur_thread_id, fnc_name)
				
				if (num_of_threads > 1) and (num_of_threads < 9):
					self.create_arrows_for_threads(num_of_threads,cur_thread_id,line_num[-1])
					self.disp_thread_pthreads(depth,num_of_threads,cur_thread_id, fnc_name)


	def clear_listboxes(self):
		for i in range(len(self.lb)):
			self.lb[i].pack_forget()
			self.lb[i].destroy()
		self.lb = []
		self.draw = 0
		self.openmp_prog = 0
		self.seq = 0
		self.pthreads_prog = 0

		self.mycan = Canvas(self,width=95,height=600, bg="honeydew",bd=0)
		self.mycan.pack()
		self.mycan.place(x=0,y=0)	

	def create_arrows_for_threads(self,num,thread_id,line_number):
		line_num_for_threads[thread_id] = line_number
		self.create_arrow(num, line_number, thread_id)
	
	def create_arrow(self,num,line_number,thread_id):
		self.mycan = Canvas(self,width=95,height=560)
		self.mycan.pack()
		self.mycan.place(x=0,y=0)
		x = 5

		for i in range(1,num+1):	
			if(line_num_for_threads[i] and i != thread_id):
				offset = line_num_for_threads[i]
	
				if(offset < 15):
					offset = (offset - (self.startLine - 1))*13.5

				else:
					if(self.startLine == 1):
						offset = offset * 14.5
					else:
						offset = (offset - (self.startLine - 1))*14.5
				oval = self.mycan.create_oval(x,40+offset,x+1,40+offset,width=10,outline=self.thread_colors[i-1])
				x += 10

		temp_offset = int(line_number)

		if(temp_offset < 15):
					temp_offset = (temp_offset - (self.startLine - 1))*13.5
		else:
			if(self.startLine == 1):
				temp_offset = temp_offset * 14.5
			else:
				temp_offset = (temp_offset - (self.startLine - 1))*14.5
		
		self.line_th = self.mycan.create_line(65,40+temp_offset,95,40+temp_offset,width=3,fill=self.thread_colors[thread_id-1])
		self.line_th = self.mycan.create_line(80,30+temp_offset,95,40+temp_offset,width=3,fill=self.thread_colors[thread_id-1])
		self.line_th = self.mycan.create_line(95,40+temp_offset,80,50+temp_offset,width=3,fill=self.thread_colors[thread_id-1])	
	
	def create_notebook(self, num_of_threads, cur_thread_id):
		#create a notebook
		self.notebook_openmp = Notebook(self.parent, cursor='hand1')
		
		#add tabs/panes
		self.tab1 = Frame(self.notebook_openmp, width=545, height=455, bg='white')
		self.tab2 = Frame(self.notebook_openmp, width=545, height=455, bg='white')
		self.tab3 = Frame(self.notebook_openmp, width=545, height=455, bg='white')
		self.tab4 = Frame(self.notebook_openmp, width=545, height=455, bg='white')
		self.tab5 = Frame(self.notebook_openmp, width=545, height=455, bg='white')
		self.tab6 = Frame(self.notebook_openmp, width=545, height=455, bg='white')
		
		self.notebook_openmp.add(self.tab1, text = "1 - 8", compound=TOP)
		self.notebook_openmp.add(self.tab2, text = "9 - 16")
		self.notebook_openmp.add(self.tab3, text = "17 - 24")
		self.notebook_openmp.add(self.tab4, text = "25 - 32")
		self.notebook_openmp.add(self.tab5, text = "33 - 40")
		self.notebook_openmp.add(self.tab6, text = "41 - 48")

		if(self.place_global_canvas == 1):
			self.notebook_openmp.place(x=750,y=200)
		else:
			self.notebook_openmp.place(x=750,y=80)
		
	def create_main_listbox(self, num_of_threads, cur_thread_id):
		if (self.main_lb_draw == 0):
			self.lb.append(self.create_listboxes_th(0))
			self.main_lb_draw = 1
		self.lb[0].place(x=self.txval_main, y=self.tyval_main)

	def create_thread_listbox(self, num_of_threads, cur_thread_id):
		if (num_of_threads < 9):
			init = False
			for i in range(1,num_of_threads):
				if(i > 3 and init == False):
					self.txval = 10
					self.tyval = 240
					init = True
				self.disp_listbox_th(i, num_of_threads, cur_thread_id)
				
		else:
			init_up = False
			init_down = False
			for i in range(1,num_of_threads):
				if(((i > 3 and i < 8) or (i > 11 and i < 16) or (i > 19 and i < 24) or (i > 27 and i < 32) or (i > 35 and i < 40) or (i > 43 and i < 48)) and init_down == False):
					self.txval = 10
					self.tyval = 240
					
					init_down = True
					
				if(((i > 7 and i < 12) or (i > 15 and i < 20) or (i > 23 and i < 28) or (i > 31 and i < 36) or (i > 39 and i < 44)) and init_up == False):
					self.txval = 10
					self.tyval = 20
					
					init_up = True
						
				if(i == 7 or i == 15 or i == 23 or i == 31 or i == 39):
						init_down = False
						
				if(i == 11 or i == 19 or i == 27 or i == 35 or i == 43):
						init_up = False
						
				self.disp_listbox_th(i, num_of_threads, cur_thread_id)
			
	def create_listboxes_th(self, num):
		if(num < 8):
			return Listbox(self.tab1, activestyle='dotbox', cursor='hand1', bg='white', height=8, width=12, font=self.lbFont)
		elif(num < 16):
			return Listbox(self.tab2, activestyle='dotbox', cursor='hand1', bg='white', height=8, width=12, font=self.lbFont)
		
		elif(num < 24):
			return Listbox(self.tab3, activestyle='dotbox', cursor='hand1', bg='white', height=8, width=12, font=self.lbFont)
		
		elif(num < 32):
			return Listbox(self.tab4, activestyle='dotbox', cursor='hand1', bg='white', height=8, width=12, font=self.lbFont)
		
		elif(num < 40):
			return Listbox(self.tab5, activestyle='dotbox', cursor='hand1', bg='white', height=8, width=12, font=self.lbFont)
		
		elif(num < 48):
			return Listbox(self.tab6, activestyle='dotbox', cursor='hand1', bg='white', height=8, width=12, font=self.lbFont)
			
	def disp_listbox_th(self, num, num_of_threads, cur_thread_id):
		self.lb.append(self.create_listboxes_th(num))
		
		if(self.pthreads_prog == 1):
			self.txval = self.txval_listbox[num]
			self.tyval = self.tyval_listbox[num]
		
		self.lb[num].place(x=self.txval, y=self.tyval)
		
		if(self.pthreads_prog == 0):
			self.txval += 135
			
	def create_thread_listbox_pthreads(self, num_of_threads, cur_thread_id):
		l = get_active_threads()	#it has the currently active threads
		
		if (num_of_threads < 9):
			init = False
			for i in range(1,num_of_threads):
				if(i > 3 and init == False):
					self.txval = 50
					self.tyval = 240
					init = True
				self.disp_listbox_th(i, num_of_threads, cur_thread_id)	
		self.make_listbox_disabled(num_of_threads)
	
	def make_listbox_disabled(self, num_of_threads):
		for i in range(1,num_of_threads):
			self.lb[i].config(bg="white")
	
	def thread_background(self,thread_id):
		self.lb[thread_id].config(bg=self.thread_colors[thread_id], bd=2)

	def disp_thread_openmp(self, depth,num_of_threads, cur_thread_id, fnc_name):
		rec_call = False

		if(cur_thread_id == 1):
			self.thread_background(0)
		else:
			self.thread_background(cur_thread_id-1)
	
		if(depth == 4 and cur_thread_id != 1):	#openmp main function only
			depth = 1
		elif(depth > 4 and cur_thread_id != 1):	#if depth is 5 => openmp main function and the fnc call
			depth = depth - 3
		
		if depth > 1:
			if(depth == 2):		#it means only one function call after main	
				self.info_in_lb_threads[cur_thread_id-1] = copy.copy(self.main_frame_in_lb_threads[cur_thread_id-1])
				
			else:		
				index = []

				for i,j in enumerate(self.info_in_lb_threads[cur_thread_id-1]):	
					if j == 100*'=':
						index.append(i)
			
				if depth-1 == len(index):	#index gives the number of fnc frames in listbox
					temp = index[-1]
					length = len(self.info_in_lb_threads[cur_thread_id-1])
					clear_index = length - temp
					del self.info_in_lb_threads[cur_thread_id-1][-clear_index:]
				
				elif depth <= len(index):	#recursive calls
					self.lb[cur_thread_id-1].delete(index[-1],END)
					temp = index[-1]
					length = len(self.info_in_lb_threads[cur_thread_id-1])
					clear_index = length - temp
					del self.info_in_lb_threads[cur_thread_id-1][-clear_index:]
					rec_call = True
					self.disp_fnc_in_listbox_threads(cur_thread_id)

			if(not rec_call):
				stack_select_frame(0)			# select the current function's frame
				stack_list_locals()
				
				self.info_in_lb_threads[cur_thread_id-1].append(100*'=')

				if fnc_name:
					self.info_in_lb_threads[cur_thread_id-1].append(fnc_name + " function frame")

				self.disp_variables_in_fnc_frames_threads(cur_thread_id)
		else:									#if depth == 1
			self.info_in_lb_threads[cur_thread_id-1] = []
			stack_list_locals()
			self.info_in_lb_threads[cur_thread_id-1].append("Thread id = " + str(cur_thread_id))			
			if(fnc_name):
				self.info_in_lb_threads[cur_thread_id-1].append(fnc_name + " function frame")
			self.get_variables_in_main_frame_threads(cur_thread_id)

				
	def disp_thread_pthreads(self,depth,num_of_threads,cur_thread_id, fnc_name):
		rec_call = False
		
		if(cur_thread_id == 1):
			self.thread_background(0)
		else:
			self.thread_background(cur_thread_id-1)

		if(self.pthreads_prog and depth > 1):
			depth = depth - 2
		
		if(depth > 1):	
			if(depth == 2):		#it means only one function call after main
				self.info_in_lb_threads[cur_thread_id-1] = copy.copy(self.main_frame_in_lb_threads[cur_thread_id-1])
		
			else:		
				index = []

				for i,j in enumerate(self.info_in_lb_threads[cur_thread_id-1]):	
					if j == 100*'=':
						index.append(i)
			
				if depth-1 == len(index):	#index gives the number of fnc frames in listbox
					temp = index[-1]
					length = len(self.info_in_lb_threads[cur_thread_id-1])
					clear_index = length - temp
					del self.info_in_lb_threads[cur_thread_id-1][-clear_index:]
				
				elif depth <= len(index):	#recursive calls
					self.lb[cur_thread_id-1].delete(index[-1],END)
					temp = index[-1]
					length = len(self.info_in_lb_threads[cur_thread_id-1])
					clear_index = length - temp
					del self.info_in_lb_threads[cur_thread_id-1][-clear_index:]
					rec_call = True
					self.disp_fnc_in_listbox_threads(cur_thread_id)
		
			if(not rec_call):
				stack_select_frame(0)			# select the current function's frame
				stack_list_locals()

				self.info_in_lb_threads[cur_thread_id-1].append(100*'=')
				if fnc_name:
					self.info_in_lb_threads[cur_thread_id-1].append(fnc_name + " function frame")

				self.disp_variables_in_fnc_frames_threads(cur_thread_id)

		else:
			self.info_in_lb_threads[cur_thread_id-1] = []
			stack_list_locals()
			self.info_in_lb_threads[cur_thread_id-1].append("Thread id = " + str(cur_thread_id))			
			if(fnc_name):
				self.info_in_lb_threads[cur_thread_id-1].append(fnc_name + " function frame")
			self.get_variables_in_main_frame_threads(cur_thread_id)
		
	def get_variables_in_main_frame_threads(self,cur_thread_id):
		if(self.globals == 1 and self.place_global_canvas == 1):			
			self.global_listbox = Listbox(self.parent,height=5,width=50,bg='white',font=("Helvetica",12))
			self.global_listbox.place(x=750,y=10)	
			self.global_listbox.insert(END,"Global Variables")
			self.notebook_openmp.place(x=750, y=200)

			for i in self.global_var_list:	
				if(data_evaluate_expression_var(i)):
					self.global_listbox.insert(END,i + " = " + data_evaluate_expression_var(i))

			self.globals = 0

		else:
			self.notebook_openmp.place(x=750, y=10)
						
		for key in local_var_dict:
			if len(local_var_dict[key][0]) > 2 and local_var_dict[key][0][0]+local_var_dict[key][0][1] == "0x":#pointer
				ptr_value = data_evaluate_expression(key)
				local_var_dict[key] = ptr_value
				self.info_in_lb_threads[cur_thread_id-1].append(str(key)+"---->"+str(ptr_value))

			elif(local_var_dict[key][0] and local_var_dict[key][0][0] == '{'):	#it is an array
				self.get_arr_values(key)

				self.info_in_lb_threads[cur_thread_id-1].append(key + "[ ] = ")

				for a in self.arr:
					self.info_in_lb_threads[cur_thread_id-1].append(a)
				
			else:	
				self.info_in_lb_threads[cur_thread_id-1].append(str(key)+" = "+local_var_dict[key][0])
				
		local_var_dict.clear()
		self.disp_in_listbox_threads(cur_thread_id)

	def disp_in_listbox_threads(self,cur_thread_id):
		if(self.place_global_canvas == 1):
			self.notebook_openmp.place(x=750,y=200)
		else:
			self.notebook_openmp.place(x=750,y=10)
			
		self.lb[cur_thread_id-1].delete(0,END)

		for i in self.info_in_lb_threads[cur_thread_id-1]:
			self.lb[cur_thread_id-1].insert(END,i)

		self.main_frame_in_lb_threads[cur_thread_id-1] = copy.copy(self.info_in_lb_threads[cur_thread_id-1])
		self.info_in_lb_threads[cur_thread_id-1] = []	
	
	def disp_fnc_in_listbox_threads(self,cur_thread_id):
		if(self.place_global_canvas == 1):
			self.notebook_openmp.place(x=750,y=200)
		else:
			self.notebook_openmp.place(x=750,y=10)
		
		self.lb[cur_thread_id-1].delete(0,END)

		for i in self.info_in_lb_threads[cur_thread_id-1]:
			self.lb[cur_thread_id-1].insert(END,i)
		
	def disp_variables_in_fnc_frames_threads(self,cur_thread_id):
		if(self.place_global_canvas == 1):
			self.notebook_openmp.place(x=750,y=200)
		else:
			self.notebook_openmp.place(x=750,y=10)
			
		stack_list_args()		#function to collect arguments of all the functions

		for i in range(len(args_dict[0])):
			self.info_in_lb_threads[cur_thread_id-1].append(args_dict[0].keys()[i] + " = " +args_dict[0].values()[i])
			
		for key in local_var_dict:		
			if len(local_var_dict[key][0]) > 2 and local_var_dict[key][0][0]+local_var_dict[key][0][1] == "0x":#pointer
				ptr_value = data_evaluate_expression(key)
				local_var_dict[key] = ptr_value
				self.info_in_lb_threads[cur_thread_id-1].append(str(key)+"---->"+str(ptr_value))

			elif(local_var_dict[key][0] and local_var_dict[key][0][0] == '{'):	#it is an array
				self.get_arr_values(key)

				self.info_in_lb_threads[cur_thread_id-1].append(key + "[ ] = ")
				for a in self.arr:
					self.info_in_lb_threads[cur_thread_id-1].append(a)
				
			else:
				self.info_in_lb_threads[cur_thread_id-1].append(str(key)+" = "+local_var_dict[key][0])
				
		local_var_dict.clear()
		self.disp_fnc_in_listbox_threads(cur_thread_id)
				

	def disp(self,depth,fnc_name):
		rec_call = False			#assuming it is not a recursive call
		if(depth > 1):	
			if(depth == 2):		#it means only one function call after main
				self.info_in_lb = copy.copy(self.main_frame_in_lb)
			
			else:			#enters this before the 3rd function frame is created because depth becomes greater than 2
				index = []

				for i,j in enumerate(self.info_in_lb):	#get all indices with the string (100*'=').. marks end of a func
					if j == 100*'=':
						index.append(i)
				
				if depth-1 == len(index):	#index gives the number of fnc frames in listbox
					temp = index[-1]
					length = len(self.info_in_lb)
					clear_index = length - temp
					del self.info_in_lb[-clear_index:]
					
				elif depth <= len(index):	#recursive calls. Clear frame when depth == number of frames in listbox
					self.lb_main.delete(index[-1],END)
					temp = index[-1]
					length = len(self.info_in_lb)
					clear_index = length - temp
					del self.info_in_lb[-clear_index:]
					rec_call = True
					self.disp_fnc_in_listbox()
			
			if(not rec_call):
				stack_select_frame(0)			# select the current function's frame
				stack_list_locals()
			
				self.move_pointer(line_num[-2],line_num[-1])

				self.info_in_lb.append(100*'=')
				if fnc_name:
					self.info_in_lb.append(fnc_name + " function frame")

				self.disp_variables_in_fnc_frames()
						
		else:
			self.info_in_lb = []		#if control returns to main.. clear rest of the frames
			stack_list_locals()
			self.move_pointer(line_num[-2],line_num[-1])
			self.info_in_lb.append("Main frame")
			self.get_variables_in_main_frame()
	
	def get_variables_in_main_frame(self):
		if(self.globals == 1 and self.place_global_canvas == 1):			
			self.global_listbox = Listbox(self.parent,height=5,width=50,bg='white',font=("Helvetica",12))
			self.global_listbox.place(x=750,y=10)	
			self.global_listbox.insert(END,"Global Variables")
			self.notebook_seq.place(x=750, y=200)

			for i in self.global_var_list:
				self.global_listbox.insert(END,i + " = " + data_evaluate_expression_var(i))

			self.globals = 0

		else:
			self.notebook_seq.place(x=750, y=10)
						
		for key in local_var_dict:
			if len(local_var_dict[key][0]) > 2 and local_var_dict[key][0][0]+local_var_dict[key][0][1] == "0x":#pointer
				ptr_value = data_evaluate_expression(key)
				local_var_dict[key] = ptr_value
				self.info_in_lb.append(str(key)+"---->"+str(ptr_value))

			elif(local_var_dict[key][0] and local_var_dict[key][0][0] == '{'):	#it is an array
				self.get_arr_values(key)
				self.info_in_lb.append(key + "[ ] = ")
				for a in self.arr:
					self.info_in_lb.append(a)
			else:	
				self.info_in_lb.append(str(key)+" = "+local_var_dict[key][0])
				
		local_var_dict.clear()
		self.disp_in_listbox()

	def disp_in_listbox(self):
		if(self.place_global_canvas == 1):
			self.notebook_seq.place(x=750,y=200)
		else:
			self.notebook_seq.place(x=750,y=10)
			
		self.lb_main.delete(0,END)

		for i in self.info_in_lb:
			self.lb_main.insert(END,i)

		self.main_frame_in_lb = copy.copy(self.info_in_lb)
		self.info_in_lb = []

	def disp_variables_in_fnc_frames(self):
		if(self.place_global_canvas == 1):
			self.notebook_seq.place(x=750,y=200)
		else:
			self.notebook_seq.place(x=750,y=10)
			
		stack_list_args()		#function to collect arguments of all the functions

		for i in range(len(args_dict[0])):
			self.info_in_lb.append(args_dict[0].keys()[i] + " = " +args_dict[0].values()[i])
			
		for key in local_var_dict:		
			if len(local_var_dict[key][0]) > 2 and local_var_dict[key][0][0]+local_var_dict[key][0][1] == "0x":#pointer
				ptr_value = data_evaluate_expression(key)
				local_var_dict[key] = ptr_value
				self.info_in_lb.append(str(key)+"---->"+str(ptr_value))

			elif(local_var_dict[key][0] and local_var_dict[key][0][0] == '{'):	#it is an array
				self.get_arr_values(key)
				self.info_in_lb.append(key + "[ ] = ")
				for a in self.arr:
					self.info_in_lb.append(a)
			else:
				self.info_in_lb.append(str(key)+" = "+local_var_dict[key][0])
				
		local_var_dict.clear()
		self.move_pointer(line_num[-2],line_num[-1])
		self.disp_fnc_in_listbox()

	def disp_fnc_in_listbox(self):
		if(self.place_global_canvas == 1):
			self.notebook_seq.place(x=750,y=200)
			self.global_listbox = Listbox(self.parent,height=5,width=50,bg='white',font=("Helvetica",12))
			self.global_listbox.place(x=750,y=10)	
			self.global_listbox.insert(END,"Global Variables")
			self.notebook_seq.place(x=750, y=200)

			for i in self.global_var_list:
				self.global_listbox.insert(END,i + " = " + data_evaluate_expression_var(i))

			self.globals = 0
		else:
			self.notebook_seq.place(x=750,y=10)
			
		self.lb_main.delete(0,END)

		for i in self.info_in_lb:
			self.lb_main.insert(END,i)

	def get_arr_values(self, key):
		self.arr = local_var_dict[key][0]
		self.arr = self.arr.replace('{', '')
		self.arr = self.arr.replace('}', '')
		self.arr = self.arr.split(',')

	def run(self):			#places the arrow at the beginning of the program
		self.run_program = 1
		if self.seq:
			system("readelf -s a.out | grep GLOBAL | grep OBJECT | grep -v '_' > global_vars.txt")	#to get global vars
			self.get_global_vars()
			self.sequential_gui()
		else:
			system("readelf -s a.out | grep GLOBAL | grep OBJECT | grep -v '_' > global_vars.txt")	#to get global vars
			self.get_global_vars()

		self.mycan = Canvas(self,width=95,height=560, bg="honeydew",bd=0)
		self.mycan.pack()
		self.mycan.place(x=0,y=0)
	
		offset = int(line_num[self.k])
		offset = offset*16
		self.k += 1
		
		line_start_x = 65
		line_end_x = 95

		self.line = self.mycan.create_line(line_start_x, 40+offset, line_end_x, 40+offset, width=3, fill='red')
		self.line = self.mycan.create_line(line_start_x+15, 30+offset, line_end_x, 40+offset, width=3, fill='red')
		self.line = self.mycan.create_line(line_start_x+30, 40+offset, line_end_x-15, 50+offset, width=3, fill='red')


	def sequential_gui(self):
		self.notebook_seq = Notebook(self.parent, cursor='hand1')
		self.main_tab = Frame(self.notebook_seq, width=545, height=700, bg='thistle')
		self.notebook_seq.add(self.main_tab, text = "Main Thread Display", compound=TOP)
		
		if(self.place_global_canvas == 1):
			self.notebook_seq.place(x=750,y=50)
		elif(self.place_global_canvas == 0):
			self.notebook_seq.place(x=750, y=10)		
		
		self.lb_main = Listbox(self.main_tab,height=33,width=60,bg='white',font=("Helvetica",11))
		self.lb_main.place(x=20, y=5)

		if(self.place_global_canvas == 1):
			self.lb_main.config(height=23)
		
			
	def move_pointer(self,line_number1,line_number2):		#Goes through the program step by step based on the line numbers
		self.mycan = Canvas(self,width=95,height=560, bg="honeydew",bd=0)
		self.mycan.pack()
		self.mycan.place(x=0,y=0)
		
		offset1 = int(line_number1)
		offset2 = int(line_number2)

		if(offset1 < 13):
			offset1 = (offset1 - (self.startLine - 1))*13.5
		
		if(offset2 < 13):
			offset2 = (offset2 - (self.startLine - 1))*13.5
			
		else:

			if(self.startLine == 1):
				offset1 = offset1*14.5
				offset2 = offset2*14.5
			
			else:
				offset1 = (offset1 - (self.startLine - 1))*14.5
				offset2 = (offset2 - (self.startLine - 1))*14.5

		line_start_x = 65
		line_end_x = 95
		
		self.line = self.mycan.create_line(line_start_x, 40+offset1, line_end_x, 40+offset1, width=3, fill='green')
		self.line = self.mycan.create_line(line_start_x+15, 30+offset1, line_end_x, 40+offset1, width=3, fill='green')
		self.line = self.mycan.create_line(line_start_x+30, 40+offset1, line_end_x-15, 50+offset1, width=3, fill='green')
	
		self.line = self.mycan.create_line(line_start_x,40+offset2,line_end_x,40+offset2,width=3, fill='red')
		self.line = self.mycan.create_line(line_start_x+15,30+offset2,line_end_x,40+offset2,width=3, fill='red')
		self.line = self.mycan.create_line(line_start_x+30,40+offset2,line_end_x-15,50+offset2,width=3, fill='red') 	

def gui_main():
	root = Tk()
	root.geometry("2500x1500+300+300")
	root.title('GUI for parallel programs')	
	root.option_add("*background", "honeydew")
	app = GUI(root)
	root.mainloop()

gui_main()
