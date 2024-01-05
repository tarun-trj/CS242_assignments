# ASSIGNMENT 02

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

## TASK 01:

### STEPS TO SEARCH LINES WITH SPECIFIED STRING IN A GIVEN FILE:

- copy the file search.sh to the **same folder** as the desired file from task1 folder

- open command line in the directory containing the program and run the command below: (where <string> is unquoted string you wish to search and <file_name> is name of the file you want to search in)

	`$ chmod +x search.sh && ./search.sh "<string>" <file_name>`
	
- all matched lines are returned as output in the terminal along with line number of match.

- as a sample test.txt file has been provided to run the code on. to check extract task1 directory and open terminal in it and execute:

	`$ chmod +x search.sh && ./search.sh "Hello" test.txt`

#### EXPLANATION OF CODE:

- check for validity of arguments using $# variable which stores number of arguments in a script.

- Validity testing checks whether exactly twoo arguments are present and whether the second argument is a non empty readable file.

- once validity is verified proceed to search every line for matches. to avoid repetitions due to several matches in one line grep was quietened using -q command to return true/false values instead of standard grep output.

- upon match the matched line is displayed along with the line number.

- loop till file has been exhausted

#### NOTE:

- in case it is not desired to move search.sh to source directory, move it to a desired directory and in the command replace <file_name> with complete address to input file on your device
		
	example:
	
	`$ chmod +x search.sh && ./search.sh "<string>" drive/path/to/input/file/input.txt`
		
- output will be displayed in the same terminal


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


## TASK 02:

### STEPS TO SEND MESSAGES FROM INPUT FILE TO ALL LOGGED IN USERS:
	
- Copy the greet.sh to desired directory from task2 directory to the directory containing the file with message

- Open command line in the same directory and run the following command: (where <name_of_message_file> is the file name of file with messages)

	`$ chmod +x greet.sh && ./greet.sh <name_of_message_file>`

- message to every user is sent from the message file.

- as a sample msg.txt file has been provided to run the code on. to check, extract task2 directory, open terminal in it and execute:

	`$ chmod +x greet.sh && ./greet.sh msg.txt`



#### EXPLANATION OF CODE:

- validity of arguments is tested using several conditional statements.

- validity checks are: number of arguments must be 2, message file must exist and must be readable, message file must not be empty (in order in the code)

- upon validation who command and awk script are used to create a temporary file containing a non repeating list of currently logged in users.

- finally loop through the temp file and send message to every user except sender via write command from the input file.

- because write command is disabled for sending messages to self, use echo command to greet yourself.

- after exiting while loop, delete the temp file using rm command.

#### NOTE:

- in case it is not desired to move greet.sh to source directory, move it to a desired directory and in the command replace <name_of_message_file> with complete address to input file on your device
		
	example:
	
	`$ chmod +x search.sh && ./search.sh drive/path/to/input/file/input.txt`
