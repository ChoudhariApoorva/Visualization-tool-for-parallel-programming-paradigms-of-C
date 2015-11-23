# Visualization-tool-for-parallel-programming-paradigms-of-C

The main aim of the project was to develop a tool to visualize parallel computing paradigms of C. The parallel paradigms considered were OpenMP and Pthreads. The input to the tool was a C program which was run under gdb. The output from gdb was captured in the tool and depicted on the GUI. 
The visualization includes the instruction pointer which indicates the step by step execution of the program. The tool displays how exactly the threads are created and the distribution and/or sharing of the data. It also portrays local variables, global variables, activation records, function parameters (if any). In case of threads, the currently 
executing instruction is highlighted for each thread.

●	The user should have a stable version of python installed.
●	The version of gcc required is gcc 4.4.7.
●	Run "python gui.py" to launch the tool

Sample programs are under the folders - Openmp, Pthreads, Sequential


