# ASSIGNMENT 01


---


## TASK 01:

### STEPS TO REMOVE COMMENTS FROM C/C++ CODE:

- copy the file task1_rmcomments.awk to the **same folder** as your C file from task1 folder

- open command line in the directory containing the program and run the command below: (where inputFIle is name of your desired file alongwith necessary filetype)

	`$ awk -f task1_rmcomments.awk inputFile>test2`
	
- the code without comments is saved in a file named test2 in the same directory.

#### Explanation of code:

- Search for occurences of /* and */ in each record. These signify start and end of comments.

- Once /* or */ is found change state of code to inside or outside comment block respectively. We use match function and predefined variables RSTART and RLENGTH to include or exclude desired portion of each record

#### NOTE:

- in case it is not desired to move script.awk to source folder, move it to a desired folder and in the command replace 'task1_rmcomments' with complete address to task1_rmcomments on your device
		
	example:
	
	`$ awk -f .../myfolder/task1_rmcomments.awk inputFile>test2`
		
- test2 will be created in same directory as your source code.


---


## TASK 02:

### STEPS TO CALCULATE TIME DIFFERENCE:
	
- Copy the files create.awk and run.awk to desired directory from task2 folder

- Open command line in the same directory and run the following command:

	`$ awk -f task2_create.awk>test3 && awk -f task2_run.awk test3.txt>test4`

- test3 and test4 are created as required in the task

#### EXPLANATION OF CODE:

- create.awk contains code to print simple tab seperated records as provided in task in test3.txt file. Separator \t has been defined to make life easier.

- run.awk contains conversion code to find time difference as well as convert time to hh:mm:ss format.

- run.awk first takes input from execution of create.awk and converts the times in field 1 and field 2 into respective hour minute and seconds. Then it finds time difference in seconds between the two times.

- Finally it converts difference in seconds to hour min second format again and saves outputs in test4 file with Time1 Time2 and Difference being the columns. 
